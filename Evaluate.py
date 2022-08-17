from random import shuffle
import copy
from Modeling import Job
from statistics import mean


# 实例化方法——适应度评估（Individual类的evaluate）（核心）
def evaluate(individual, problems_origin):
    # 针对每个个体创建一个列表，用于存储针对多个问题的调度方案
    individual.scheme = None
    # 初始化每个Individual的fitnesses列表
    individual.fitnesses = []
    problems = copy.deepcopy(problems_origin)
    # 用于存储绘图用字典的key和value
    draw_key = []
    draw_value = []

    # 遍历problems中的每一项元素，执行评估（目前只有1个problem）
    for problem in problems:
        # hyper_period属性传参
        hyper_period = problem.hyper_period
        # 初始化每个Individual的各项目标函数
        individual.total_process_time = 0
        individual.total_due_time = 0
        # 用于存储task的顺序（包含stations数量的列表， 每个列表有time个元素）
        jobsorts = [[[] for _ in range(hyper_period)] for _ in range(len(problem.stations))]
        # 用于查看实时fitness的辅助变量
        fitness_vals = []
        # 初始化辅助变量（工时变量）
        process_time = 0
        # 初始化辅助变量（拖期变量）
        missed_deadlines = 0
        # 初始化总作业序列列表
        stations = [station for station in problem.stations]

        # 遍历每个时刻，执行过程仿真
        for time in range(hyper_period + 1):

            # 路由规则
            # 遍历所有task，用于给每个station的job序列加入新Job
            for task in problem.tasks:
                # 到达一个判定点（task已到释放时间，还有未执行的工序，任务刚弹出需要重排）
                if task.release <= time and task.exec_time != [] and task.need_popped is True:
                    # 初始化一个备选station临时存放点
                    stations_temp = []
                    # 基于该task遍历所有station，释放一个job至对应station的job序列
                    for station in stations:
                        # 如果该task的最前道序可以使用该station
                        if task.process[0] in station.capacity:
                            # 生成备选station列表
                            stations_temp.append(station)
                            # 评估确定该station的优先级
                            # 如果该station序列中存在job
                            if station.queue:
                                # 过渡优先值初始化
                                priority_temp = 0
                                # 遍历station中所有job并分别计算优先值
                                for job in station.queue:
                                    # 临时优先值为所有遍历完job的优先值总和
                                    priority_temp += individual.root.left.interpret(job, station, time)
                                # 得到该station的当前优先值
                                station.priority = priority_temp
                            # 如果该station序列中没有任务，则优先值为0（最高级别）
                            else:
                                station.priority = 0
                    # 确定被选中的station（优先值最小为最高级别）
                    station_best = min(stations_temp)
                    # 在job序列对应的station中加入一个Job
                    station_best.queue.append(Job(task, station_best, time))
                    # 该station排序状态改为“需要重排”
                    station_best.need_popped = False
                    # 该task状态变为“不需要重排”
                    task.need_popped = False

            # 排序规则
            # 判断是否要执行重排
            for station in stations:
                # 如果该station需要进行重排
                if not station.have_popped:
                    # 对该station的job序列执行遍历，重排
                    for job in station.queue:
                        # 计算该job的优先级数值
                        job.priority = individual.root.right.interpret(job, station, time)
                    # 随机排列该station的job序列
                    shuffle(station.queue)
                    # 将该station的job序列按优先级从小到大排序（根据Job的富比较方法）
                    station.queue.sort()
                    # 排序状态变为已排完，不需要重排
                    station.have_popped = True

            # 对每个station的job执行一系列操作
            # 按每个station分别进行判断
            for station in stations:
                # 如果本job序列还存在job则执行
                if len(station.queue) > 0:
                    # 对job列表中第一个job判断。当前时间大于job堵塞开始时间，并且job持续堵塞时
                    if time > station.queue[0].blocking_start and station.queue[0].blocking_duration > 0:
                        # 堵塞持续时间-1
                        station.queue[0].blocking_duration -= 1
                    # 序列中第一个job执行时间-1
                    station.queue[0].exec_time -= 1
                    # 总工时+1
                    process_time += 1
                    # 状态改为“正在运行”
                    station.queue[0].has_run = True

                    # 如果当前job执行完毕
                    if station.queue[0].exec_time <= 0:
                        # 逐步生成draw_key中的元组(任务序号、工序序号、工作站序号)
                        draw_key.append((station.queue[0].num, station.queue[0].task.process_num[0], station.num))
                        # 逐步生成draw_value中的元组
                        draw_value.append((time+1 - station.queue[0].task.exec_time[0],
                                           time+1, station.queue[0].task.exec_time[0]))
                        # 删除该task的当前序工艺类型
                        station.queue[0].task.process.pop(0)
                        station.queue[0].task.process_num.pop(0)
                        # 删除该task的当前序执行时间
                        station.queue[0].task.exec_time.pop(0)
                        # 该task状态变为刚弹出
                        station.queue[0].task.need_popped = True
                        # 状态改为未排完，需要重排
                        station.have_popped = False
                        # 在序列中删除该运行结束的job
                        station.queue.pop(0)

                    # 对当前station的job序列进行遍历，计算拖期
                    for job in station.queue:
                        # 如果遍历出有个job，已经超期，且还没执行完毕
                        if job.deadline != 0 and job.deadline < time and job.exec_time > 0:
                            # 如果是非周期任务则零星拖期参数+1
                            missed_deadlines += 1

            # 调试用
            fitness_vals.append(missed_deadlines)

        # 添加个体对本问题的调度方案
        individual.scheme = jobsorts
        # 添加个体对本问题的适应度值
        individual.fitnesses.append(-missed_deadlines - process_time - 2*individual.tree_complexity())
        # 添加各项目标函数值
        individual.total_due_time = missed_deadlines
        individual.total_process_time = process_time
        # 添加绘图辅助参数
        individual.draw_key = draw_key
        individual.draw_value = draw_value

        # # 个体统计
        # individual.stats.append()

    # 个体适应度值取列表平均数（目前只有一种）
    individual.fitness = mean(individual.fitnesses)
