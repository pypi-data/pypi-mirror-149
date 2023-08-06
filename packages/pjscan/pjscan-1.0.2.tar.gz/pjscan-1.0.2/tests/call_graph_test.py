import logging
import unittest

import networkx as nx

from pjscan.graph_traversal import ProgramDependencyGraphBackwardTraversal, \
    ControlGraphForwardTraversal, BaseGraphTraversal
from pjscan.graph_traversal_recorder import GraphTraversalRecorder, GraphTraversalStraightRecorder
from pjscan import AnalysisFramework as Neo4jEngine
from pjscan.const import *
from pjscan.helper import GeometryVisualizer

logger = logging.getLogger(__name__)


class CallGraphTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CallGraphTest, self).__init__(*args, **kwargs)
        self.neo4j_engine: Neo4jEngine = Neo4jEngine.from_yaml(
            './neo4j_default_config.yaml')  # the config should be edited by your self

    def test_call_graph_case1(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest2/trait.php"
        )[NODE_FILEID]
        loc_20_root = self.neo4j_engine.match_first(
            **{
                NODE_LINENO: 20, NODE_FILEID: file_id,
            }
        )
        # loc_19_root = self.neo4j_engine.get_ast_root_node(loc_19_root)
        for x in self.neo4j_engine.match_relationship({loc_20_root}):
            print(x)
