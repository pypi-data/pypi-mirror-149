import networkx as nx
import py2neo
from typing import List
from abc import ABC, abstractmethod
from pjscan.const import *
from pjscan.analysis_framework import AnalysisFramework


class AbstractPrefetchTask(ABC):
    '''

        Attributes
        ----------

        cache_graph : cache_graph.BasicCacheGraph
            use the cache pool to record the result of prefetch

        Method
        ------
        do_task()
            the method you should definite your own task.

            In this method, you should finish your own prefetch stratege, including prefetch condition(in which condition you will do prefetch),
            prefetch operation and store it in cache_graph. Especially, if the parameter your prefetch is costomizedm, please use contomimzed_storage to store it.


        Examples
        --------

        This is an example of how to override the do_task() method.
        You want to prefetch about the PDG relationship,
        and you use the drop out strategy to judge whether the thread should prefetch,
        then difinite the query of database

        >>> def do_task(self):
        ...     if random.randint(0, 100) * 0.01 >= self.drop_out:
        ...         return
        ...     if self.node[NODE_TYPE] not in AST_ROOT:
        ...         return
        ...     if self.cache_graph.get_pdg_inflow(self.node) is None:
        ...         rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[None, self.node], r_type=DATA_FLOW_EDGE, ).all()
        ...         self.cache_graph.add_pdg_inflow(self.node, rels)
        ...     if self.cache_graph.get_pdg_outflow(self.node) is None:
        ...         rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[self.node, None], r_type=DATA_FLOW_EDGE, ).all()
        ...         self.cache_graph.add_pdg_outflow(self.node, rels)

        Notes
        -----
        You can extend this method your self.

        Otherwise, we provide 4 class which extends it , which used for prefetch different relationships

        You can use it as
            AstPrefetchTask

            CfgPrefetchTask

            PdgPrefetchTask

            CgPrefetchTask

        Besides, the attributes 'analysis_framework' is pjscan.AnalysisFramework, it will initialize in prefetch thread
        to make a new connection with database.
        '''

    def __init__(self, cache_graph, analysis_framework: AnalysisFramework = None):
        """Initial the prefetch task

            Parameters
            ----------
            cache_graph : cache_graph.BasicCacheGraph
                use the cache pool to record the result of prefetch

            """
        if cache_graph is None:
            raise "Task Wrong!Graph is not definited!!"
        self.cache_graph = cache_graph
        self.analysis_framework = None  # type:AnalysisFramework

    @abstractmethod
    def do_task(self):
        """do your own task.

        """
        return None


class AstPrefetchTask(AbstractPrefetchTask):
    def __init__(self, **kwargs):
        """Initial AST the prefetch task

        Parameters
        ----------
        args
        kwargs

        Notes
        _____
        attributes 'node' is the node to be prefetched.

        """
        super(AstPrefetchTask, self).__init__()
        self.node = kwargs.get("node", None)

    def do_task(self):
        """do the task to query AST relationship of a node

        And store it in cache_graph

        """
        self.cache_graph.add_node(self.node)
        if self.cache_graph.get_ast_inflow(self.node) is None:
            rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[None, self.node],
                                                                           r_type=AST_EDGE, ).all()
            self.cache_graph.add_ast_inflow(self.node, rels)
        if self.cache_graph.get_ast_outflow(self.node) is None:
            rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[self.node, None],
                                                                           r_type=AST_EDGE, ).all()
            self.cache_graph.add_ast_outflow(self.node, rels)


class CfgPrefetchTask(AbstractPrefetchTask):
    def __init__(self, **kwargs):
        """Initial CFG the prefetch task

        Parameters
        ----------
        args
        kwargs

        Notes
        _____
        attributes 'node' is the node to be prefetched.

        """
        super(CfgPrefetchTask, self).__init__()
        self.node = kwargs.get("node", None)

    def do_task(self):
        """do the task to query CFG relationship of a node

        And store it in cache_graph

        """
        self.cache_graph.add_node(self.node)
        if self.cache_graph.get_cfg_inflow(self.node) is None:
            rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[None, self.node],
                                                                           r_type=CFG_EDGE, ).all()
            self.cache_graph.add_cfg_inflow(self.node, rels)
        if self.cache_graph.get_cfg_outflow(self.node) is None:
            rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[self.node, None],
                                                                           r_type=CFG_EDGE, ).all()
            self.cache_graph.add_cfg_outflow(self.node, rels)


class PdgPrefetchTask(AbstractPrefetchTask):
    def __init__(self, **kwargs):
        """Initial PDG the prefetch task

        Parameters
        ----------
        args
        kwargs

        Notes
        _____
        attributes 'node' is the node to be prefetched.

        """
        super(PdgPrefetchTask, self).__init__()
        self.node = kwargs.get("node", None)

    def do_task(self):
        """do the task to query PDG relationship of a node

        And store it in cache_graph

        """
        if self.node[NODE_TYPE] in AST_ROOT:
            self.cache_graph.add_node(self.node)
            if self.cache_graph.get_pdg_inflow(self.node) is None:
                # TODO I NEED TO LABEL WHICH IS AST_ROOT.
                rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[None, self.node],
                                                                               r_type=DATA_FLOW_EDGE, ).all()
                self.cache_graph.add_pdg_inflow(self.node, rels)
            if self.cache_graph.get_pdg_outflow(self.node) is None:
                rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[self.node, None],
                                                                               r_type=DATA_FLOW_EDGE, ).all()
                self.cache_graph.add_pdg_outflow(self.node, rels)


class CgPrefetchTask(AbstractPrefetchTask):
    def __init__(self, **kwargs):
        """Initial CG the prefetch task

        Parameters
        ----------
        args
        kwargs

        Notes
        _____
        attributes 'node' is the node to be prefetched.

        """
        super(CgPrefetchTask, self).__init__()
        self.node = kwargs.get("node", None)

    def do_task(self):
        """do the task to query CG relationship of a node

        And store it in cache_graph

        """
        self.cache_graph.add_node(self.node)
        if self.cache_graph.get_cg_inflow(self.node) is None:
            rels = self.analysis_framework.neo4j_graph.relationships.match(nodes=[None, self.node],
                                                                           r_type=CALLS_EDGE, ).all()
            self.cache_graph.add_cg_inflow(self.node, rels)
        if self.cache_graph.get_cg_outflow(self.node) is None:
            rels = self.analysis_framework_neo4j_graph.relationships.match(nodes=[self.node, None],
                                                                           r_type=CALLS_EDGE, ).all()
            self.cache_graph.add_cg_outflow(self.node, rels)
