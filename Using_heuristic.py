import pandas as pd
import os


def Coding_index():
    # 文件名
    filename = os.getcwd() + r'\heuristic.xlsx'
    # 读取excel的task
    data_task = pd.read_excel(filename, sheet_name='Sheet1')
    # 用于存储格式化后的总数据
    data_index = str(data_task.values[0, 1]).split(',')
    data_index = list(map(int, data_index))
    return data_index


def Coding_operation():
    # 文件名
    filename = os.getcwd() + r'\heuristic.xlsx'
    # 读取excel的task
    data_task = pd.read_excel(filename, sheet_name='Sheet1')
    # 用于存储格式化后的总数据

    data_operation = str(data_task.values[1, 1]).split(',')
    data_operation = list(map(int, data_operation))
    return data_operation
