"""
EPICS Archiver Appliance Data Source helpers.

Data source reference:
https://sasaki77.github.io/archiverappliance-datasource/
"""

import attr

from grafanalib.validators import is_list_of, is_in
from attr.validators import instance_of, optional


# List of valid operators that can be used in a query.
OPERATORS = frozenset(
    [
        # Defaul
        "",
        # Other operator options
        "firstSample",
        "lastSample",
        "firstFill",
        "lastFill",
        "mean",
        "min",
        "max",
        "count",
        "ncount",
        "nth",
        "median",
        "std",
        "jitter",
        "ignoreflyers",
        "flyers",
        "variance",
        "popvariance",
        "kurtosis",
        "skewness",
        "raw",
        "last",
    ]
)


@attr.s(frozen=True)
class FunctionDefinitionParam(object):
    """
    Archiver function definition parameters.

    Generally created automatically for you by way of
    `FunctionDefinition.from_json_data`.

    :param name: The parameter name.
    :param options: The parameter options (i.e., value should be one of these).
    :param type: The parameter type name.
    """

    name = attr.ib(default="", validator=instance_of(str))
    options = attr.ib(default=None, validator=optional(is_list_of(str)))
    type = attr.ib(default="", validator=instance_of(str))

    @classmethod
    def from_json_data(cls, data):
        """Create a function definition parameter from its JSON source."""
        return cls(**data)

    def validate_value(self, value):
        """
        Validate ``value`` for this specific parameter type.

        Raises an exception if invalid, and returns a possibly modified value.

        :param value: The value to check.
        """
        if self.type == "int":
            # Raise if not a valid integer:
            int(value)
            return value
        if self.type == "float":
            # Raise if not a valid float:
            float(value)
            return value
        if self.type == "string":
            if not self.options:
                return str(value)

            if set(self.options) == {"true", "false"}:
                # Special case booleans to make this a bit more friendly
                if isinstance(value, bool):
                    return {
                        True: "true",
                        False: "false",
                    }[value]

            if value in self.options:
                return value
            raise ValueError("{1!r} not a valid option {0.options}".format(self, value))
        raise RuntimeError("Unhandled type: {0.type}".format(self))

    def to_json_data(self):
        json_data = {
            "name": self.name,
            "type": self.type,
        }
        if self.options:
            json_data["options"] = self.options
        return json_data


@attr.s(frozen=True)
class FunctionDefinition(object):
    """
    Archiver data function definition.

    :param name: The function name.
    :param defaultParams: Default parameters, if unspecified
    :param shortName: Short name or alias of the function.
    :param version: Optional version marker for the function.
    :param category: Category the function fits in.
    :param description: Description of the function.
    :param fake: A reserved parameter for the function definition.
    :param params: Function parameter information.
    """

    name = attr.ib(default="", validator=instance_of(str))
    defaultParams = attr.ib(factory=list, validator=is_list_of(str))
    shortName = attr.ib(default=None, validator=optional(instance_of(str)))
    version = attr.ib(default=None, validator=optional(instance_of(str)))
    category = attr.ib(default="", validator=instance_of(str))
    description = attr.ib(default=None, validator=optional(instance_of(str)))
    fake = attr.ib(default=None, validator=optional(instance_of(bool)))
    params = attr.ib(factory=list, validator=is_list_of(FunctionDefinitionParam))

    def __call__(self, *args):
        """
        Generate a ``FunctionDescriptor`` by calling this definition.

        Allows for easy use of ``transform_scale`` and other pre-defined
        EPICS Archiver Appliance functions.
        """
        if len(self.params) != len(args):
            raise ValueError(
                "Invalid parameters for {0.name} args={1!r}. "
                "Function definition parameters: {0.params}".format(self, args)
            )

        validated_args = [
            param.validate_value(value) for param, value in zip(self.params, args)
        ]

        return FunctionDescriptor(
            defn=self,
            params=[str(value) for value in validated_args],
        )

    @classmethod
    def from_json_data(cls, data):
        """Create a function definition based on its JSON source."""
        return cls(
            name=data["name"],
            params=[
                FunctionDefinitionParam.from_json_data(param)
                for param in data["params"]
            ],
            category=data["category"],
            defaultParams=data["defaultParams"],
            shortName=data.get("shortName", None),
        )

    def to_json_data(self):
        json_data = {
            "defaultParams": self.defaultParams,
            "category": self.category,
            "name": self.name,
            "params": self.params,
        }
        if self.shortName is not None:
            json_data["shortName"] = self.shortName
        if self.version is not None:
            json_data["version"] = self.version
        if self.description is not None:
            json_data["description"] = self.description
        if self.fake is not None:
            json_data["fake"] = self.fake
        return json_data


