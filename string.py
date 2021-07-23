import random

# 随机大于0 且小于1 之间的小数
random.random()
# 随机一个大于0小于9的小数
random.uniform(0, 9)

# 随机一个大于等于1且小于等于5的整数
random.randint(1, 5)
# 随机一个大于等于1且小于等于10之间的奇数，其中2表示递增基数
random.randrange(1, 10, 2)

# 随机返回参数列表中任意一个元素
random.choice(['123', 'abc', 52, [1, 2]])
# 随机返回参数列表中任意两个元素，参数二指定返回的数量
random.sample(['123', 'abc', 52, [1, 2]], 2)

# 打乱列表顺序
random.shuffle([1, 2, 5, 7, 9, 10])
