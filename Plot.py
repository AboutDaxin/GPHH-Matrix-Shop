import matplotlib.pyplot as plt
import os


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
        ylabels.append("Cell" + " " + str(i + 1))
    plt.yticks(range(1, max(m) + 1), ylabels, rotation=45)
    # 生成title
    if number == 0:
        plt.title("Gantt")
    elif number == 1:
        plt.title("Gantt TTGP-ISP")
    elif number == 2:
        plt.title("Gantt-CCGP")
    elif number == 3:
        plt.title("Gantt CCGP-ISP")
    plt.xlabel("Process Time /h")
    plt.ylabel("Cells")
    plt.savefig(os.path.dirname(os.getcwd()) + r'\output_file\Gantt.jpg')
    plt.show()
