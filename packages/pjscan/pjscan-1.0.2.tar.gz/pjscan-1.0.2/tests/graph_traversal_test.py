import logging
import unittest

import networkx as nx

from pjscan.graph_traversal import ProgramDependencyGraphBackwardTraversal, \
    ControlGraphForwardTraversal, BaseGraphTraversal, GlobalProgramDependencyGraphBackwardTraversal, \
    GlobalControlGraphForwardTraversal
from pjscan.graph_traversal_recorder import GraphTraversalRecorder
from pjscan import AnalysisFramework as Neo4jEngine
from pjscan.const import *
from pjscan.helper import GeometryVisualizer

logger = logging.getLogger(__name__)


class ControlGraphForwardTrueBranchTraversal(BaseGraphTraversal):
    def __init__(self, *args, **kwargs):
        super(ControlGraphForwardTrueBranchTraversal, self).__init__(*args, **kwargs)
        self.loop_structure_instance = {}

    def __switch(self, next_node):
        if next_node in self.loop_structure_instance.keys():
            return self.__switch(self.loop_structure_instance[next_node])
        else:
            return next_node

    def traversal(self, node, *args, **kwargs):
        parent_node = self.analysis_framework.get_ast_parent_node(node)

        # If only true branch
        if parent_node[NODE_TYPE] == TYPE_IF_ELEM and node[NODE_CHILDNUM] == 0:
            logger.info(f"detect if node on line [{parent_node}]")
            x = self.analysis_framework.find_cfg_successors(node)
            return [x[0]]

        # We can cut the loop structure's return node.
        next_nodes = self.analysis_framework.find_cfg_successors(node)
        result = []
        for next_node in next_nodes:
            if parent_node[NODE_TYPE] == TYPE_FOR and \
                    self.analysis_framework.get_ast_ith_child_node(parent_node, 2) \
                    not in self.loop_structure_instance.keys():
                self.loop_structure_instance[
                    self.analysis_framework.get_ast_ith_child_node(parent_node, 2)
                ] = self.analysis_framework.find_cfg_successors(
                    self.analysis_framework.get_ast_ith_child_node(parent_node, 1)
                )[1]
            elif parent_node[NODE_TYPE] == TYPE_WHILE:
                self.loop_structure_instance[node] = self.analysis_framework.find_cfg_successors(node)[1]
            elif node[NODE_TYPE] == TYPE_FOREACH:
                self.loop_structure_instance[node] = self.analysis_framework.find_cfg_successors(node)[1]
            if next_node[NODE_INDEX] < node[NODE_INDEX]:
                # This must be loop structure instance
                if next_node in self.loop_structure_instance.keys():
                    next_node = self.__switch(next_node)
                else:
                    print("Problem not solved")
                    # return False
            result.append(next_node)
        return result


class GraphTraversalTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(GraphTraversalTest, self).__init__(*args, **kwargs)
        self.analysis_framework: Neo4jEngine = Neo4jEngine.from_yaml(
            './neo4j_default_config.yaml')  # the config should be edited by your self

    def test_traversal_local_pdg_backward(self):
        file_name_node = self.analysis_framework.get_fig_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        # to pass origin , 3 methods are recommand:
        # 1st method ,use function chall chains (first statement is analysis_framework
        origin_funcs = [
            lambda _analysis_framework: [_analysis_framework.match_first(**{
                NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ECHO, NODE_LINENO: 243,
            })]
        ]
        # 2ed method ,use function chall chains (first statement is analysis_framework
        # origin_nodes = [self.analysis_framework.match_first(**{
        #     NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ECHO, NODE_LINENO: 243,
        # })]
        graph_traversal = ProgramDependencyGraphBackwardTraversal(self.analysis_framework, origin=origin_funcs)
        # 3rd method , pass origin node list
        # graph_traversal.origin = [self.analysis_framework.match_first(**{
        #     NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ECHO, NODE_LINENO: 243, })]
        graph_traversal.run()
        # GeometryVisualizer.show_graph(graph_traversal.get_record())
        self.assertTrue(1)

    def test_traversal_local_cfg_forward_case1(self):
        file_name_node = self.analysis_framework.fig_step.get_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        graph_traversal = ControlGraphForwardTraversal(self.analysis_framework)
        # set origin
        origin_node = self.analysis_framework.basic_step.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ASSIGN, NODE_LINENO: 175,
        })
        graph_traversal.origin = [origin_node]
        # set terminal
        terminal_node = self.analysis_framework.basic_step.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_BINARY_OP, NODE_LINENO: 212,
        })
        graph_traversal.terminal = [lambda x, **kwargs: x[NODE_INDEX] == terminal_node[NODE_INDEX]]
        # set sanitizer
        graph_traversal.sanitizer = [lambda x, **kwargs: x[NODE_INDEX] > terminal_node[NODE_INDEX]]
        # run instance
        graph_traversal.run()
        # get result and visualize
        GeometryVisualizer.show_graph(graph_traversal.get_record())
        g = graph_traversal.get_record()
        res = []
        for x in nx.all_simple_paths(g, origin_node.identity, terminal_node.identity):
            r = list(map(lambda z: g.nodes.get(z)[NODE_LINENO], x))
            # print(r)
            res.append(r)
        for manual_result in [
            [175, 177, 179, 181, 182, 182, 184, 186, 208, 212],
            [175, 177, 179, 181, 182, 182, 184, 188, 190, 208, 212],
            [175, 177, 179, 181, 182, 182, 184, 188, 192, 208, 212],
            [175, 177, 179, 181, 182, 182, 184, 188, 192, 195, 196, 198, 204, 208, 212],
            [175, 177, 179, 181, 182, 182, 184, 188, 192, 195, 196, 198, 200, 204, 208, 212],
            [175, 177, 179, 181, 182, 182, 184, 188, 192, 195, 196, 204, 208, 212],
            [175, 177, 179, 181, 182, 182, 208, 212],
            [175, 177, 212],
        ]:
            self.assertIn(manual_result, res)
        self.assertEqual(graph_traversal.get_result()[0], terminal_node)

    def test_traversal_local_cfg_forward_case2(self):
        """
        This is an example where we must traverse the IF-TRUE branch

        Returns
        -------

        """
        file_name_node = self.analysis_framework.get_fig_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        graph_traversal = ControlGraphForwardTrueBranchTraversal(self.analysis_framework)
        origin_node = self.analysis_framework.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ASSIGN, NODE_LINENO: 175,
        })
        graph_traversal.origin = [origin_node]
        terminal_node = self.analysis_framework.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_BINARY_OP, NODE_LINENO: 212,
        })
        graph_traversal.sanitizer = [lambda x, **kwargs: x[NODE_INDEX] > terminal_node[NODE_INDEX]]
        graph_traversal.terminal = [lambda x, **kwargs: x[NODE_INDEX] == terminal_node[NODE_INDEX]]

        graph_traversal.run()

        GeometryVisualizer.show_graph(graph_traversal.get_record())

        g = graph_traversal.get_record()
        res = []

        for x in nx.all_simple_paths(g, origin_node.identity, terminal_node.identity):
            r = list(map(lambda z: g.nodes.get(z)[NODE_LINENO], x))
            # print(r)
            res.append(r)
        for manual_result in [
            [175, 177, 179, 181, 182, 182, 184, 186, 208, 212],
            [175, 177, 179, 181, 182, 182, 208, 212],
            [175, 177, 212],
        ]:
            self.assertIn(manual_result, res)
        self.assertEqual(graph_traversal.get_result()[0], terminal_node)

    def test_traversal_global_pdg_case(self):
        """

        Returns
        -------

        """
        file_name_node = self.analysis_framework.get_fig_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        graph_traversal = GlobalProgramDependencyGraphBackwardTraversal(self.analysis_framework)
        terminal_node = self.analysis_framework.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ASSIGN, NODE_LINENO: 156,
        })
        origin_node = self.analysis_framework.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ASSIGN, NODE_LINENO: 162,
        })
        graph_traversal.origin = [origin_node]
        graph_traversal.sanitizer = [lambda x, **kwargs: x[NODE_INDEX] < terminal_node[NODE_INDEX] \
            if x[NODE_FUNCID] == terminal_node[NODE_FUNCID] else False]
        graph_traversal.terminal = [lambda x, **kwargs: x[NODE_INDEX] == terminal_node[NODE_INDEX]]
        graph_traversal.run()
        GeometryVisualizer.show_graph(graph_traversal.get_record())

    def test_traversal_global_cfg_case(self):
        file_name_node = self.analysis_framework.get_fig_file_name_node(
            "local_flow_1/admin/user_list_backend.php")
        graph_traversal = GlobalControlGraphForwardTraversal(self.analysis_framework)
        origin_node = self.analysis_framework.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ASSIGN, NODE_LINENO: 156,
        })
        terminal_node = self.analysis_framework.match_first(**{
            NODE_FILEID: file_name_node[NODE_FILEID], NODE_TYPE: TYPE_ASSIGN, NODE_LINENO: 162,
        })
        graph_traversal.origin = [origin_node]
        graph_traversal.sanitizer = [lambda x, **kwargs: x[NODE_INDEX] > terminal_node[NODE_INDEX] \
            if x[NODE_FUNCID] == terminal_node[NODE_FUNCID] else False]
        graph_traversal.terminal = [lambda x, **kwargs: x[NODE_INDEX] == terminal_node[NODE_INDEX]]
        graph_traversal.run()
        GeometryVisualizer.show_graph(graph_traversal.get_record())


if __name__ == '__main__':
    unittest.main()
