#!/usr/bin/env python
# -*- coding: UTF-8 -*-
"""
@Project ：code
@File ：time_utils.py
@Author ：yanghao
@Desciption : 时间工具类
@Date ：2022/4/23 0:42
"""
import datetime
import time

import numpy as np


def transfor_timeStr_2_timeStamp(timeStr, precision="millisecond"):
    """
    将时间字符串转化为时间戳格式，时间字符串样例为%Y-%m-%d %H:%M:%S.%f
    :param timeStr: array-like 时间字符串，可以为%Y-%m-%d %H:%M:%S.%f/%Y-%m-%d %H:%M:%S,必须要年月日
    :param precision: 精确度 3个选择：秒级（second）,毫秒级(millisecond),微秒级(microsecond),纳秒(nanosecond)
    :return: array-like 时间戳数组 array
    """

    def in_transfor(time_signal, precision):
        # 先升高到最精确纳秒
        just_timeStr = time_signal.ljust(29, "0")
        t = datetime.datetime.strptime(just_timeStr[:-3], "%Y-%m-%d %H:%M:%S.%f")
        if precision == "millisecond":
            return np.long(t.timestamp() * 1000)
        elif precision == "microsecond":
            return np.long(t.timestamp() * 1000000)
        elif precision == "nanosecond":
            return np.long(t.timestamp() * 1000000000) + np.long(just_timeStr[-3:])
        else:
            # 默认毫秒
            return np.long(t.timestamp() * 1000)

    if isinstance(timeStr, str):
        # 单个时间字符串
        return in_transfor(timeStr, precision)
    else:
        return [in_transfor(time_, precision) for time_ in timeStr]


def test_transfor_timeStr_2_millisecond():
    print(transfor_timeStr_2_timeStamp(["2020-05-04 04:33:39.111111111", "2020-05-04 04:33:39.121111111"]))
