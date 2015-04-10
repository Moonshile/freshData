#coding=utf-8

import os

from config import TRAIN_USER, TRAIN_USER_SORTED
from utils import read_from_csv, write_to_csv, sort_raw_data

# 根据用户名、时间对原始数据集进行排序
def sort_train_user():
    (head, data) = read_from_csv(TRAIN_USER)
    data_sorted = sort_raw_data(data)
    write_to_csv(TRAIN_USER_SORTED, head, data)

sort_train_user()
