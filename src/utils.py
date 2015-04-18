#coding=utf-8

from datetime import datetime, timedelta
from heapq import heappush, heappop

from config import TRAIN_ITEM

def time2str(time):
    return datetime.strftime(time, '%Y-%m-%d %H')

def str2time(str):
    return datetime.strptime(str, '%Y-%m-%d %H')

def str_timedelta_hours(s1, s2):
    delta = str2time(s1) - str2time(s2)
    return delta.days*24 + delta.seconds/3600

def read_from_csv(path, func=lambda x: x.strip().split(',')):
    res = []
    head = None
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('user_id'):
                head = func(line)
                continue
            res.append(func(line))
    return (head, res)

def write_to_csv(path, head, data, func=lambda x: ','.join(x) + '\n'):
    with open(path, 'w') as f:
        f.write(func(head))
        for d in data:
            f.write(func(d))

# 以answers为准计算predicts的F1值
def compute_f1(predicts, answers):
    if not predicts:
        return (0, 0, 0)
    intersec = float(len(set(predicts)&set(answers)))
    p = intersec/len(predicts)
    r = intersec/len(answers)
    f1 = 2*p*r/(p + r) if intersec else 0.
    return (p, r, f1)

# 以answer_file文件为准计算predict_file文件的F1值
def check(predict_file, answer_file):
    (head_t, predicts) = read_from_csv(predict_file, func=lambda x:x)
    (head_a, answers) = read_from_csv(answer_file, func=lambda x:x)
    return compute_f1(predicts, answers)

# 根据用户名、时间对用户行为数据集进行排序
def sort_raw_data(data):
    return sorted(data, 
        cmp=lambda x, y: cmp(x[-1], y[-1]) if cmp(x[0], y[0]) == 0 else cmp(x[0], y[0])
    )

# 获取目标Item子集
def retrieve_item_ids():
    (head, items) = read_from_csv(TRAIN_ITEM,
        func=lambda x: x.split(',')[0]
    )
    return set(items)

# 寻找最好的阈值，返回该阈值和结果集
def find_theta(X, y, answers, item_ids, quiet=True):
    thetas = map(lambda x: .01*x, range(0, 101))
    max_f1 = -1
    max_theta = None
    pre_res = None
    for theta in thetas:
        predict = []
        for i in range(0, len(X)):
            if y[i] > theta and str(X[i][1]) in item_ids:
                predict.append(','.join(map(lambda x : str(x), X[i][:2])))
        (p, r, f1) = compute_f1(predict, answers)
        if f1 > max_f1:
            max_f1 = f1
            max_theta = theta
            pre_res = predict
            if not quiet:
                print 'Size: %d; scores: (%4f, %4f, %4f)'\
                    % (len(predict), p, r, f1)
        if len(predict) == 0:
            break
    return max_theta, pre_res

# 使用堆排序选择得分最高的N个记录
class TopResult(object):

    def __init__(self, size):
        super(TopResult, self).__init__()
        self.size = size
        self.heap = []

    def push(self, x):
        to_push = x
        if len(self.heap) == self.size:
            x_min = self.pop()
            if cmp(x_min, x) >= 0:
                to_push = x_min
        heappush(self.heap, to_push)

    def pop(self):
        heappop(self.heap)

    def get(self):
        return self.heap

    def push_many(self, X, y):
        for i in range(0, len(y)):
            element = (y[i], X[i])
            self.push(element)

    def get_many(self):
        res = []
        for (y, x) in self.heap:
            res.append(x)
        return res

# 返回得分最高的一定比例的数据
def cut_with_count(X, y, item_ids, count):
    heap = TopResult(count)
    for i in range(0, len(X)):
        if str(X[i][1]) in item_ids:
            heap.push((y[i], ','.join(map(lambda x : str(x), X[i][:2]))))
    return heap.get_many()

# 以一定的权重融合多个模型
class Chaos(object):

    def __init__(self, X):
        super(Chaos, self).__init__()
        self.X = X
        self.ys = []

    def add_y(self, weight, y):
        self.ys.append((weight, y))

    def get(self, item_ids, cut=0.001):
        merged_y = None
        for w, y in self.ys:
            if not merged_y:
                merged_y = [0.]*len(y)
            for i in range(0, len(y)):
                merged_y[i] += w*y[i]
        return cut_with_count(self.X, y, item_ids, cut)


