#coding=utf-8

from datetime import datetime, timedelta

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

# 返回得分最高的一定比例的数据
def cut_with_count(X, y, item_ids, cut=0.001):
    predict = []
    for i in range(0, len(X)):
        if str(X[i][1]) in item_ids:
            predict.append([','.join(map(lambda x : str(x), X[i][:2])), y[i]])
    predict = sorted(predict, cmp=lambda x, y: cmp(y[1], x[1]))
    return map(lambda x: x[0], predict[:int(cut*len(predict))])
