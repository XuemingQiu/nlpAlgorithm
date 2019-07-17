# _*_coding: utf-8_*_
"""
    @describe: 用来设置模型的参数，以及训练文件的路劲
    @author: xuemingQiu
    @date 19-7-17
"""
import os

# base path
path = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

# 训练路径
train_path = os.path.join(path, "testDatas/Sequencelable_train.txt")

# data_helper.py文件解析后保存的路径
train_data_path = os.path.join(path, "testDatas/train_data.txt")
train_lable_path = os.path.join(path, "testDatas/train_lable.txt")

# 模型参数
output_model_path = os.path.join(path, "model/lstmmodel")
