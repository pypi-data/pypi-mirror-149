import logging
import unittest
from pjscan import AnalysisFramework as Neo4jEngine
from pjscan.const import *
from typing import Union, Dict, Set, List


class FigTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(FigTest, self).__init__(*args, **kwargs)
        self.neo4j_engine: Neo4jEngine = Neo4jEngine.from_yaml(
            './neo4j_default_config.yaml')  # the config should be edited by your self

    def test_const_inclusion_1(self):
        """

        Returns
        -------

        """
        file_node = self.neo4j_engine.get_fig_file_name_node(
            "GraphTraversalTestCase/1da9d6afc4f6ca045ff5aabc4640b9d9c343a3be/admin/user_list_backend.php"
        )
        f_node = self.neo4j_engine.get_fig_filesystem_node(file_node)
        include_dst = self.neo4j_engine.find_fig_include_dst(f_node)[0]
        self.assertEqual(include_dst[NODE_NAME], 'common.inc.php')

    def test_const_inclusion_2(self):
        """

        Returns
        -------

        """
        file_node = self.neo4j_engine.get_fig_file_name_node(
            "GraphTraversalTestCase/1da9d6afc4f6ca045ff5aabc4640b9d9c343a3be/include/common.inc.php"
        )
        f_node = self.neo4j_engine.get_fig_filesystem_node(file_node)
        include_dst = self.neo4j_engine.find_fig_include_src(f_node)[0]
        self.assertEqual(include_dst[NODE_NAME], 'user_list_backend.php')


if __name__ == '__main__':
    unittest.main()
