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

# 预训练的词向量的路径
# 这里是利用gensim进行训练的，通过numpy进行保存的，可以换成其他预训练的，但是在读取的时候需要改动。
word_embeding_path = os.path.join(path, "model/word_embedding.npy")

# 双向的lstm模型的参数设置
input_size = 300  # 也是word_embedding词向量的维度
hidden_size = 128  # 隐藏层的单元个数
num_layers = 5  # 有5层隐藏层
num_epochs = 5  # 训练迭代轮数
learning_rate = 0.001  # 学习率
# 模型的输出路径
output_model_path = os.path.join(path, "model/lstmmodel")
