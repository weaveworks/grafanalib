import json
import string

import grafanalib._gen as _gen
import grafanalib.core as G
import pytest

import hypothesis.strategies as st
from hypothesis import HealthCheck, given, settings


def colors():
    """Generate arbitrary value from 0 to 255, for RGB color."""
    return st.integers(min_value=0, max_value=255)


def alphas():
    """Generate alpha values"""
    return st.floats(min_value=0, max_value=1)


def rgbas():
    """Generate arbitrary, valid RGBA objects."""
    return st.builds(G.RGBA, r=colors(), g=colors(), b=colors(), a=alphas())


def rgbs():
    """Generate arbitrary, valid RGB objects."""
    return st.builds(G.RGB, r=colors(), g=colors(), b=colors())


def pixels():
    """Generate arbitrary valid Pixels object"""
    return st.builds(G.Pixels, num=st.integers(min_value=0))


def percents():
    """Generate arbitrary valid Percent objects"""
    return st.builds(G.Percent, num=st.integers(min_value=0, max_value=100))


def mappings():
    """Generate arbitrary valid Mapping objects"""
    return st.builds(G.Mapping, name=st.text(), value=st.integers())


def unknown():
    return st.text(string.printable)


def grids():
    """Generate arbitrary valid Grrid objects"""
    return st.builds(
        G.Grid,
        threshold1=unknown(),
        threshold1Color=rgbas(),
        threshold2=unknown(),
        threshold2Color=rgbas(),
        leftLogBase=unknown(),
        rightLogBase=unknown(),
        rightMin=unknown(),
        rightMax=unknown(),
        leftMin=unknown(),
        leftMax=unknown()
    )


def legends():
    """Generate arbitrary valid Legend objects"""
    return st.builds(
        G.Legend,
        avg=st.booleans(),
        current=st.booleans(),
        max=st.booleans(),
        min=st.booleans(),
        show=st.booleans(),
        total=st.booleans(),
        values=unknown(),
        alignAsTable=st.booleans(),
        hideEmpty=st.booleans(),
        hideZero=st.booleans(),
        rightSide=st.booleans(),
        sideWidth=unknown(),
        sort=unknown(),
        sortDesc=unknown()
    )

@st.composite
def targets(draw):
    """Generate arbitrary valid Legend objects
    NOTE: Uses @st.composte as both st.builds and the G.Target object use
          parameter named `target`"""
    return G.Target(
        expr=draw(unknown()),
        legendFormat=draw(st.text(string.printable)),
        intervalFactor=draw(st.integers()),
        metric=draw(st.text(string.printable)),
        refId=draw(st.text(string.printable)),
        step=draw(st.integers()),
        hide=draw(st.booleans()),
        format=draw(unknown()),
        calculatedInterval=draw(unknown()),
        datasourceErrors=draw(unknown()),
        errors=draw(unknown()),
        interval=draw(unknown()),
        target=draw(unknown()),
        alias=draw(unknown()),
        dimensions=draw(unknown()),
        metricName=draw(unknown()),
        namespace=draw(unknown()),
        period=draw(unknown()),
        region=draw(unknown()),
        statistics=draw(unknown())
    )


def tooltips():
    """Generate arbitrary valid Tooltip objects"""
    return st.builds(
        G.Tooltip,
        msResolution=st.booleans(),
        shared=st.booleans(),
        sort=st.integers(),
        valueType=st.text(string.printable)
    )


def xaxes():
    """Generate arbitrary valid XAxis objects"""
    return st.builds(
        G.XAxis,
        # XAxis loses information
        mode=st.sampled_from(("time", )),  # , "series")),
        name=st.none(),
        values=st.lists(max_size=0),
        show=st.booleans(),
        buckets=st.none()
    )


def yaxes():
    """Generate arbitrary valid YXaxis objects"""
    return st.builds(
        G.YAxis,
        decimals=unknown(),
        format=unknown(),
        label=unknown(),
        logBase=st.integers(),
        max=unknown(),
        min=st.integers(),
        show=st.booleans()
    )


def yaxeses():
    """Generate arbitrary valid YAxes objects"""
    return st.builds(G.YAxes, left=yaxes(), right=yaxes())


