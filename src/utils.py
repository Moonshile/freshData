#coding=utf-8

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

def write_to_csv(path, head, data):
    with open(path, 'w') as f:
        f.write(','.join(head) + '\n')
        for d in data:
            f.write(','.join(d) + '\n')

# 以answers为准计算predicts的F1值
def compute_f1(predicts, answers):
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