@attr.s
class FunctionDescriptor(object):
    """
    Archiver function descriptor, used when *calling* a function.

    :param defn: The definition of the function to be called.
    :param params: The parameters to pass to that function.
    """

    defn = attr.ib(validator=instance_of(FunctionDefinition))
    params = attr.ib(factory=list, validator=is_list_of(str))

    def to_json_data(self):
        return {
            "params": self.params,
            "def": self.defn,
        }


@attr.s
class ArchiverTargetQuery(object):
    """
    Archiver Appliance Data Source target query JSON structure.

    Data source reference:
    https://sasaki77.github.io/archiverappliance-datasource/

    :param target: Process Variable name - PV name. Regular expression is
        allowed here if "regex" is set.
    :param alias: Alias for the legend.
    :param aliasPattern: Set regular expression pattern to use PV name for
        legend alias. Alias pattern is used to match PV name. Matched
        characters within parentheses can be used in Alias text input like $1,
        $2, ... $n.
    :param functions: Functions are used to apply post-processing to the data.
        Use ``grafanalib.archiverappliance.function(*args)`` to easily specify
        these.
    :param operator: Controls processing of data during data retrieval. Refer
        Archiver Appliance User Guide about processing of data. Special
        operators "raw" and "last" are also available. "raw" allows to retrieve
        the data without processing. "last" allows to retrieve the last data in
        the specified time range.
    :param refId: Reference ID for referring to this query Grafana.
    :param regex: Is "target" a regular expression?
    :param stream: Stream data without reloading the dashboard?
    :param streamCapacity: The stream data is stored in a circular buffer.
        Capacity determines the buffer size. The default is determined by
        initial data size.
    :param streamInterval: Streaming interval in milliseconds. You can also
        use a number with unit. e.g. 1s, 1m, 1h. The default is determined by
        width of panel and time range.
    """

    alias = attr.ib(default="", validator=instance_of(str))
    aliasPattern = attr.ib(default="", validator=instance_of(str))
    functions = attr.ib(
        factory=list,
        validator=is_list_of(FunctionDescriptor),
    )
    operator = attr.ib(default="", validator=is_in(OPERATORS))
    refId = attr.ib(default="", validator=instance_of(str))
    regex = attr.ib(default=False, validator=instance_of(bool))
    stream = attr.ib(default=False, validator=instance_of(bool))
    streamCapacity = attr.ib(default="", validator=instance_of(str))
    streamInterval = attr.ib(default="", validator=instance_of(str))
    target = attr.ib(default="", validator=instance_of(str))

    def to_json_data(self):
        return {
            "alias": self.alias,
            "aliasPattern": self.aliasPattern,
            "functions": self.functions,
            "operator": self.operator,
            "refId": self.refId,
            "regex": self.regex,
            "stream": self.stream,
            "strmCap": self.streamCapacity,
            "strmInt": self.streamInterval,
            "target": self.target,
        }


transform_scale = FunctionDefinition.from_json_data(
    {
        "name": "scale",
        "category": "Transform",
        "params": [{"name": "factor", "type": "float"}],
        "defaultParams": ["100"],
    }
)

transform_offset = FunctionDefinition.from_json_data(
    {
        "name": "offset",
        "category": "Transform",
        "params": [{"name": "delta", "type": "float"}],
        "defaultParams": ["100"],
    }
)

transform_delta = FunctionDefinition.from_json_data(
    {
        "name": "delta",
        "category": "Transform",
        "params": [],
        "defaultParams": [],
    }
)

transform_fluctuation = FunctionDefinition.from_json_data(
    {
        "name": "fluctuation",
        "category": "Transform",
        "params": [],
        "defaultParams": [],
    }
)

transform_moving_average = FunctionDefinition.from_json_data(
    {
        "name": "movingAverage",
        "category": "Transform",
        "params": [{"name": "windowSize", "type": "int"}],
        "defaultParams": ["10"],
    }
)

array_to_scalar_by_average = FunctionDefinition.from_json_data(
    {
        "name": "toScalarByAvg",
        "category": "Array to Scalar",
        "params": [],
        "defaultParams": [],
    }
)

array_to_scalar_by_max = FunctionDefinition.from_json_data(
    {
        "name": "toScalarByMax",
        "category": "Array to Scalar",
        "params": [],
        "defaultParams": [],
    }
)

