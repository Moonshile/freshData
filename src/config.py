#coding=utf-8

# 原始数据文件
TRAIN_ITEM = '../data/tianchi_mobile_recommend_train_item.csv'
TRAIN_USER = '../data/tianchi_mobile_recommend_train_user.csv'

# 按照用户名和时间排序后的原始数据文件
TRAIN_USER_SORTED = '../data/tianchi_mobile_recommend_train_user_sorted.csv'

# 线下调试模型所用数据文件的位置
DATA_DIR = '../data/'
OFF_LINE = '../data/offline/'







# 需要进行的动作

import os

dirs = [DATA_DIR, OFF_LINE]
for d in dirs:
    if not os.path.isdir(d):
        os.mkdir(d)