def graphs():
    """Generate arbitrary valid Graph objects"""
    return st.builds(
        G.Graph,
        title=unknown(),
        dataSource=unknown(),
        targets=st.lists(targets()),
        aliasColors=st.dictionaries(st.text(), st.integers()),
        bars=st.booleans(),
        description=unknown(),
        editable=st.booleans(),
        error=st.booleans(),
        fill=st.integers(),
        grid=grids(),
        id=unknown(),
        isNew=st.booleans(),
        legend=legends(),
        lines=st.booleans(),
        lineWidth=st.integers(),
        links=st.lists(max_size=0),
        nullPointMode=st.text(string.printable),
        percentage=st.booleans(),
        pointRadius=st.integers(),
        points=st.booleans(),
        renderer=st.text(string.printable),
        seriesOverrides=st.lists(max_size=0),
        span=st.integers(),
        stack=st.booleans(),
        steppedLine=st.booleans(),
        timeFrom=unknown(),
        timeShift=unknown(),
        tooltip=tooltips(),
        transparent=st.booleans(),
        xAxis=xaxes()
    )


def tables():
    """Generate arbitrary valid Table objects"""
    return st.builds(
        G.Table,
        columns=unknown(),
        dataSource=unknown(),
        editable=unknown(),
        error=unknown(),
        fontSize=unknown(),
        height=pixels(),
        hideTimeOverride=unknown(),
        id=unknown(),
        links=st.lists(max_size=0),
        pageSize=unknown(),
        scroll=unknown(),
        showHeader=unknown(),
        sort=unknown(),
        span=st.integers(),
        styles=unknown(),
        targets=st.lists(targets()),
        timeFrom=unknown(),
        title=unknown(),
        transform=unknown(),
        transparent=unknown(),
        filterNull=unknown()
    )


def texts():
    """Generate arbitrary valid Text objects"""
    return st.builds(
        G.Text,
        content=st.text(string.printable),
        editable=st.booleans(),
        error=st.booleans(),
        height=unknown(),
        id=unknown(),
        links=st.lists(max_size=0),
        mode=st.sampled_from(('markdown', 'html', 'text')),
        span=st.integers(),
        title=st.text(string.printable),
        transparent=st.booleans(),
        dataSource=unknown(),
        style=unknown(),
        isNew=unknown()
    )


def singlestats():
    """Generate arbitrary valid SingleStat objects"""
    return st.builds(
        G.SingleStat,
        dataSource=unknown(),
        targets=st.lists(targets()),
        title=unknown(),
        cacheTimeout=unknown(),
        colors=st.lists(rgbas()),
        colorBackground=st.booleans(),
        colorValue=st.booleans(),
        description=unknown(),
        decimals=unknown(),
        editable=st.booleans(),
        format=unknown(),
        gauge=gauges(),
        height=pixels(),
        hideTimeOverride=st.booleans(),
        id=unknown(),
        interval=unknown(),
        links=st.lists(max_size=0),
        mappingType=st.integers(),
        mappingTypes=st.lists(mappings(), min_size=2, max_size=2),
        maxDataPoints=st.integers(),
        minSpan=unknown(),
        nullText=unknown(),
        nullPointMode=unknown(),
        postfix=unknown(),
        postfixFontSize=unknown(),
        prefix=unknown(),
        prefixFontSize=unknown(),
        rangeMaps=st.lists(max_size=0),
        repeat=unknown(),
        span=st.integers(),
        sparkline=sparklines(),
        thresholds=unknown(),
        transparent=st.booleans(),
        valueFontSize=unknown(),
        valueName=unknown(),
        valueMaps=st.lists(max_size=0),
        tableColumn=unknown(),
        error=unknown(),
        timeFrom=unknown(),
        timeShift=unknown()
    )


def panels():
    """Generate arbitrary valid Panel objects which can be graphs, singlestats,
    tables or texts"""
    return graphs() | singlestats() | tables() | texts()


def rows():
    """Generate arbitrary valid Row objects"""
    return st.builds(
        G.Row,
        panels=st.lists(elements=panels()),
        collapse=st.booleans(),
        editable=st.booleans(),
        height=pixels(),
        showTitle=unknown(),
        title=unknown(),
        repeat=unknown(),
        repeatIteration=unknown(),
        repeatRowId=unknown(),
        titleSize=unknown()
    )


def sparklines():
    """Generate arbitrary valid SparkLine objects"""
    return st.builds(
        G.SparkLine,
        fillColor=rgbas(),
        full=st.booleans(),
        lineColor=rgbs(),
        show=st.booleans()
    )


def valuemaps():
    """Generate arbitrary valid ValueMap objects"""
    return st.builds(G.ValueMap, op=unknown(), text=unknown(), value=unknown())


