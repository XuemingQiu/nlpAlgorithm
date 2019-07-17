# _*_coding: utf-8_*_
"""
    @describe:
    @author: xuemingQiu
    @date 19-7-17
"""
from settings import *

__all__ = ['get_train_lable']


def get_train_lable():
    """
    将 train.txt文件解析成  train_data.txt文件和train_lable.txt文件
    :return: (data,lable)
    """
    data = []
    lable = []
    with open(train_path, "r") as f:
        for line in f.readlines():
            temp = line.strip().replace('  ', '_').split('_')
            line_data = []
            line_lable = []
            for w in temp:
                if w == ' ':
                    continue
                line_data.append(w.split('/')[0])
                if len(w.split('/')) > 1:
                    line_lable.append(w.split('/')[1])
                else:
                    line_lable.append('#')
            data.append(' '.join(line_data))
            lable.append(' '.join(line_lable))
    saveTrainData(data, lable)
    return data, lable


def saveTrainData(data, lable):
    train_data, train_lable = data, lable
    # print(len(train_data[0].split(' ')), len(train_lable[0].split(' ')))
    with open(train_data_path, "w") as f:
        for line in train_data:
            f.write(line + "\n")
    with open(train_lable_path, "w") as f:
        for line in train_lable:
            f.write(line + "\n")


if __name__ == '__main__':
    get_train_lable()
