from GP import GP
from Modeling import Problem
from Modeling import Task, Station
import Input_outside
import Plot


def Instance():
    # 用于存储对比运行的关键数据
    output_gp = []
    output_generations = []
    output_data_avg = []
    output_data_best = []
    output_data_time = []
    output_data_complexity = []
    output_time_cost = []
    # 执行多次测试
    for n in range(4):
        # 第几次试验
        test_index = n
        # 实例化一个gp，n为第几次运行
        gp = GP(number=n)
        # 创建一个存储实例问题的列表
        problems = []
        # 实例化一个任务
        task_list = []
        for t in Input_outside.TASK:
            task_list.append(Task(t[0], t[1], t[2], t[3], t[4]))
        # 实例化一个车间
        station_list = []
        for s in Input_outside.STATION:
            station_list.append(Station(s[0], s[1], s[2]))
        # 将该实例加入problems列表（第三个参数为限定时间）
        problems.append(Problem(task_list, station_list, 9999))
        # 执行该问题
        gp.run(problems, test_index)
        # 传参，存储绘图用数据
        output_gp.append(gp)
        output_generations.append(gp.generations)
        output_data_avg.append(gp.data_avg)
        output_data_best.append(gp.data_best)
        output_data_time.append(gp.data_time)
        output_data_complexity.append(gp.data_complexity)
        output_time_cost.append(gp.time_cost)

    # 绘图对比收敛速度
    Plot.plt_compare(output_gp[0], output_generations[0], output_data_avg[0], output_data_best[0],
                     output_data_time[0], output_data_complexity[0],
                     output_gp[1], output_generations[1], output_data_avg[1], output_data_best[1],
                     output_data_time[1], output_data_complexity[1],
                     output_gp[2], output_generations[2], output_data_avg[2], output_data_best[2],
                     output_data_time[2], output_data_complexity[2],
                     output_gp[3], output_generations[3], output_data_avg[3], output_data_best[3],
                     output_data_time[3], output_data_complexity[3]
                     )

    # 绘图对比计算时间
    Plot.plt_process_time(output_time_cost[0], output_time_cost[1], output_time_cost[2], output_time_cost[3])

    # 绘图10次独立运行的优化目标提琴图
    Plot.plt_violin(output_data_avg[0][-1], output_data_best[0][-1], output_data_avg[1][-1], output_data_best[1][-1],
                    output_data_avg[2][-1], output_data_best[2][-1], output_data_avg[3][-1], output_data_best[3][-1])


