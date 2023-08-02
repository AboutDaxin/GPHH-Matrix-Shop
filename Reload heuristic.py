import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os

# 文件名
filename = os.getcwd() + r'\heuristic.xlsx'
data_task = pd.read_excel(filename, sheet_name='Heuristic')
# 进行格式化
a = data_task.values.tolist()
index_array = data_task.values[0, 1]
index_array = int(index_array)
operation_array = data_task.values[1, 1]
print(index_array)
