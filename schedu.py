import datetime
import sched
import time
from threading import Timer


def run():
    print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


# 设置时间调度器
# 注意 sched 模块不是循环的，一次调度被执行后就结束了，如果想再执行，请再次 enter
scheduler = sched.scheduler(time.time, time.sleep)
# 延后1天的凌晨0点
timestamp = (datetime.datetime.now() + datetime.timedelta(days=1)).replace(
    hour=0, minute=6, second=0, microsecond=0).timestamp()
# 设置运行时间
scheduler.enterabs(timestamp, 0, run)
# 四个参数分别为：间隔事件、优先级（用于同时间到达的两个事件同时执行时定序）、被调用触发的函数，给该触发函数的参数（tuple形式）
scheduler.enter(0, 0, run)  # 提交拉取的内核
# 运行函数
scheduler.run()

##########################

# 第一个参数是时间间隔（单位是秒，只有秒），第二个参数是要调用的函数名，第三个参数是调用函数的参数(tuple)
t = Timer(6, run, (1,))
t.start()
