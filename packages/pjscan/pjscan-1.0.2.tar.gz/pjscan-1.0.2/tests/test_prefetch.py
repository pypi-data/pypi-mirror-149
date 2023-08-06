import unittest, time, random

from pjscan.cache import BasePrefetchThread
from pjscan.const import *
from pjscan import AnalysisFramework as Neo4jEngine
from pjscan.graph_traversal import GlobalProgramDependencyGraphBackwardTraversal


class PdgBackwardPrefetchThread(BasePrefetchThread):
    def __init__(self, *args, **kwargs):
        self.drop_out = kwargs.get("drop_out", 0.5)
        assert 0.0 <= self.drop_out <= 1.0
        super(PdgBackwardPrefetchThread, self).__init__(*args, **kwargs)

    def prefetch(self, node):
        if random.randint(0, 100) * 0.01 >= self.drop_out:
            return
        if node[NODE_TYPE] not in AST_ROOT:
            return
        if self.cache_graph.get_pdg_inflow(node) is None:
            rels = self.graph.relationships.match(nodes=[None, node], r_type=DATA_FLOW_EDGE, ).all()
            self.cache_graph.add_pdg_inflow(node, rels)
        if self.cache_graph.get_pdg_outflow(node) is None:
            rels = self.graph.relationships.match(nodes=[node, None], r_type=DATA_FLOW_EDGE, ).all()
            self.cache_graph.add_pdg_outflow(node, rels)


class PrefetchTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PrefetchTest, self).__init__(*args, **kwargs)

    def test_prefetch_pdg_backward_prefetch(self):
        start_time = time.time()
        self.neo4j_engine: Neo4jEngine = Neo4jEngine.from_yaml('neo4j_default_config.yaml')
        file_name_node = self.neo4j_engine.get_fig_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        graph_traversal = GlobalProgramDependencyGraphBackwardTraversal(self.neo4j_engine)
        origin = [self.neo4j_engine.get_ast_root_node(i) for i in self.neo4j_engine.match(
            **{NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_CALL, })]
        print(f"The origin size is {origin.__len__()}")
        graph_traversal.origin = origin
        graph_traversal.run()
        end_time = time.time()
        # GeometryVisualizer.show_graph(graph_traversal.get_record())
        print(f"The process with cache is {round(end_time - start_time, 2)}")

        start_time = time.time()
        self.neo4j_engine: Neo4jEngine = Neo4jEngine.from_yaml('neo4j_default_config.yaml', prefetch_setting={
            "astThreadCount": 1,
            "ast_prefetch_thread_configure": {
                "new_connector": True
            },
            "pdgThreadCount": 1,
            "pdg_prefetch_thread_configure": {
                "class_name": PdgBackwardPrefetchThread,
                "drop_out": 0.25
            },
        })
        file_name_node = self.neo4j_engine.get_fig_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        graph_traversal = GlobalProgramDependencyGraphBackwardTraversal(self.neo4j_engine)
        origin = [self.neo4j_engine.get_ast_root_node(i) for i in self.neo4j_engine.match(
            **{NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_CALL, })]
        print(f"The origin size is {origin.__len__()}")
        graph_traversal.origin = origin
        graph_traversal.run()
        end_time = time.time()
        # GeometryVisualizer.show_graph(graph_traversal.get_record())
        print(f"The process with cache/pdg*1,ast*1 is {round(end_time - start_time, 2)}")


if __name__ == '__main__':
    unittest.main()