array_to_scalar_by_min = FunctionDefinition.from_json_data(
    {
        "name": "toScalarByMin",
        "category": "Array to Scalar",
        "params": [],
        "defaultParams": [],
    }
)

array_to_scalar_by_sum = FunctionDefinition.from_json_data(
    {
        "name": "toScalarBySum",
        "category": "Array to Scalar",
        "params": [],
        "defaultParams": [],
    }
)

array_to_scalar_by_median = FunctionDefinition.from_json_data(
    {
        "name": "toScalarByMed",
        "category": "Array to Scalar",
        "params": [],
        "defaultParams": [],
    }
)

array_to_scalar_by_std = FunctionDefinition.from_json_data(
    {
        "name": "toScalarByStd",
        "category": "Array to Scalar",
        "params": [],
        "defaultParams": [],
    }
)

filter_top = FunctionDefinition.from_json_data(
    {
        "name": "top",
        "category": "Filter Series",
        "params": [
            {"name": "number", "type": "int"},
            {
                "name": "value",
                "type": "string",
                "options": ["avg", "min", "max", "absoluteMin", "absoluteMax", "sum"],
            },
        ],
        "defaultParams": ["5", "avg"],
    }
)

filter_bottom = FunctionDefinition.from_json_data(
    {
        "name": "bottom",
        "category": "Filter Series",
        "params": [
            {"name": "number", "type": "int"},
            {
                "name": "value",
                "type": "string",
                "options": ["avg", "min", "max", "absoluteMin", "absoluteMax", "sum"],
            },
        ],
        "defaultParams": ["5", "avg"],
    }
)

filter_exclude = FunctionDefinition.from_json_data(
    {
        "name": "exclude",
        "category": "Filter Series",
        "params": [{"name": "pattern", "type": "string"}],
        "defaultParams": [""],
    }
)

sort_by_average = FunctionDefinition.from_json_data(
    {
        "name": "sortByAvg",
        "category": "Sort",
        "params": [{"name": "order", "type": "string", "options": ["desc", "asc"]}],
        "defaultParams": ["desc"],
    }
)

sort_by_max = FunctionDefinition.from_json_data(
    {
        "name": "sortByMax",
        "category": "Sort",
        "params": [{"name": "order", "type": "string", "options": ["desc", "asc"]}],
        "defaultParams": ["desc"],
    }
)

sort_by_min = FunctionDefinition.from_json_data(
    {
        "name": "sortByMin",
        "category": "Sort",
        "params": [{"name": "order", "type": "string", "options": ["desc", "asc"]}],
        "defaultParams": ["desc"],
    }
)

sort_by_sum = FunctionDefinition.from_json_data(
    {
        "name": "sortBySum",
        "category": "Sort",
        "params": [{"name": "order", "type": "string", "options": ["desc", "asc"]}],
        "defaultParams": ["desc"],
    }
)

sort_by_abs_max = FunctionDefinition.from_json_data(
    {
        "name": "sortByAbsMax",
        "category": "Sort",
        "params": [{"name": "order", "type": "string", "options": ["desc", "asc"]}],
        "defaultParams": ["desc"],
    }
)

sort_by_abs_min = FunctionDefinition.from_json_data(
    {
        "name": "sortByAbsMin",
        "category": "Sort",
        "params": [{"name": "order", "type": "string", "options": ["desc", "asc"]}],
        "defaultParams": ["desc"],
    }
)

options_max_num_pvs = FunctionDefinition.from_json_data(
    {
        "name": "maxNumPVs",
        "category": "Options",
        "params": [{"name": "number", "type": "int"}],
        "defaultParams": ["100"],
    }
)

options_bin_interval = FunctionDefinition.from_json_data(
    {
        "name": "binInterval",
        "category": "Options",
        "params": [{"name": "interval", "type": "int"}],
        "defaultParams": ["900"],
    }
)

options_disable_auto_raw = FunctionDefinition.from_json_data(
    {
        "name": "disableAutoRaw",
        "category": "Options",
        "params": [{"name": "boolean", "type": "string", "options": ["true", "false"]}],
        "defaultParams": ["true"],
    }
)

options_disable_extrapolation = FunctionDefinition.from_json_data(
    {
        "name": "disableExtrapol",
        "category": "Options",
        "params": [{"name": "boolean", "type": "string", "options": ["true", "false"]}],
        "defaultParams": ["true"],
    }
)
