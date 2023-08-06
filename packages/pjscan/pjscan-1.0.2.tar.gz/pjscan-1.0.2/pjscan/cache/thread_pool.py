import py2neo
from .prefetch_thread import *


class PrefetchPool(object):
    '''PrefetchPool is the manager of all the PrefetchThreads

    PrefetchPool will be created in traversal , with the input the cache_graph and thread_count

    Attributes
    ----------

    threads: List[PrefetchThread]
        the list that manage all prefetch thread.

    queue: queue.Queue
        the queue to be prefetched, in this queue there is many tasks to be done.

    cache_graph : cache_graph.BasicCacheGraph
        use the cache pool to record the result of prefetch

    Method
    ------
    start_all()
        start all the thread.

    stop_all()
        stop all the thread

    put_task_in_queue(task)
            difinite how to put the task in queue
    '''

    def __init__(self, cache_graph, thread_count: int = 0):
        """PrefetchPool is the manager of all the PrefetchThreads

        PrefetchPool will be created in traversal , with the input the cache_graph and thread_count

        Attributes
        ----------
        cache_graph : BasicCacheGraph
            the cache_graph ref

        threads : List[PrefetchThread]
            the list that manage all prefetch thread, the length of threads is thread_count

        queue : queue.Queue
            stores all the task to be done, all the thread fetch task from this queue and do them.

        Method
        ------
        start_all()
            start all the thread

        stop_all()
            stop all the thread

        put_task_in_queue(task)
            difinite how to put the task in queue

        """
        self.threads = []
        self.queue = Queue()
        self.cache_graph = cache_graph
        for i in range(thread_count):
            prefetch_thread = PrefetchThread(queue=self.queue, cache_graph=self.cache_graph)
            prefetch_thread.daemon = True
            self.threads.append(prefetch_thread)
        self.start_all()

    def start_all(self):
        """Start all the threads

        """
        for i in self.threads:
            i.start()

    def stop_all(self):
        """Stop all the threads

        """
        for i in self.threads:
            i.stop()

    def put_task_in_queue(self, task):
        """Put task in thread

        Parameters
        ----------
        task : the class extends to AbstractPrefetchTask
            put this task in queue

        """
        self.queue.put(task)