def rangemaps():
    """Generate arbitrary valid RangeMap objects"""
    return st.builds(G.RangeMap, start=unknown(), end=unknown(), text=unknown())


def gauges():
    """Generate arbitrary valid Gauge objects"""
    return st.builds(
        G.Gauge,
        minValue=st.integers(),
        maxValue=st.integers(),
        show=st.booleans(),
        thresholdLabels=st.booleans(),
        thresholdMarkers=st.booleans()
    )


def datasources():
    """Generate arbitrary valid DataSourceInput objects"""
    return st.builds(
        G.DataSourceInput,
        name=unknown(),
        label=unknown(),
        pluginId=unknown(),
        pluginName=unknown(),
        description=unknown()
    )


def constantinputs():
    """Generate arbitrary valid ConstantInput objects"""
    return st.builds(
        G.ConstantInput,
        name=unknown(),
        label=unknown(),
        value=unknown(),
        description=unknown())


def inputs():
    """Generate arbitrary valid input objects which can be datasources or
    constantinputs"""
    return datasources() | constantinputs()


def annotations():
    """Generate arbitrary valid Annotations objects"""
    return st.builds(G.Annotations, list=st.lists(max_size=0))


def templating():
    """Generate arbitrary valid Templating objects"""
    return st.builds(G.Templating, list=st.lists(max_size=0))


def templates():
    """Generate arbitrary valid Template objects"""
    return st.builds(
        G.Template,
        default=unknown(),
        dataSource=unknown(),
        label=unknown(),
        name=unknown(),
        query=unknown(),
        allValue=unknown(),
        includeAll=st.booleans(),
        multi=st.booleans(),
        regex=unknown()
    )


def times():
    """Generate arbitrary valid Time objects"""
    return st.builds(G.Time, start=unknown(), end=unknown())


def timepickers():
    """Generate arbitrary valid TimePicker objects"""
    return st.builds(
        G.TimePicker,
        refreshIntervals=unknown(),
        timeOptions=unknown(),
        collapse=st.booleans(),
        enable=unknown(),
        notice=unknown(),
        now=unknown(),
        status=unknown()
    )


def dashboards():
    """Generate arbitrary valid Dashboard objects"""
    return st.builds(
        G.Dashboard,
        title=st.text(string.printable),
        rows=st.lists(rows()),
        annotations=annotations(),
        editable=st.booleans(),
        gnetId=unknown(),
        hideControls=st.booleans(),
        id=unknown(),
        inputs=st.lists(inputs()),
        links=st.lists(max_size=0),
        refresh=unknown(),
        schemaVersion=st.integers(),
        sharedCrosshair=st.booleans(),
        style=unknown(),
        tags=st.lists(max_size=0),
        templating=templating(),
        time=times(),
        timePicker=timepickers(),
        timezone=unknown(),
        version=st.integers(),
        graphTooltip=st.integers()
    )


def json_round_trip(obj):
    """Dumps the object to a JSON and load it back. This is necessary as the
    DashboardEncoder takes care of nested structures """
    output = json.dumps(obj.to_json_data(), cls=_gen.DashboardEncoder)
    return json.loads(output)


@pytest.mark.parametrize(("generator", "parser"), [
    (rgbs, G.RGB),
    (rgbas, G.RGBA),
    (pixels, G.Pixels),
    (percents, G.Percent),
    (mappings, G.Mapping),
    (grids, G.Grid),
    (legends, G.Legend),
    (targets, G.Target),
    (tooltips, G.Tooltip),
    (xaxes, G.XAxis),
    (yaxes, G.YAxis),
    (yaxeses, G.YAxes),
    (graphs, G.Graph),
    (singlestats, G.SingleStat),
    (tables, G.Table),
    (texts, G.Text),
    (rows, G.Row),
    (sparklines, G.SparkLine),
    (valuemaps, G.ValueMap),
    (rangemaps, G.RangeMap),
    (gauges, G.Gauge),
    (datasources, G.DataSourceInput),
    (constantinputs, G.ConstantInput),
    (templates, G.Template),
    (annotations, G.Annotations),
    (times, G.Time),
    (timepickers, G.TimePicker),
    (templating, G.Templating),
    (dashboards, G.Dashboard),
])
def test_roundtrip(generator, parser):
    @settings(suppress_health_check=[HealthCheck.too_slow])
    @given(original=generator())
    def round_trip(original):
        json_dict = json_round_trip(original)
        parsed = parser.parse_json_data(json_dict)
        assert original == parsed

    round_trip()
