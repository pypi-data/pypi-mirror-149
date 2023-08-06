import unittest
from pjscan import AnalysisFramework as Neo4jEngine
from pjscan.const import *
from typing import Union, Dict, Set, List
from pjscan.neo4j_defauilt_config import NEO4J_DEFAULT_CONFIG


class CHGTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(CHGTest, self).__init__(*args, **kwargs)
        self.neo4j_engine: Neo4jEngine = Neo4jEngine(NEO4J_DEFAULT_CONFIG)

    def test_case2(self):
        """
        tests/resource/NormalCase/CHG/classExtendsTest2/trait.php
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest2/trait.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 2, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        self.assertEqual(trait_b['flags'], [CLASS_TRAIT])
        class_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 15, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_c, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_a)
        trait_rel = self.neo4j_engine.match_relationship([class_c, None], r_type=TRAIT_EDGE).first()
        self.assertEqual(trait_rel.end_node, trait_b)
        return True
    def test_case3(self):
        '''
            这里有个问题
            会把extend语句解析成implement
        '''
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest3.php"
        )[NODE_FILEID]
        interface_a_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 2, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        interface_b_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 12, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_d = self.neo4j_engine.match(
            **{
                NODE_LINENO: 17, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        r1 = self.neo4j_engine.match_relationship([class_d, class_c], r_type=IMPLEMENT_EDGE).first()
        self.assertEqual(
            r1.end_node, class_c
        )
        r2 = self.neo4j_engine.match_relationship([class_c, None], r_type=IMPLEMENT_EDGE).all()[1]
        self.assertEqual(
            r2.end_node, interface_a_node
        )
        r3 = self.neo4j_engine.match_relationship([class_c, None], r_type=IMPLEMENT_EDGE).first()
        self.assertEqual(
            r3.end_node, interface_b_node
        )
        return True
    def test_case4(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest4.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 13, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        interface_b_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 29, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_c, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_a)
        implement_rel = self.neo4j_engine.match_relationship([class_c, None], r_type=IMPLEMENT_EDGE).first()
        self.assertEqual(implement_rel.end_node, interface_b_node)
    def test_case5(self):
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest5/src/GraduateStudent.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest5/src/User.php"
        )[NODE_FILEID]
        file3_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest5/src/TeacherInterface.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 6, NODE_FILEID: file1_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file2_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file3_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)
        implement_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=IMPLEMENT_EDGE).first()
        self.assertEqual(implement_rel.end_node, class_c)
        return True
    def test_case6(self):
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest6/GraduateStudent.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest6/User2.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file1_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 10, NODE_FILEID: file2_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)
    def test_case7(self):
        """
        tests/resource/NormalCase/CHG/classExtendsTest7/classExtendsTest7.php
        TestConnection<AST_CLASS> -> Connection<AST_CLASS>
        class TestConnection extends Connection
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest7.php"
        )[NODE_FILEID]
        # (_2223:AST {endlineno: 57, fileid: 4038, flags: ['TOPLEVEL_FILE'], id: 4039, lineno: 1,
        #  name: '../enhanced-phpjoern-framework/tests/resource//NormalCase/CHG/classExtendsTest7/classExtendsTest7.php', type: 'AST_TOPLEVEL'})
        method_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 43, NODE_FILEID: file_id
            }
        ).first()

        parent_class_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 18, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        r = self.neo4j_engine.match_relationship([method_node, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(
            r.end_node, parent_class_node
        )
        return True
    def test_case8(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest8.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 45, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 19, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)

    def test_case9(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest9.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 61, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 27, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 19, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)
        implement_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=IMPLEMENT_EDGE).first()
        self.assertEqual(implement_rel.end_node, class_c)
    def test_case12(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest12.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 11, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        interface_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_d = self.neo4j_engine.match(
            **{
                NODE_LINENO: 9, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)
        implement_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=IMPLEMENT_EDGE).first()
        self.assertEqual(implement_rel.end_node, interface_c)
        trait_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=TRAIT_EDGE).first()
        self.assertEqual(trait_rel.end_node, trait_d)
    def test_case13(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest13.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 15, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)
    def test_case14(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "SingleTrait.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 20, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=TRAIT_EDGE).first()
        self.assertEqual(trait_rel.end_node, trait_b)
    def test_case15(self):
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "MultiTrait.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 36, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 21, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=TRAIT_EDGE).all()
        self.assertEqual(trait_rel[0].end_node,  trait_c)
        self.assertEqual(trait_rel[1].end_node, trait_b)
    def test_case16(self):
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest16/system/Mobiles.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest16/system/traits/Faceable.php"
        )[NODE_FILEID]
        file3_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest16/system/traits/Messageable.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file1_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 6, NODE_FILEID: file2_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_c = self.neo4j_engine.match(
            **{
                NODE_LINENO: 6, NODE_FILEID: file3_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        trait_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=TRAIT_EDGE).all()
        self.assertEqual(trait_rel[0].end_node, trait_c)
        self.assertEqual(trait_rel[1].end_node, trait_b)
    def  test_case19(self):
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest19/Action/Base.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "classExtendsTest19/Core/Base.php"
        )[NODE_FILEID]
        class_a = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file1_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        class_b = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file2_id, NODE_TYPE: TYPE_CLASS
            }
        ).first()
        extend_rel = self.neo4j_engine.match_relationship([class_a, None], r_type=EXTENDS_EDGE).first()
        self.assertEqual(extend_rel.end_node, class_b)


if __name__ == '__main__':
    unittest.main()
