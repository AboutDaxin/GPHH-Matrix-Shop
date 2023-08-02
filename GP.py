from math import ceil
import Evaluate
from Tree import Individual
import Plot
import time
import pandas as pd
import os


# 最大个体评估次数（包含初代的个体）
MAX_EVALUATIONS = 1
# 运行多少次
RUNS = 1


# 定义GP类
class GP:
    # 初始化方法：在GP类进行实例化时执行。参数为如下，简化参数弃用
    def __init__(self, number, population_size=1, children_size=0, mutation=0.05, duplication=0.1, parsimony=0.5):
        # 生成此实例的一个种群
        # 类属性：定义实例的种群(population)为一个列表
        self.number = number
        self.population = []
        # 传参用
        self.generations = None
        self.data_avg = None
        self.data_best = None
        self.data_time = None
        self.data_complexity = None
        self.time_cost = None

        # 生成一个个体
        for _ in range(ceil(population_size)):
            # 实例化个体，使用Tree模块的Individual类
            individual = Individual(parsimony)
            # 使用full方法形成个体，使用Tree模块的full函数
            individual.full(4)
            # 在种群列表中增加这个个体，完成整个种群的构建
            self.population.append(individual)

        # 设置此实例的一些初始化变量
        # “父”，“子”为空列表
        # 评估次数初始值为0，简化参数为预设的0.5
        self.parents = []
        self.population_size = population_size
        self.children = []
        self.children_size = children_size
        self.mutation = mutation
        self.duplication = duplication
        self.evaluations = 0
        self.parsimony = parsimony

    # 定义实例化方法——问题的适应度评估(GP类)
    def evaluate(self, problems, test_index):
        test_index = test_index
        # 对子代中的个体进行遍历
        for individual in self.children:
            # 对每个个体执行核心evaluate(Individual类)方法
            Evaluate.evaluate(individual, problems, test_index)
            # 执行一次循环，评估次数参数+1
            self.evaluations += 1

    # 定义实例化方法——运行
    def run(self, problems, test_index):
        print('start:'+str(test_index))
        # 记录代码运行时间
        start_time = time.process_time()
        # 设置bests为一个空列表，用于存储最优结果
        bests = []

        # 执行RUN次循环
        for run in range(RUNS):
            # 执行初始化操作
            self.__init__(number=self.number)
            # 初次评估，因为evaluate方法是针对children属性执行的，所以将population暂时转移了一下
            self.children = self.population
            # 执行适应度评估（GP类）
            self.evaluate(problems, test_index)
            self.population = self.children

            # 本轮运行完成，输出优化信息
            # 输出本次运行次数（占位符）
            print('==== RUN {} ===='.format(run))
            # 设置当前最佳为population中的最优Individual（富比较）
            current_best = max(self.population)
            # 输出终代最优及平均Individual的适应度值和heuristic格式等信息
            print('best fitness: {}\nbest objective: {}'
                  '\n(Min-based)heuristic-routing: {}\n(Min-based)heuristic-sequencing: {}'.
                  format(current_best.fitness, current_best.objective,
                         current_best.root.left.string(), current_best.root.right.string()))

            # 输出目标函数值
            print('total process time: {}\ntotal due time: {}\nmakespan: {}'.
                  format(current_best.total_process_time, current_best.total_due_time, current_best.makespan))
            # 输出stats值
            print('stats:{{{}, total set time: {}}}'.format(current_best.stats, current_best.total_transtime))
            # 列表bests中添加本轮的最优值
            bests.append(current_best)

        # 记录总演化时间
        end_time = time.process_time()
        # 结束上述所有轮运行，提示执行全局优化
        print('==== GLOBAL OPTIMUM ====')
        # 取bests列表中的最大值
        best = max(bests)
        decoding_array1 = best.root.decoding_index()
        decoding_array2 = best.root.decoding_operation()
        decoding_array3 = best.root.left.string()
        decoding_array4 = best.root.right.string()
        # 输出heuristic数据表格
        df1 = pd.DataFrame({"Type": ['Index array', 'Operations array', 'Routing heuristic', 'Sequencing heuristic'],
                           "Value": [decoding_array1, decoding_array2, decoding_array3, decoding_array4]})
        # 生成调度表
        data_jobs = []
        for i in range(len(best.draw_value)):
            data_job = []
            for j in best.draw_key[i]:
                data_job.append(j)
            for j in best.draw_value[i]:
                data_job.append(j)
            data_jobs.append(data_job)
        df2 = pd.DataFrame(data_jobs)
        df2.rename(columns={0: 'Job index', 1: 'Operation index', 2: 'Station index', 3: 'Start time', 4: 'Finish time',
                            5: 'Process time', 6: 'Setup time'}, inplace=True)
        df2 = df2.sort_values(by='Job index', ascending=True)
        with pd.ExcelWriter(os.getcwd() + '\\heuristic.xlsx') as writer:
            # df1.to_excel(writer, sheet_name='Heuristic', index=False)
            df2.to_excel(writer, sheet_name='Schedule', index=False)

        # 输出最优值的适应度和根字符
        print('best fitness: {}\nbest objective: {}'
              '\n(Min-based)heuristic-routing: {}\n(Min-based)heuristic-sequencing: {}'.
              format(best.fitness, best.objective,
                     best.root.left.string(), best.root.right.string()))
        # 输出目标函数值
        print('total process time: {}\ntotal due time: {}\nmakespan: {}'.
              format(best.total_process_time, best.total_due_time, best.makespan))
        # 输出最优值的stats
        print('stats: {{{}, total set time: {}, time cost: {}}}'.
              format(best.stats, best.total_transtime, round(end_time-start_time, 5)))

        self.time_cost = round((end_time-start_time)/RUNS, 4)
        # # 输出进化过程图
        # Plot.plt_evolve(self, generations, data_avg, data_best)
        # 输出最优方案的甘特图
        Plot.plt_gantt(best, self.number)
