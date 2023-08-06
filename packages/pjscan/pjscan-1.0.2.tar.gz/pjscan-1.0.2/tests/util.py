import os
from typing import *
import sys
from io import StringIO

import pandas as pd


class StatisticContextManager(object):
    """
    用于统计的context manager

    """

    def __init__(self, iterable: Union[Iterable, str], result: List[Dict] = None,
                 output_dir="Statistic",
                 sum_callback=Union[Callable, Iterable[Callable]],
                 result_callback=Union[Callable, Iterable[Callable]]):
        self._result = result if result is not None else []
        if isinstance(iterable, str):
            self.iterable = [iterable]
        else:
            self.iterable = iterable
        self.cache = {}
        self.output_dir = output_dir

        if sum_callback is not None:
            self.sum_callback = [sum_callback] if isinstance(sum_callback, Callable) else sum_callback
        else:
            self.sum_callback = []

        if result_callback is not None:
            self.result_callback = [result_callback] if isinstance(result_callback, Callable) else result_callback
        else:
            self.result_callback = []

    def __iter__(self):
        return self.iterable.__iter__()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # 参数分别为异常类型、异常信息和堆栈
        if exc_type:
            print('error', exc_value, )

    @property
    def result(self):
        return self._result

    def push_result(self, r: Dict):
        self._result.append(r)

    def pop_result(self):
        return pd.DataFrame(self._result)

    def store_result(self, output_path, sort_value=None):
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
        if sort_value:
            return pd.DataFrame(self._result).sort_values(by=sort_value).to_csv(
                os.path.join(self.output_dir, output_path), index=False, sep='\t')
        else:
            return pd.DataFrame(self._result).to_csv(os.path.join(self.output_dir, output_path), index=False, sep='\t')

    def sum_result(self):
        if self._result.__len__() >= 1:
            summery = {}
            for k in self._result[-1].keys():
                res = 0
                _a = 0
                _b = 0
                _c = 0
                _d = 0
                for sub in self._result:
                    if isinstance(sub[k], str):
                        is_summary_percentage = summary_percentage(sub[k])
                        if is_summary_percentage:
                            _a += is_summary_percentage[0]
                            _b += is_summary_percentage[1]
                        is_summary_tuple = summary_tuple(sub[k])
                        if is_summary_tuple:
                            _c += is_summary_tuple[0]
                            _d += is_summary_tuple[1]

                    elif isinstance(sub[k], int) or isinstance(sub[k], float):
                        res += sub[k]
                if _b != 0:
                    summery[k] = join_and_static(_a, _b)
                elif _c != 0 and _d != 0:
                    summery[k] = f"{_c},{_d}"
                else:
                    summery[k] = res
            # self._result.append({
            #     k: sum(map(lambda x: x[k] if isinstance(x[k], int) else summary_percentage(x[k]), self._result)) for k in
            #     self._result[-1].keys()
            # })
            self.push_result(summery)


import re


def summary_percentage(string):
    sub = re.findall(r"(.*?) / (.*?) \((.*?)%\)", string)
    if sub.__len__() == 1 and sub[0].__len__() == 3:
        return int(sub[0][0]), int(sub[0][1])
    else:
        return False


def summary_tuple(string):
    sub = re.findall(r"^(.*?) , (.*?)$", string)
    if sub.__len__() == 1 and sub[0].__len__() == 2:
        return int(sub[0][0]), int(sub[0][1])
    else:
        return False


def join_and_static(n, total):
    assert n < total
    if total == 0:
        return "0 / 0 (100%)"
    p = round(n / total, 4) * 100
    return f"{n} / {total} " + "(%.2f" % p + "%)"
