import grafanalib.core as G
import grafanalib.azuredataexplorer as A
from grafanalib import _gen
from io import StringIO


def test_serialization_azuredataexplorer_metrics_target():
    """Serializing a graph doesn't explode."""
    graph = G.Graph(
        title="Azure Data Explorer graph",
        dataSource="default",
        targets=[
            A.AzureDataExplorerTarget()
        ],
    )
    stream = StringIO()
    _gen.write_dashboard(graph, stream)
    assert stream.getvalue() != ''
