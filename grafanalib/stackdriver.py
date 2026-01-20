import attr
from attr.validators import in_, instance_of
from typing import Optional

AP_CLOUD_MONITORING_AUTO = 'cloud-monitoring-auto'
AP_GRAFANA_AUTO = 'cloud-monitoring-auto'
AP_1M = '+60s'
AP_2M = '+120s'
AP_5M = '+300s'
AP_10M = '+600s'
AP_30M = '+1800s'
AP_1H = '+3600s'
AP_2H = '+7200s'

CSR_REDUCE_NONE = 'REDUCE_NONE'
CSR_REDUCE_MEAN = 'REDUCE_MEAN'
CSR_REDUCE_MAX = 'REDUCE_MAX'
CSR_REDUCE_MIN = 'REDUCE_MIN'
CSR_REDUCE_SUM = 'REDUCE_SUM'
CSR_REDUCE_STDDEV = 'REDUCE_STDDEV'

PSA_ALIGN_NONE = 'ALIGN_NONE'
PSA_ALIGN_INTERPOLATE = 'ALIGN_INTERPOLATE'
PSA_ALIGN_NEXT_OLDER = 'ALIGN_NEXT_OLDER'
PSA_ALIGN_MIN = 'ALIGN_MIN'
PSA_ALIGN_MAX = 'ALIGN_MAX'
PSA_ALIGN_MEAN = 'ALIGN_MEAN'
PSA_ALIGN_STDDEV = 'ALIGN_STDDEV'
PSA_ALIGN_PERCENTAGE = 'ALIGN_PERCENTAGE'


@attr.s
class TimeSeriesList(object):
    """
    TimeSeriesList for Stackdriver.
    """

    alignmentPeriod = attr.ib(default=AP_CLOUD_MONITORING_AUTO, validator=in_([AP_CLOUD_MONITORING_AUTO,
                                                                               AP_GRAFANA_AUTO,
                                                                               AP_1M,
                                                                               AP_2M,
                                                                               AP_5M,
                                                                               AP_10M]))
    crossSeriesReducer = attr.ib(default='REDUCE_NONE', validator=in_([CSR_REDUCE_NONE,
                                                                       CSR_REDUCE_MEAN,
                                                                       CSR_REDUCE_MAX,
                                                                       CSR_REDUCE_MIN,
                                                                       CSR_REDUCE_SUM,
                                                                       CSR_REDUCE_STDDEV]))
    filters = attr.ib(default=attr.Factory(lambda: []), validator=instance_of(list))
    groupBys = attr.ib(default=attr.Factory(lambda: []), validator=instance_of(list))
    perSeriesAligner = attr.ib(default=PSA_ALIGN_MEAN, validator=in_([PSA_ALIGN_NONE,
                                                                      PSA_ALIGN_INTERPOLATE,
                                                                      PSA_ALIGN_NEXT_OLDER,
                                                                      PSA_ALIGN_MIN,
                                                                      PSA_ALIGN_MAX,
                                                                      PSA_ALIGN_MEAN,
                                                                      PSA_ALIGN_STDDEV,
                                                                      PSA_ALIGN_PERCENTAGE]))
    preprocessor = attr.ib(default='none', validator=in_(['none']))
    projectName = attr.ib(default='', validator=instance_of(str))
    view = attr.ib(default='FULL', validator=in_(['FULL']))

    def to_json_data(self):
        return {
            "alignmentPeriod": self.alignmentPeriod,
            "crossSeriesReducer": self.crossSeriesReducer,
            "filters": self.filters,
            "groupBys": self.groupBys,
            "perSeriesAligner": self.perSeriesAligner,
            "preprocessor": self.preprocessor,
            "projectName": self.projectName,
            "view": self.view,
        }


@attr.s
class StackdriverTarget(object):
    """
    Target for Stackdriver.
    """

    datasource = attr.ib(default='', validator=instance_of(str))
    refId = attr.ib(default='', validator=instance_of(str))
    aliasBy = attr.ib(default=None, validator=instance_of(Optional[str]))
    timeSeriesList = attr.ib(default=attr.Factory(TimeSeriesList), validator=instance_of(TimeSeriesList))
    metricType = attr.ib(default=None, validator=instance_of(Optional[str]))

    def to_json_data(self):
        return {
            'datasource': {
                'type': 'stackdriver',
                'uid': self.datasource,
            },
            'refId': self.refId,
            'aliasBy': self.aliasBy,
            'metricType': self.metricType,
            'queryType': 'timeSeriesList',
            'timeSeriesList': self.timeSeriesList.to_json_data()
        }
