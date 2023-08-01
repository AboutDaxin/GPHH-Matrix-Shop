import copy

import matplotlib.pyplot as plt
from statistics import mean
import numpy as np
import pandas as pd
import os


# def plt_evolve(GP, generations, data_avg, data_best):
#     # map：映射，让data中的元素依次使用mean方法执行，返还值生成一个列表
#     # 此处将data_avg中的每一个列表取平均值，生成一个新列表(还是共52个元素)
#     data_avg = [i for i in map(mean, data_avg)]
#     # 同上
#     data_best = [i for i in map(mean, data_best)]
#     # 生成画图x轴，从1000到2040（不含），间隔20。实际为1000-2020，共51段
#     x = np.arange(GP.population_size, GP.population_size + GP.children_size * generations, GP.children_size)
#     # 输出代数与平均值和最优值的图像，横轴为评估次数，纵轴为适应度
#     plt.figure(2)
#     plt.plot(x, data_avg, x, data_best)
#     plt.xlabel('Evaluations')
#     plt.ylabel('Fitness')

# 生成gantt图
def plt_gantt(best, number):
    # 文字格式初始化
    # 使用中文文字
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    # 定义两个格式字典
    fontdict_task = {
        "family": "Microsoft YaHei",
        "style": "oblique",
        "weight": "bold",
        "color": "black",
        "size": 6
    }
    fontdict_time = {
        "family": "Microsoft YaHei",
        "style": "oblique",
        "color": "black",
        "size": 6
    }
    color = ['blue', 'green', 'red', 'yellow', 'purple', 'cyan', 'gray']

    # 提取数据
    complete_data = dict(zip(best.draw_key, best.draw_value))
    # 绘图操作
    if number == 0:
        plt.figure('TTGP Gantt', (26, 12))
    elif number == 1:
        plt.figure('TTGP-ISP Gantt', (26, 12))
    elif number == 2:
        plt.figure('CCGP Gantt', (26, 12))
    elif number == 3:
        plt.figure('CCGP-ISP Gantt', (26, 12))
    for k, v in complete_data.items():
        # 画job甘特图
        plt.barh(y=k[2], width=v[2], left=v[0], edgecolor="black", color=color[k[0] % 7])
        # 画job标注
        plt.text(v[0] + 0.1, k[2] - 0.14, "Task:\n" + "(" + str(k[0]) + "," + str(k[1]) + ")",
                 fontdict=fontdict_task)
        plt.text(v[0] + 0.5, k[2], "Start:\n " + str(v[0]), fontdict=fontdict_time)
        plt.text(v[0] + 0.5, k[2] - 0.35, "End:\n " + str(v[1]), fontdict=fontdict_time)

        # 画transtime甘特图
        plt.barh(y=k[2], width=v[3], left=v[0] - v[3], edgecolor="black", color='black', alpha=0.1)
        # 画transtime标注
        plt.text(v[0] - v[3] + 0.1, k[2], "Set time:\n " + str(v[3]) if v[3] != 0 else '', fontdict=fontdict_time)
    # 生成x轴刻度
    plt.xticks(range(best.makespan + 2))
    # 生成y轴label
    ylabels = []
    m = []
    for i in complete_data:
        m.append(i[2])
    for i in range(max(m)):
        ylabels.append("Cell" + str(i + 1))
    plt.yticks(range(1, max(m) + 1), ylabels, rotation=45)
    # 生成title
    if number == 0:
        plt.title("Gantt-TTGP")
    elif number == 1:
        plt.title("Gantt TTGP-ISP")
    elif number == 2:
        plt.title("Gantt-CCGP")
    elif number == 3:
        plt.title("Gantt CCGP-ISP")
    plt.xlabel("Process Time /h")
    plt.ylabel("Cells")
    plt.show()


