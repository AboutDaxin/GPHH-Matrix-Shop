# 定义任务类
class Task:
    # 初始化方法，定义任务层的一些属性，初始化为0
    def __init__(self, num=0, process=None, exec_time=None, release=0, deadline=0, weight=1):
        self.num = num
        self.process = process
        self.process_num = [i+1 for i in range(len(process))]
        self.release = release
        self.deadline = deadline
        self.weight = weight
        self.exec_time = exec_time
        self.priority = None
        self.need_popped = True

    # 富比较方法，当实例被用于比较大小时，以priority属性值比较进行代替（lt方法正常用小于号写返还值）
    def __lt__(self, other):
        return self.priority < other.priority


# 定义工位类
class Station:
    def __init__(self, num=0, capacity=None, set_time=0):
        self.num = num
        self.capacity = capacity
        self.current_capacity = 0
        self.set_time = set_time
        self.current_trans_time = 0
        self.have_trans = False
        self.queue = []
        self.priority = None
        self.have_popped = False

    # 富比较方法，当实例被用于比较大小时，以priority属性值比较进行代替（lt方法正常用小于号写返还值）
    def __lt__(self, other):
        return self.priority < other.priority


# 定义作业类（一个task在station执行时作为一个job）
class Job:
    # 初始化方法，定义作业层的一些属性（：Task为声明task的类型，有没有无所谓）
    def __init__(self, task: Task, station: Station, time):
        self.task = task
        self.station = station
        self.num = task.num
        # job剩余执行时间
        self.exec_time = task.exec_time[0] if len(task.exec_time) != 0 else 0
        # job释放时间是当前时间
        self.release = time
        self.priority = None
        self.has_run = False

    # 富比较方法
    def __lt__(self, other):
        # 若两个作业优先级相同，自身在运行而另一个没运行，则self排在前边
        if self.priority == other.priority and self.has_run is True and other.has_run is False:
            return True
        # 否则将值小的排前边（lt方法正常使用小于号）
        else:
            return self.priority < other.priority


# 定义问题类
class Problem:
    def __init__(self, tasks, stations, hyper_period=0):
        # 实例化时时，tasks是个列表
        self.tasks = tasks
        self.stations = stations
        self.hyper_period = hyper_period
