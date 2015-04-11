#coding=utf-8

import os

from config import TRAIN_USER, TRAIN_ITEM, TRAIN_USER_SORTED,\
    TRAIN_USER_SAMPLES, LABEL_SAMPLES, ANSWER_SAMPLES,\
    TRAN_USER_OFFLINE, LABEL_OFFLINE, ANSWER_OFFLINE,\
    TRAIN_USER_PARTS
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
        func=lambda x: x.split(',')[0]
    )
    return set(users)

# 将已经排序的样本按照每n条记录为一个样本分为几个小样本，并分为训练集和验证集
def sample_users_to_train_label(n, path_in, path_train, path_result, user_count=10000):
    from math import ceil
    sample_count = int(ceil(user_count/float(n)))
    pre_uid = '0000000000000000'
    cur_count = -2
    f_train = map(lambda x: open(path_train % x, 'w'), range(0, sample_count))
    f_res = map(lambda x: open(path_result % x, 'w'), range(0, sample_count))
    with open(path_in, 'r') as fin:
        for line in fin:
            # 第一行是表头
            if cur_count == -2:
                cur_count += 1
                for f in f_train + f_res:
                    f.write(line)
                continue
            l = line.split(',')
            # 新的用户
            if l[0] > pre_uid:
                cur_count += 1
                pre_uid = l[0]
            # 根据时间分别存放
            if l[-1].startswith('2014-12-18'):
                f_res[cur_count/n].write(line)
            else:
                f_train[cur_count/n].write(line)
    for f in f_train + f_res:
        f.close()

# 将已经排序的样本按照每n条记录为一个样本分为几个小样本
def sample_users(n, path_in, path_out, user_count=10000):
    from math import ceil
    sample_count = int(ceil(user_count/float(n)))
    pre_uid = '0000000000000000'
    cur_count = -2
    fout = map(lambda x: open(path_out % x, 'w'), range(0, sample_count))
    with open(path_in, 'r') as fin:
        for line in fin:
            # 第一行是表头
            if cur_count == -2:
                cur_count += 1
                for f in fout:
                    f.write(line)
                continue
            l = line.split(',')
            # 新的用户
            if l[0] > pre_uid:
                cur_count += 1
                pre_uid = l[0]
            fout[cur_count/n].write(line)
    for f in fout:
        f.close()

# 获取目标Item子集
def retrieve_item_ids():
    (head, items) = read_from_csv(TRAIN_ITEM,
        func=lambda x: x.split(',')[0]
    )
    return set(items)

# 统计给定文件中的曾经发生过购买的user-item对，并去重后保存
def label_to_ans(path_label, path_ans):
    items = retrieve_item_ids()
    pairs = set()
    with open(path_label, 'r') as f_label:
        for line in f_label:
            if line.startswith('user'):
                continue
            l = line.split(',')
            if l[2] == '4' and l[1] in items:
                pairs.add(','.join(l[:2]))
    write_to_csv(path_ans, 'user_id,item_id', pairs, func=lambda x: x + '\n')





import sys

SAMPLE_N = 10

def _help():
    print """
    -h\tFor help messages
    -a\tCast label datasets to answers
    -c\tCount users in the original train user dataset
    -s\tSort the original train user dataset by userid and time
    -m\tSample the sorted train user dataset to 10 small datasets, each contains 1000 user,
      \tand then divide each of them into train dataset and label dataset
    -d\tDivide the sorted train user dataset to 10 small datasets, each contains 1000 user,
      \tthen do nothing
    """

def _sample():
    sample_users_to_train_label(10000/SAMPLE_N, TRAIN_USER_SORTED, TRAIN_USER_SAMPLES, LABEL_SAMPLES)
    gen_offline(TRAIN_USER_SORTED, TRAN_USER_OFFLINE, LABEL_OFFLINE)

def _count():
    print len(users_of_file(TRAIN_USER_SORTED))

def _answer():
    for i in range(0, SAMPLE_N):
        label_to_ans(LABEL_SAMPLES % i, ANSWER_SAMPLES % i)
    label_to_ans(LABEL_OFFLINE, ANSWER_OFFLINE)

def _divide():
    sample_users(10000/SAMPLE_N, TRAIN_USER_SORTED, TRAIN_USER_PARTS)

switches = {
    '-h': _help,
    '-a': _answer,
    '-c': _count,
    '-s': sort_train_user,
    '-m': _sample,
    '-d': _divide,
}

if len(sys.argv) == 2:
    arg = sys.argv[1]
    f = switches.get(arg, _help)
    f()
else:
    _help()