# 生成目标比较图
def plt_compare(GP0, generations0, data_avg0, data_best0, data_time0, data_complexity0,
                GP1, generations1, data_avg1, data_best1, data_time1, data_complexity1,
                GP2, generations2, data_avg2, data_best2, data_time2, data_complexity2,
                GP3, generations3, data_avg3, data_best3, data_time3, data_complexity3):
    # 画个演化过程比较图
    plt.figure('comparison_objective')
    # 第一组
    # map：映射，让data中的元素依次使用mean方法执行，返还值生成一个列表
    # 此处将data_avg中的每一个列表取平均值(run次)，生成一个新列表
    data_avg0 = [i for i in map(mean, data_avg0)]
    # data_best0 = [i for i in map(mean, data_best0)]
    # 取相反数，绘图用
    data_avg0 = [-i for i in data_avg0]
    # data_best0 = [-i for i in data_best0]
    # 生成画图x轴
    # x0 = np.arange(GP0.population_size, GP0.population_size + GP0.children_size * generations0, GP0.children_size)
    x0 = range(generations0)
    # 输出代数与平均值和最优值的图像，横轴为评估次数，纵轴为适应度
    plt.plot(x0, data_avg0, label='TTGP')
    # plt.plot(x0, data_best0, label='Enable_best')
    # 第二组
    data_avg1 = [i for i in map(mean, data_avg1)]
    data_avg1 = [-i for i in data_avg1]
    x1 = range(generations1)
    plt.plot(x1, data_avg1, label='TTGP-ISP')
    # 第三组
    data_avg2 = [i for i in map(mean, data_avg2)]
    data_avg2 = [-i for i in data_avg2]
    x2 = range(generations2)
    plt.plot(x2, data_avg2, label='CCGP')
    # 第四组
    data_avg3 = [i for i in map(mean, data_avg3)]
    data_avg3 = [-i for i in data_avg3]
    x3 = range(generations3)
    plt.plot(x3, data_avg3, label='CCGP-ISP')
    # 加标注
    plt.legend()
    plt.xlabel('Evaluations')
    plt.ylabel('Objectives')

    # 画个演化时间比较图
    plt.figure('time cost comparison ')
    # 第一组
    data_time0 = [i for i in map(mean, data_time0)]
    # 去掉第一个元素，0
    temp_data_time0 = copy.deepcopy(data_time0)
    temp_data_time0.pop(0)
    xt0 = range(1, generations0)
    plt.plot(xt0, temp_data_time0, label='TTGP time cost')
    # 第二组
    data_time1 = [i for i in map(mean, data_time1)]
    temp_data_time1 = copy.deepcopy(data_time1)
    temp_data_time1.pop(0)
    xt1 = range(1, generations1)
    plt.plot(xt1, temp_data_time1, label='TTGP-ISP time cost')
    # 第三组
    data_time2 = [i for i in map(mean, data_time2)]
    temp_data_time2 = copy.deepcopy(data_time2)
    temp_data_time2.pop(0)
    xt2 = range(1, generations2)
    plt.plot(xt2, temp_data_time2, label='CCGP time cost')
    # 第四组
    data_time3 = [i for i in map(mean, data_time3)]
    temp_data_time3 = copy.deepcopy(data_time3)
    temp_data_time3.pop(0)
    xt3 = range(1, generations3)
    plt.plot(xt3, temp_data_time3, label='CCGP-ISP time cost')
    # 加标注
    plt.legend()
    plt.xlabel('Generations')
    plt.ylabel('Time')

    # 画个复杂度比较图
    plt.figure('complexity comparison')
    # 第一组
    data_complexity0 = [i for i in map(mean, data_complexity0)]
    xc0 = range(generations0)
    plt.plot(xc0, data_complexity0, label='TTGP complexity')
    # 第二组
    data_complexity1 = [i for i in map(mean, data_complexity1)]
    xc1 = range(generations1)
    plt.plot(xc1, data_complexity1, label='TTGP-ISP complexity')
    # 第三组
    data_complexity2 = [i for i in map(mean, data_complexity2)]
    xc2 = range(generations2)
    plt.plot(xc2, data_complexity2, label='CCGP complexity')
    # 第四组
    data_complexity3 = [i for i in map(mean, data_complexity3)]
    xc3 = range(generations3)
    plt.plot(xc3, data_complexity3, label='TTGP-ISP complexity')
    # 加标注
    plt.legend()
    plt.xlabel('Evaluations')
    plt.ylabel('Complexity')

    # 输出时间进化数据表格
    df = pd.DataFrame({"generations": xc0, "TTGP time": data_time0, "TTGP-ISP time": data_time1,
                       "CCGP time": data_time2, "CCGP-ISP time": data_time3,
                       "TTGP complexity": data_complexity0, "TTGP-ISP complexity": data_complexity1,
                       "CCGP complexity": data_complexity2, "CCGP-ISP complexity": data_complexity3})
    df = df.set_index('generations')
    df.to_excel(os.getcwd() + '\\data_temp.xlsx')


# 生成运算时间比较图
def plt_process_time(time0, time1, time2, time3):
    plt.figure('time_cost')
    plt.bar(1, time0, width=0.3, facecolor='blue', edgecolor='white')
    plt.bar(2, time1, width=0.3, facecolor='yellow', edgecolor='white')
    plt.bar(3, time2, width=0.3, facecolor='green', edgecolor='white')
    plt.bar(4, time3, width=0.3, facecolor='red', edgecolor='white')
    plt.text(1, time0 + 0.05, '%.5f' % time0, ha='center', va='bottom')
    plt.text(2, time1 + 0.05, '%.5f' % time1, ha='center', va='bottom')
    plt.text(3, time2 + 0.05, '%.5f' % time2, ha='center', va='bottom')
    plt.text(4, time3 + 0.05, '%.5f' % time3, ha='center', va='bottom')
    plt.xticks([1, 2, 3, 4], ['TTGP', 'TTGP-ISP', 'CCGP', 'CCGP-ISP'])


# 生成提琴图
def plt_violin(data_avg0, data_best0, data_avg1, data_best1, data_avg2, data_best2, data_avg3, data_best3):
    plt.figure('violin_objective')
    # 取相反数，绘图用
    data_avg0 = [-i for i in data_avg0]
    data_best0 = [-i for i in data_best0]
    data_avg1 = [-i for i in data_avg1]
    data_best1 = [-i for i in data_best1]
    data_avg2 = [-i for i in data_avg2]
    data_best2 = [-i for i in data_best2]
    data_avg3 = [-i for i in data_avg3]
    data_best3 = [-i for i in data_best3]
    # 绘图
    plt.subplot(2, 1, 1)
    plt.violinplot([data_avg0, data_avg1, data_avg2, data_avg3], showmeans=True, showmedians=True)
    plt.xticks([1, 2, 3, 4], ['TTGP Average', 'TTGP-ISP Average', 'CCGP Average', 'CCGP-ISP Average'])
    plt.subplot(2, 1, 2)
    plt.violinplot([data_best0, data_best1, data_best2, data_best3], showmeans=True, showmedians=True)
    plt.xticks([1, 2, 3, 4], ['TTGP Best', 'TTGP-ISP Best', 'CCGP Best', 'CCGP-ISP Best'])

