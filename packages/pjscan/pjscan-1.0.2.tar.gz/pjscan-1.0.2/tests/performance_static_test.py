from pjscan import AnalysisFramework as Neo4jEngine
import unittest
from pjscan.neo4j_defauilt_config import NEO4J_DEFAULT_CONFIG

try:
    from tests.util import StatisticContextManager, join_and_static
except ImportError as e:
    from util import StatisticContextManager, join_and_static

from pjscan.const import *
# from tqdm import tqdm
# from cpg2code import Cpg2CodeFactory


class PerformanceStaticTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(PerformanceStaticTest, self).__init__(*args, **kwargs)
        self.neo4j_engine: Neo4jEngine = None

    def code2cpg_debugger(self, node_id):
        node = self.neo4j_engine.get_ast_root_node(self.neo4j_engine.get_node_itself(node_id))
        print(f"DEBUGGING NODE in file {self.neo4j_engine.get_fig_belong_file(node)}#L{node[NODE_LINENO]}")
        try:
            print(Cpg2CodeFactory.extract_code(self.neo4j_engine, node))
        except Exception as e:
            print(e)

    def _test_missing_single(self, configure, builtin_function_call=0, builtin_class=0):
        # I need this script to debug
        NEO4J_DEFAULT_CONFIG['NEO4J_PORT'] = configure
        self.neo4j_engine = Neo4jEngine.from_dict(NEO4J_DEFAULT_CONFIG)

        # CG statistics (function call)
        # function_call_statement = set(i for i, in
        #                               self.neo4j_engine.run(
        #                                   f'MATCH (A:AST) WHERE A.type = "{TYPE_CALL}" return A.id'
        #                               ))
        # function_call_edge = set(i for i, in
        #                          self.neo4j_engine.run(
        #                              f'MATCH (A:AST)-[r:{CALLS_EDGE}]->(B:AST) WHERE A.type = "{TYPE_CALL}" return A.id'
        #                          ))
        # print((function_call_statement - function_call_edge).__len__())
        static_call_statement = set(i for i, in
                                    self.neo4j_engine.run(
                                        f'MATCH (A:AST) WHERE A.type = "{TYPE_STATIC_CALL}" return A.id'
                                    ))
        static_call_edge = set(i for i, in
                               self.neo4j_engine.run(
                                   f'MATCH (A:AST)-[r:{CALLS_EDGE}]->(B:AST) WHERE A.type = "{TYPE_STATIC_CALL}" return A.id'
                               ))
        print((static_call_statement - static_call_edge).__len__())
        print("[*] DEBUGGING static_call part")
        for index, node_id in enumerate(static_call_statement - static_call_edge):
            if index >= 300: break
            self.code2cpg_debugger(node_id)

        method_call_statement = set(i for i, in
                                    self.neo4j_engine.run(
                                        f'MATCH (A:AST) WHERE A.type = "{TYPE_METHOD_CALL}" return A.id'
                                    ))
        method_call_edge = set(i for i, in
                               self.neo4j_engine.run(
                                   f'MATCH (A:AST)-[r:{CALLS_EDGE}]->(B:AST) WHERE A.type = "{TYPE_METHOD_CALL}" return A.id'
                               ))
        print((method_call_statement - method_call_edge).__len__())
        print("[*] DEBUGGING method_call part")
        for index, node_id in enumerate(method_call_statement - method_call_edge):
            if index >= 300: break
            self.code2cpg_debugger(node_id)
        return {}

    def _test_performance_single(self, configure, builtin_function_call=0, builtin_class=0):
        NEO4J_DEFAULT_CONFIG['NEO4J_PORT'] = configure
        self.neo4j_engine = Neo4jEngine.from_dict(NEO4J_DEFAULT_CONFIG)
        # core_file_cnt statistics
        core_file_cnt = self.neo4j_engine.run_and_fetch_one(
            f"MATCH (A:{LABEL_FILESYSTEM}) where A.type=\"{TYPE_FILE}\" RETURN count(A)")[0]

        # static node and relationships
        node_number = self.neo4j_engine.run_and_fetch_one("MATCH (A) return count(A)")[0]
        edge_number = self.neo4j_engine.run_and_fetch_one("MATCH (A)-[r]-(B) return count(r)")[0]
        # FIG statistics
        include_statement_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST) WHERE A.type="{TYPE_INCLUDE_OR_EVAL}" and'
                f' ("{FLAG_EXEC_INCLUDE}" in A.flags or "{FLAG_EXEC_INCLUDE_ONCE}" in A.flags or'
                f'  "{FLAG_EXEC_REQUIRE}" in A.flags or "{FLAG_EXEC_REQUIRE_ONCE}" in A.flags ) return count(A)')[0]
        include_edge_number = self.neo4j_engine.run_and_fetch_one(
            f"MATCH (A)-[r:{INCLUDE_EDGE}]->(B) return count(r)")[0]
        # CHG statistics
        extend_or_implement_statement_number = 0
        extend_or_implement_edge_number = 0
        trait_statement_number = 0
        trait_edge_number = 0
        try:
            for node in self.neo4j_engine.match(LABEL_AST, **{NODE_TYPE: TYPE_CLASS}):
                # note : because of VPN , this script is very slow , I must move it to remote
                # print(node)
                extends_list = self.neo4j_engine.get_ast_ith_child_node(node, 2)
                extend_or_implement_statement_number += self.neo4j_engine.find_ast_child_nodes(extends_list).__len__()
                implements_list = self.neo4j_engine.get_ast_ith_child_node(node, 3)
                extend_or_implement_statement_number += self.neo4j_engine.find_ast_child_nodes(
                    implements_list).__len__()
        except Exception as e:
            print(e)
            extend_or_implement_statement_number = 0xffffff
            trait_statement_number = 0xffffff

        extend_or_implement_edge_number = \
            self.neo4j_engine.run_and_fetch_one(f"MATCH (A:AST)-[r:{EXTENDS_EDGE}]->(B:AST) return count(r)")[0] + \
            self.neo4j_engine.run_and_fetch_one(f"MATCH (A:AST)-[r:{IMPLEMENT_EDGE}]->(B:AST) return count(r)")[0]

        for node in self.neo4j_engine.match(LABEL_AST, **{NODE_TYPE: TYPE_USE_TRAIT}):
            traits_list = self.neo4j_engine.get_ast_child_node(node)
            trait_statement_number += self.neo4j_engine.find_ast_child_nodes(traits_list).__len__()

        trait_edge_number = self.neo4j_engine.run_and_fetch_one(
            f"MATCH (A)-[r:{TRAIT_EDGE}]->(B) return count(r)")[0]

        # CG statistics (function call)
        function_call_statement_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST) WHERE A.type = "{TYPE_CALL}" return count(A)'
            )[0]
        function_call_edge_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST)-[r:{CALLS_EDGE}]->(B:AST) WHERE A.type = "{TYPE_CALL}" return count(r)'
            )[0]
        # CG statistics (static call)
        static_call_statement_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST) WHERE A.type = "{TYPE_STATIC_CALL}" return count(A)'
            )[0]
        static_call_edge_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST)-[r:{CALLS_EDGE}]->(B:AST) WHERE A.type = "{TYPE_STATIC_CALL}" return count(r)'
            )[0]
        # CG statistics (construction call)

        # CG statistics (method call)
        method_call_statement_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST) WHERE A.type = "{TYPE_METHOD_CALL}" return count(A)'
            )[0]
        method_call_edge_number = \
            self.neo4j_engine.run_and_fetch_one(
                f'MATCH (A:AST)-[r:{CALLS_EDGE}]->(B:AST) WHERE A.type = "{TYPE_METHOD_CALL}" return count(r)'
            )[0]
        return {
            'file': core_file_cnt,
            "node": node_number,
            "edge": edge_number,
            "include statement": join_and_static(include_edge_number, include_statement_number),
            "extended/implement statement":
                join_and_static(extend_or_implement_edge_number + builtin_class, extend_or_implement_statement_number),
            "use_trait statement":
                join_and_static(trait_edge_number, trait_statement_number),
            "function call statement":
                join_and_static(function_call_edge_number + builtin_function_call, function_call_statement_number),
            "static call statement":
                join_and_static(static_call_edge_number, static_call_statement_number),
            "method call statement":
                join_and_static(method_call_edge_number, method_call_statement_number),
        }

    def test_missing(self):
        """
        Here is some useful scripts


        """

        input_matrix = [
            # ["WordPress-5.7.1_origin", "raw", 16216 + 1, 0, 0],
            # ["october-2.0.10_origin", "raw", 16222 + 1, 0, 0],
            # ["roundcubemail-1.4.11_origin", "raw", 16230 + 1, 0, 0],
            # ["core-10.7.0_origin", "raw", 16220 + 1, 0, 0],
            # ["kanboard-1.2.19_origin", "raw", 16218 + 1, 0, 0],
            # ["phpmyadmin-RELEASE_5_1_0_origin", "raw", 16226 + 1, 0, 0],
            # ["PrestaShop-1.7.7.4_origin", "raw", 16224 + 1, 0, 0],
            # ["MISP-2.4.142_origin", "raw", 16228 + 1, 0, 0],
            # ["WordPress-5.7.1", "new", 16101, 23866, 27],  # 29.58    202.94    16.23
            # ["October", "new", 16103, 33390, 715],  # 56.73    258.85    21.66
            # ["roundcubemail", "new", 16105, 8689, 6],  # 22.85    36.52    14.69
            # ["core-10.7.0", "new", 16107, 41275, 473],  # 160.04    1607.97    40.02
            # ["kanboard-1.2.19", "new", 16109, 0, 0],  # 12.93    16.31    14.78
            # ["phpmyadmin-RELEASE_5_1_0", "new", 16111, 32774, 301],  # 152.61    422.93    39.33
            # ["PrestaShop-1.7.7.4", "new", 16113, 82728, 743],  # 238.8    4134.79    50.28
            # ["MISP-2.4.142", "new", 16115, 5458, 2],  # 11.47    8.83    12.48
            # ["WordPress-5.7.1", "ast-30", 16201, 0, 0],
            # ["kanboard-1.2.19", "ast-30", 16202 + 1, 0, 0],
            # ["core-10.7.0", "ast-30", 16204 + 1, 0, 0],
            # ["october-2.0.10", "ast-30", 16206 + 1, 0, 0],
            # ["PrestaShop-1.7.7.4", "ast-30", 16208 + 1, 0, 0],
            # ["phpmyadmin-RELEASE_5_1_0", "ast-30", 16210 + 1, 0, 0],
            # ["MISP-2.4.142", "ast-30", 16212 + 1, 0, 0],
            # ["roundcubemail-1.4.11", "ast-30", 16214 + 1, 0, 0],
        ]
        with StatisticContextManager(input_matrix) as statistician:
            for application_name, database_mode, neo4j_port, builtin_function_call, builtin_class in input_matrix:
                r = {
                    "application_name": application_name,
                    "database_mode": database_mode,
                }
                x = self._test_missing_single(neo4j_port, builtin_function_call, builtin_class)
                r.update(**x)
                statistician.push_result(r)
            statistician.store_result('result.tsv')

    def test_performance(self):
        """
        This is a script used to test performance.

        Returns
        -------

        """
        input_matrix = [
            # ["WordPress-5.7.1_origin", "raw", 16216 + 1, 0, 0],
            # ["october-2.0.10_origin", "raw", 16222 + 1, 0, 0],
            # ["roundcubemail-1.4.11_origin", "raw", 16230 + 1, 0, 0],
            # ["core-10.7.0_origin", "raw", 16220 + 1, 0, 0],
            # ["kanboard-1.2.19_origin", "raw", 16218 + 1, 0, 0],
            # ["phpmyadmin-RELEASE_5_1_0_origin", "raw", 16226 + 1, 0, 0],
            # ["PrestaShop-1.7.7.4_origin", "raw", 16224 + 1, 0, 0],
            # ["MISP-2.4.142_origin", "raw", 16228 + 1, 0, 0],
            # ["WordPress-5.7.1", "new", 16101, 0, 0],  # 29.58    202.94    16.23
            # ["October", "new", 16103, 0, 0],  # 56.73    258.85    21.66
            # ["roundcubemail", "new", 16105, 0, 0],  # 22.85    36.52    14.69
            # ["core-10.7.0", "new", 16107, 0, 0],  # 160.04    1607.97    40.02
            # ["kanboard-1.2.19", "new", 16109, 0, 0],  # 12.93    16.31    14.78
            # ["phpmyadmin-RELEASE_5_1_0", "new", 16111, 0, 0],  # 152.61    422.93    39.33
            ["PrestaShop-1.7.7.4", "new", 16113, 0, 0],  # 238.8    4134.79    50.28
            # ["MISP-2.4.142", "new", 16115, 0, 0],  # 11.47    8.83    12.48
            # ["WordPress-5.7.1", "ast-30", 16201, 0, 0],
            # ["kanboard-1.2.19", "ast-30", 16202 + 1, 0, 0],
            # ["core-10.7.0", "ast-30", 16204 + 1, 0, 0],
            # ["october-2.0.10", "ast-30", 16206 + 1, 0, 0],
            # ["PrestaShop-1.7.7.4", "ast-30", 16208 + 1, 0, 0],
            # ["phpmyadmin-RELEASE_5_1_0", "ast-30", 16210 + 1, 0, 0],
            # ["MISP-2.4.142", "ast-30", 16212 + 1, 0, 0],
            # ["roundcubemail-1.4.11", "ast-30", 16214 + 1, 0, 0],
        ]  # name
        with StatisticContextManager(input_matrix) as statistician:
            for application_name, database_mode, neo4j_port, builtin_function_call, builtin_class in input_matrix:
                r = {
                    "application_name": application_name,
                    "database_mode": database_mode,
                }
                x = self._test_performance_single(neo4j_port, builtin_function_call, builtin_class)
                r.update(**x)
                statistician.push_result(r)
            # print(statistician.pop_result())
            statistician.store_result('result.tsv')
