from GP import GP
from Modeling import Problem
from Modeling import Task, Station
import Input_outside


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
    for n in range(1):
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
