#coding=utf-8

DATA_DIR = '../data/'
# 线下调试模型所用数据文件的位置
OFF_LINE = '../data/offline/'
# 小样本位置
SAMPLES_DIR = '../data/offline/samples/'
# 分解后的行文数据文件
PARTS_DIR = '../data/parts/'

# 原始数据文件
TRAIN_ITEM = '../data/tianchi_mobile_recommend_train_item.csv'
TRAIN_USER = '../data/tianchi_mobile_recommend_train_user.csv'

# 提交文件名
PREDICT = '../data/tianchi_mobile_recommendation_predict.csv'

# 按照用户名和时间排序后的原始数据文件
TRAIN_USER_SORTED = '../data/tianchi_mobile_recommend_train_user_sorted.csv'
TRAIN_USER_PARTS = '../data/parts/part_%d.csv'
FEATURE = '../data/feature.csv'

# 线下调试模型所用的原始训练集和结果集
TRAN_USER_OFFLINE = '../data/offline/train_user.csv'
LABEL_OFFLINE = '../data/offline/label.csv'
ANSWER_OFFLINE = '../data/offline/answer.csv'
FEATURE_OFFLINE = '../data/offline/feature.csv'

# 小样本文件名
TRAIN_USER_SAMPLES = '../data/offline/samples/train_user_%d.csv'
LABEL_SAMPLES = '../data/offline/samples/label_%d.csv'
ANSWER_SAMPLES = '../data/offline/samples/answer_%d.csv'
PREDICT_SAMPLES = '../data/offline/samples/predict_%d.csv'
FEATURE_SAMPLES = '../data/offline/samples/feature_%d.csv'

# 需要进行的动作

import os

dirs = [DATA_DIR, OFF_LINE, SAMPLES_DIR, PARTS_DIR]
for d in dirs:
    if not os.path.isdir(d):
        os.mkdir(d)

