"""humioQuery: options.annotation.humioQuery,
humioRepository: options.annotation.humioRepository,
refId: options.annotation.refId"""
import attr


@attr.s
class HumioTarget(object):
    """
    Generates Humio target JSON structure.

    Link to Humio Grafana plugin https://grafana.com/grafana/plugins/humio-datasource/

    Humio docs on query language https://docs.humio.com/reference/language-syntax/

    :param humioQuery: Query that will be executed on Humio
    :param humioRepository: Repositry to execute query on.
    :param refId: target reference id
    """

    humioQuery = attr.ib(default="")
    humioRepository = attr.ib(default="")
    refId = attr.ib(default="")

    def to_json_data(self):

        return {
            "humioQuery": self.humioQuery,
            "humioRepository": self.humioRepository,
            "refId": self.refId
        }
