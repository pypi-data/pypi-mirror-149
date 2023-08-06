from pjscan.graph_traversal import *
from pjscan.const import *
from pjscan.cache.prefetch_task import *
from pjscan import *
import unittest, random
import time


class PdgBackwardPrefetchTask(AbstractPrefetchTask):
    def __init__(self, *args, **kwargs):
        super(PdgBackwardPrefetchTask, self).__init__(*args, **kwargs)
        self.drop_out = kwargs.get("drop_out", 50)
        self.node = kwargs.get("node", None)

    def do_task(self):
        if random.randint(0, 100) * 0.01 >= self.drop_out:
            return
        if self.node[NODE_TYPE] not in AST_ROOT:
            return
        if self.cache_graph.get_pdg_inflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[None, self.node], r_type=DATA_FLOW_EDGE, ).all()
            self.cache_graph.add_pdg_inflow(self.node, rels)
        if self.cache_graph.get_pdg_outflow(self.node) is None:
            rels = self.graph.relationships.match(nodes=[self.node, None], r_type=DATA_FLOW_EDGE, ).all()
            self.cache_graph.add_pdg_outflow(self.node, rels)


class GlobalProgramDependencyGraphBackwardTraversal(BaseGraphTraversal):
    """The PDG Backward Traversal Interface with Interprocedural Analysis

    """

    def __init__(self, *args, **kwargs):
        """

        Parameters
        ----------
        args
        kwargs
        """
        super(GlobalProgramDependencyGraphBackwardTraversal, self).__init__(*args, **{})
        self.func_depth = {}
        self.max_func_depth = kwargs.get('max_func_depth', 3)
        self.sanitizer_param_list = {"analysis_framework": self.analysis_framework}
        self.useCache = kwargs.get('cache', False)
        print(self.useCache)
        if self.useCache:
            self.cache_graph = self.analysis_framework.cache
            self.thread_pool = PrefetchPool(self.analysis_framework.neo4j_graph, 2)

        # here list some storage

    def traversal(self, node, *args, **kwargs):
        # print(node)
        # cancel param
        if node[NODE_FUNCID] not in self.func_depth:
            self.func_depth[node[NODE_FUNCID]] = 0
        if self.func_depth[node[NODE_FUNCID]] >= self.max_func_depth:
            return []

        # local pdg
        result = []
        define_nodes = self.analysis_framework.find_pdg_def_nodes(node)
        result.extend(define_nodes)

        # global pdg
        if node[NODE_TYPE] != TYPE_ASSIGN:
            return result
        call_nodes = self.analysis_framework.filter_ast_child_nodes(
                self.analysis_framework.get_ast_ith_child_node(node, 1),
                node_type_filter=[TYPE_CALL, TYPE_METHOD_CALL, TYPE_STATIC_CALL]
        )
        for call_node in call_nodes:
            callable_node = self.analysis_framework.find_cg_decl_nodes(call_node)
            if callable_node:
                callable_node = callable_node[0]
                # traverse from return .
                return_nodes = self.analysis_framework.ast_step.find_function_return_expr(callable_node)
                for return_node in return_nodes:
                    if return_node[NODE_FUNCID] not in self.func_depth:
                        self.func_depth[return_node[NODE_FUNCID]] = self.func_depth[node[NODE_FUNCID]] + 1
                result.extend(return_nodes)
        if self.useCache:
            for node in result:
                prefetch_setting = {"drop_out": 25, "node": node}
                pdg_task = PdgBackwardPrefetchTask(cache_graph=self.cache_graph, **prefetch_setting)
                self.thread_pool.put_task_in_queue(pdg_task)
        return result


class PrefetchTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PrefetchTest, self).__init__(*args, **kwargs)

    def test_prefetch_pdg_backward_prefetch(self):
        start_time = time.time()
        self.neo4j_engine: AnalysisFramework = AnalysisFramework.from_yaml(
            '../examples/findSQLVul/neo4j_default_config.yaml')
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
        self.neo4j_engine: AnalysisFramework = AnalysisFramework.from_yaml(
            '../examples/findSQLVul/neo4j_default_config.yaml')
        file_name_node = self.neo4j_engine.get_fig_file_name_node(
                "local_flow_1/admin/user_list_backend.php")
        graph_traversal = GlobalProgramDependencyGraphBackwardTraversal(self.neo4j_engine, **{'cache': True})
        origin = [self.neo4j_engine.get_ast_root_node(i) for i in self.neo4j_engine.match(
                **{NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_CALL, })]
        print(f"The origin size is {origin.__len__()}")
        graph_traversal.origin = origin
        graph_traversal.run()
        end_time = time.time()
        # GeometryVisualizer.show_graph(graph_traversal.get_record())
        print(f"The process with cache/pdg*1,ast*1 is {round(end_time - start_time, 2)}")


if __name__ == '__main__':    unittest.main()
