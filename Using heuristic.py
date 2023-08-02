import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 文件名
filename = os.getcwd() + r'\heuristic.xlsx'
# 读取excel的task
data_task = pd.read_excel(filename, sheet_name='Heuristic')
# 用于存储格式化后的总数据
data_index = str(data_task.values[0, 1]).split(',')
data_index = list(map(int, data_index))
data_operation = str(data_task.values[1, 1]).split(',')
data_operation = list(map(int, data_operation))
print(data_operation)
