import logging
import unittest
from pjscan import AnalysisFramework as Neo4jEngine
from pjscan.const import *
from typing import Union, Dict, Set, List


class NewFeatureTest(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super(NewFeatureTest, self).__init__(*args, **kwargs)
        self.neo4j_engine: Neo4jEngine = Neo4jEngine.from_yaml(
            './neo4j_default_config.yaml')  # the config should be edited by your self

    def test_php71_catch_multiple_exception_types(self):
        """
        先查到 try - catch 的catch部分。然后我预期它有两个exception类型；并且这两个exception类型分别是x和y
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "catch_multiple_exception_types.php"
        )[NODE_FILEID]
        catch_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 9, NODE_FILEID: file_id, NODE_TYPE: TYPE_NAME
            }
        ).all()
        self.assertEqual(len(catch_node), 2)
        exception1 = self.neo4j_engine.get_ast_child_node(catch_node[0])[NODE_CODE]
        exception2 = self.neo4j_engine.get_ast_child_node(catch_node[1])[NODE_CODE]
        self.assertEqual(exception1, 'MissingParameterException')  # add assertion here
        self.assertEqual(exception2, 'IllegalOptionException')
        return True

    def test_php71_class_constant_visibility(self):
        """
            先获取到类的常量 然后判断是否有可见性标签
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "class_constant_visibility.php"
        )[NODE_FILEID]
        const_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file_id, NODE_TYPE: TYPE_CLASS_CONST_GROUP
            }
        ).first()  # 这里类型有点奇怪 解析成了AST_CLASS_CONST_GROUP的根节点 我在framework工具中加了TYPE_CLASS_CONST_GROUP这个定义
        self.assertEqual(const_node['flags'], [MODIFIER_PROTECTED])
        return True

    def test_php71_iterable_pseudo_type(self):
        """
            先判断参数类型为iterable 然后判断循环中迭代采用的是iterable参数
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "iterable_pseudo_type.php"
        )[NODE_FILEID]
        param_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file_id, NODE_TYPE: TYPE_PARAM
            }
        ).first()
        param_type_node = self.neo4j_engine.get_ast_child_node(param_node)
        param_iterable_name = self.neo4j_engine.get_ast_ith_child_node(param_node, 1)['code']
        self.assertEqual(param_type_node['type'], TYPE_TYPE)  # 这里在const类里面新加入了AST_TYPE的定义
        self.assertEqual(param_type_node['flags'], [TYPE_ITERABLE])
        foreach_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file_id, NODE_TYPE: TYPE_FOREACH
            }
        ).first()
        foreach_iterable_name = \
            self.neo4j_engine.get_ast_child_node(self.neo4j_engine.get_ast_child_node(foreach_node))['code']
        self.assertEqual(param_iterable_name, foreach_iterable_name)
        return True

    def test_php71_nullable_types(self):
        """
            直接判断param的子结点是不是nullable即可
            return的判定也类似
        """
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "nullable_types_PARAMETER_TYPE.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "nullable_types_RETURN_TYPE.php"
        )[NODE_FILEID]
        param_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file1_id, NODE_TYPE: TYPE_PARAM
            }
        ).first()
        method_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file2_id, NODE_TYPE: TYPE_METHOD
            }
        ).first()
        type1 = self.neo4j_engine.get_ast_child_node(param_node)['type']
        type2 = self.neo4j_engine.get_ast_ith_child_node(method_node, 4)['type']
        self.assertEqual(type1, TYPE_NULLABLE)
        self.assertEqual(type2, TYPE_NULLABLE)
        return True

    def test_php71_square_bracket_syntax_for_list(self):
        """
            这里的testcase调用1和3
            对于file1 先判断是否有两个array元素 然后判断是否是syntax类型
            对于file3 逐层query比较复杂采用匹配方式找到6个syntax
        """
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "square_bracket_syntax_for_list.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "square_bracket_syntax_for_list_3.php"
        )[NODE_FILEID]
        file1_assign_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file1_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        file1_array_node = self.neo4j_engine.find_ast_child_nodes(file1_assign_node)
        self.assertEqual(len(file1_array_node), 2)
        self.assertEqual(file1_array_node[0]['flags'], [ARRAY_SYNTAX_SHORT])
        self.assertEqual(file1_array_node[1]['flags'], [ARRAY_SYNTAX_SHORT])
        file2_array_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file2_id, NODE_TYPE: TYPE_ARRAY
            }
        ).all()
        self.assertEqual(len(file2_array_node), 6)
        for i in file2_array_node:
            self.assertEqual(i['flags'], [ARRAY_SYNTAX_SHORT])

        return True

    def test_php71_support_for_keys_in_list(self):
        """
            找到array节点 直接比较是否flag标识为ARRAY_SYNTAX_LIST
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "support_for_keys_in_list.php"
        )[NODE_FILEID]
        array_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 9, NODE_FILEID: file_id, NODE_TYPE: TYPE_ARRAY
            }
        ).first()
        self.assertEqual(array_node['flags'], [ARRAY_SYNTAX_LIST])
        return True

    def test_php71_void_functions(self):
        """
            直接判断函数的返回值是否满足条件即可
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "void_functions.php"
        )[NODE_FILEID]
        function_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 11, NODE_FILEID: file_id, NODE_TYPE: TYPE_METHOD
            }
        ).first()
        return_type = self.neo4j_engine.get_ast_ith_child_node(function_node, 4)['flags']
        self.assertEqual(return_type, [TYPE_VOID])
        return True

    def test_php72_object_type_hinting(self):
        """
            直接判断函数返回类型和参数类型是否为object
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "object_type_hinting.php"
        )[NODE_FILEID]
        function_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 13, NODE_FILEID: file_id, NODE_TYPE: TYPE_METHOD
            }
        ).first()
        return_type_node = self.neo4j_engine.get_ast_ith_child_node(function_node, 4)
        self.assertEqual(return_type_node['flags'], [FLAG_TYPE_OBJECT])
        param_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 13, NODE_FILEID: file_id, NODE_TYPE: TYPE_PARAM
            }
        ).first()
        param_type_node = self.neo4j_engine.get_ast_child_node(param_node)
        self.assertEqual(param_type_node['flags'], [FLAG_TYPE_OBJECT])
        return True

    def test_php72_trailing_comma_in_list_syntax(self):
        """
            这个测试可以直接找到use结构并查询是否use_elem有多少个 以此来判断逗号是否完成分隔效果
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "trailing_comma_in_list_syntax.php"
        )[NODE_FILEID]
        use_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file_id, NODE_TYPE: TYPE_USE
            }
        ).first()
        use_elem_node = self.neo4j_engine.find_ast_child_nodes(use_node)
        self.assertEqual(len(use_elem_node), 3)
        return True

    def test_php73_flexible_heredoc_and_nowdoc_syntax(self):
        """
            找到AST_PROP_ELEM类型 并判定子结点是否都为bar 即可判定是否解析成功
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "flexible_heredoc_and_nowdoc_syntax.php"
        )[NODE_FILEID]
        prop_elem_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file_id, NODE_TYPE: TYPE_PROP_ELEM
            }
        ).first()
        var_1 = self.neo4j_engine.get_ast_ith_child_node(prop_elem_node, 0)['code']
        var_2 = self.neo4j_engine.get_ast_ith_child_node(prop_elem_node, 1)['code']
        self.assertEqual(var_1, var_2)
        return True

    def test_php73_list_reference_assignment(self):
        """
            找到第4行的assign左边的array  并判断flags是不是ARRAY_SYNTAX_LIST,即[]这种形式
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "list_reference_assignment.php"
        )[NODE_FILEID]
        array_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 4, NODE_FILEID: file_id, NODE_TYPE: TYPE_ARRAY
            }
        ).first()
        self.assertEqual(array_node['flags'], [ARRAY_SYNTAX_LIST])
        return True

    def test_php73_trailing_comma_in_function_calls(self):
        """
            找到AST_ARG_LIST 然后判断AST子结点是否含有三个参数即可判断逗号是否正确分隔
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "trailing_comma_in_function_calls.php"
        )[NODE_FILEID]
        array_arg_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 4, NODE_FILEID: file_id, NODE_TYPE: TYPE_ARG_LIST
            }
        ).first()
        arg_count = len(self.neo4j_engine.find_ast_child_nodes(array_arg_node))
        self.assertEqual(arg_count, 3)
        return True

    def test_php74_array_spread_operator(self):
        """
            由于新特性会将...array1这种解析为一个新的AST类型AST_UNPACK 故可以直接判断是否有两个unpack类型即可
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "array_spread_operator_1.php"
        )[NODE_FILEID]
        unpack_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file_id, NODE_TYPE: TYPE_UNPACK
            }
        ).all()
        self.assertEqual(len(unpack_node), 2)
        return True

    def test_php74_arrow_functions(self):
        """
            这个特性找到assign节点 并判断子结点是否解析成为了array_function即可
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "arrow_functions.php"
        )[NODE_FILEID]
        assign_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 4, NODE_FILEID: file_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        array_function_node = self.neo4j_engine.get_ast_ith_child_node(assign_node, 1)
        self.assertEqual(array_function_node['type'], TYPE_ARRAY_FUNCTION)
        return True

    def test_php74_null_coalescing_assignment_operator(self):
        """
            找到AST_ASSIGN_OP 直接判断flags是不是BINARY_COALESCE 即可判断??=有没有正确解析
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "null_coalescing_assignment_operator.php"
        )[NODE_FILEID]
        assign_op_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_ASSIGN_OP
            }
        ).first()
        self.assertEqual(assign_op_node['flags'], [BINARY_COALESCE])
        return True

    def test_php74_numeric_literal_separator(self):
        """
            直接找到assign的double值 判断是不是	107925284.88 以此判断107_925_284.88有没有正常解析
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "numeric_literal_separator.php"
        )[NODE_FILEID]
        assign_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        double_number = self.neo4j_engine.get_ast_ith_child_node(assign_node, 1)[NODE_CODE]
        self.assertEqual(double_number, '107925284.88')
        return True

    def test_php74_typed_properties_in_classes(self):
        """
            采用第二个文件 解析第5行的代码 获取type并比较是否为int
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "typed_properties_in_classes_2.php"
        )[NODE_FILEID]
        type_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_TYPE
            }
        ).first()
        self.assertEqual(type_node['flags'], [FLAG_TYPE_LONG])
        return True

    def test_php8_attributes(self):
        """
            这里只用判断是否正确解析成了AST_ATTRIBUTE类型即可
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "attribute_5.php"
        )[NODE_FILEID]
        attribute_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 29, NODE_FILEID: file_id, NODE_TYPE: TYPE_ATTRIBUTE
            }
        ).all()
        self.assertEqual(len(attribute_node), 1)
        return True

    def test_php8_constructor_property_promotion(self):
        """
            这里需要找到construct方法 然后用调用关系看看空定义的construct是否能正确连接CG
            src:constructor_property_promotion_1.php
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "constructor_property_promotion_1.php"
        )[NODE_FILEID]
        call_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 16, NODE_FILEID: file_id, NODE_TYPE: TYPE_NEW
            }
        ).first()
        method_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 10, NODE_FILEID: file_id, NODE_TYPE: TYPE_METHOD
            }
        ).first()
        caller_node = self.neo4j_engine.find_cg_call_nodes(call_node)[0]
        self.assertEqual(caller_node, method_node)
        return True

    def test_php8_match_expression(self):
        """
            这里直接判断assign右侧是否正确解析成了AST_MATCH类型即可
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "match_expression_1.php"
        )[NODE_FILEID]
        assign_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        match_node = self.neo4j_engine.get_ast_ith_child_node(assign_node, 1)
        self.assertEqual(match_node['type'], TYPE_MATCH)
        return True

    def test_php8_named_arguments(self):
        """
            这里判断AST_NAMED_ARGS 查询有没有读取解析到定位名称
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "named_arguments_2.php"
        )[NODE_FILEID]
        name_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 13, NODE_FILEID: file_id, NODE_TYPE: TYPE_NAMED_ARG
            }
        ).first()
        name = self.neo4j_engine.get_ast_child_node(name_node)['code']
        self.assertEqual(name, 'name')
        return True

    def test_php8_new_mixed_type(self):
        """
            这里可以直接找到return的类型 满足是mix类型即为解析成功
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "new_mixed_return_type.php"
        )[NODE_FILEID]
        type_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file_id, NODE_TYPE: TYPE_TYPE
            }
        ).first()
        self.assertEqual(type_node['flags'], [TYPE_MIXED])
        return True

    def test_php8_non_capturing_catches(self):
        """
            这个特性测试主要是找到catch 并连续找到子结点 判断异常抛出类型是否为自定义
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "non-capturing_catches_1.php"
        )[NODE_FILEID]
        catch_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_CATCH
            }
        ).first()
        excption_name = self.neo4j_engine.get_ast_child_node(
            self.neo4j_engine.get_ast_child_node(self.neo4j_engine.get_ast_child_node(catch_node)))['code']
        self.assertEqual(excption_name, 'MySpecialException')
        return True

    def test_php8_nullsafe_operator(self):
        """
            这里判断ASSIGN的右侧子结点是否解析成了nullsafe类型即可
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "nullsafe_1.php"
        )[NODE_FILEID]
        assign_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 3, NODE_FILEID: file_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        null_safe_node = self.neo4j_engine.get_ast_ith_child_node(assign_node, 1)
        self.assertEqual(null_safe_node['type'], TYPE_NULLSAFE_PROP)
        return True

    def test_php8_static_return_type(self):
        """
            这里直接判断new后面的函数名是否为static即可(其实我觉得static()方法应该和其他自定义的方法不太一样 但是是按照自定义方法解析的)
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "static_return_type_1.php"
        )[NODE_FILEID]
        new_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 8, NODE_FILEID: file_id, NODE_TYPE: TYPE_NEW
            }
        ).first()
        method_name = self.neo4j_engine.get_ast_child_node(self.neo4j_engine.get_ast_child_node(new_node))['code']
        self.assertEqual(method_name, 'static')
        return True

    def test_php8_throw_expression(self):
        """
            这里找到第8行的statement_list 然后判断子结点知否能解析为AST_THROW
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "throw_expression_normal.php"
        )[NODE_FILEID]
        state_list_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 4, NODE_FILEID: file_id, NODE_TYPE: TYPE_STMT_LIST
            }
        ).first()
        throw_type = self.neo4j_engine.get_ast_child_node(state_list_node)['type']
        self.assertEqual(throw_type, TYPE_THROW)
        return True

    def test_php8_trailing_comma_in_parameter_lists(self):
        """
            这个新特性找到param list  然后判断param个数可以得到有没有正确分隔
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "trailing_comma.php"
        )[NODE_FILEID]
        param_list_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file_id, NODE_TYPE: TYPE_PARAM_LIST
            }
        ).first()
        params = self.neo4j_engine.find_ast_child_nodes(param_list_node)
        self.assertEqual(len(params), 8)
        return True

    def test_php8_union_type(self):
        """
            这个新特性关注的是能否解析为两个类型 至于int解析成LONG float解析为DOUBLE 就不做过多考虑
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "union_type_1.php"
        )[NODE_FILEID]
        union_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 4, NODE_FILEID: file_id, NODE_TYPE: TYPE_UNION
            }
        ).first()
        type_node = self.neo4j_engine.find_ast_child_nodes(union_node)
        self.assertEqual(len(type_node), 2)
        return True

    def test_php8_use_instanceof_or_new_in_expressions(self):
        """
            对于instanceof只用看assign的右边子节点能不能解析成INSTANCEOF的类型
            对于new同样方法检测是不是解析成了new节点
        """
        file1_id = self.neo4j_engine.get_fig_file_name_node(
            "use_instanceof_in_expressions.php"
        )[NODE_FILEID]
        file2_id = self.neo4j_engine.get_fig_file_name_node(
            "use_new_in_expressions.php"
        )[NODE_FILEID]
        assign_node_1 = self.neo4j_engine.match(
            **{
                NODE_LINENO: 7, NODE_FILEID: file1_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        assign_node_2 = self.neo4j_engine.match(
            **{
                NODE_LINENO: 5, NODE_FILEID: file2_id, NODE_TYPE: TYPE_ASSIGN
            }
        ).first()
        instanceof_node = self.neo4j_engine.get_ast_ith_child_node(assign_node_1, 1)
        new_node = self.neo4j_engine.get_ast_ith_child_node(assign_node_2, 1)
        self.assertEqual(instanceof_node['type'], TYPE_INSTANCEOF)
        self.assertEqual(new_node['type'], TYPE_NEW)
        return True

    def test_php8_constant_and_class_constant_dereferencability(self):
        """
            找到static call的位置 判断子结点是否为class const
        """
        file_id = self.neo4j_engine.get_fig_file_name_node(
            "constant_and_class_constant_dereferencability.php"
        )[NODE_FILEID]
        static_call_node = self.neo4j_engine.match(
            **{
                NODE_LINENO: 12, NODE_FILEID: file_id, NODE_TYPE: TYPE_STATIC_CALL
            }
        ).first()
        class_const = self.neo4j_engine.get_ast_child_node(static_call_node)
        self.assertEqual(class_const['type'], TYPE_CLASS_CONST)
        return True


if __name__ == '__main__':
    unittest.main()
