#coding=utf-8

import os

from config import TRAIN_USER, TRAIN_USER_SORTED, TRAIN_USER_SAMPLES, ANSWER_SAMPLES
from utils import read_from_csv, write_to_csv, sort_raw_data

# 根据用户名、时间对原始数据集进行排序
# 对全部数据进行排序需要约5G的内存，小瘦机器请小心使用！！！
def sort_train_user():
    (head, data) = read_from_csv(TRAIN_USER)
    data_sorted = sort_raw_data(data)
    write_to_csv(TRAIN_USER_SORTED, head, data_sorted)

# 将数据集的最后一天作为线下的结果集合，假定已排序
def gen_offline(path_in, path_new_data, path_result):
    with open(path_in, 'r') as fin:
        with open(path_result, 'w') as ft:
            with open(path_new_data, 'w') as ff:
                for line in fin:
                    if line.strip().split(',')[-1].startswith('2014-12-18'):
                        ft.write(line)
                    else:
                        ff.write(line)

# 获取一个文件中所有的用户名
def users_of_file(path):
    (head, users) = read_from_csv(path, 
        func=lambda x: x.strip().split(',')[0]
    )
    return set(users)

# 将已经排序的样本按照每n条记录为一个样本分为几个小样本
def sample_users(n, path_in, path_train, path_result):
    from math import ceil
    sample_count = ceil(len(users_of_file(path_in))/float(n))
    pre_uid = '-------'
    cur_count = -1
    f_train = map(lambda x: open(path_train % x, 'w'), range(0, sample_count))
    f_res = map(lambda x: open(path_result % x, 'w'), range(0, sample_count))
    with open(path_in, 'r') as fin:
        for line in fin:
            # 第一行是表头
            if cur_count == -1:
                for f in f_train + f_res:
                    f.write(line)
                continue
            l = line.split(',')
            # 新的用户
            if not line.startswith(pre_uid):
                cur_count += 1
                pre_uid = l[0]
            # 根据时间分别存放
            if l[-1].startswith('2014-12-18'):
                f_res[cur_count/n].write(line)
            else:
                f_train[cur_count/n].write(line)
    for f in f_train + f_res:
        f.close()
