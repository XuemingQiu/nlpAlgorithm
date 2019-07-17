# _*_coding: utf-8_*_
"""
    @describe: 用来搭建模型
    @author: xuemingQiu
    @date 19-7-17
"""
# 设置用不用gpu加速
# os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import random

import numpy
import torch
import torch.nn as nn  # 神经网络模块
import torch.nn.functional as F  # 神经网络模块中的常用功能
from torch import autograd, optim

from settings import *

__all__ = ['LSTMTagger', 'train', 'predict']
use_gpu = torch.cuda.is_available()
print("used gpu = ", use_gpu)

torch.manual_seed(1)


def get_data():
    """
    读取data_helper解析好的数据
    :return:
    """
    data = []
    lable = []
    with open(train_data_path, "r") as f:
        for line in f.readlines():
            data.append(line.strip().split())
    with open(train_lable_path, "r") as f:
        for line in f.readlines():
            lable.append(line.strip().split())
    train_result = []
    for i in range(len(data)):
        assert len(data[i]) == len(lable[i])
        train_result.append((data[i], lable[i]))
    return train_result


# 获取数据
training_data = get_data()
# 构建单词索引字典
word_to_ix = {}  # 单词的索引字典
for sent, tags in training_data:
    for word in sent:
        if word not in word_to_ix:
            word_to_ix[word] = len(word_to_ix)
# 手工设定词性标签数据字典
tag_to_ix = {'a': 0, 'b': 1, 'c': 2, 'o': 3, '#': 4}

# 加载与训练的词向量
word_embedding_dict = numpy.load(word_embeding_path, allow_pickle=True).item()

# 随机初始化词向量
init = [random.random() for i in range(200)]
word_embedding = [init for i in range(len(word_to_ix) + 1)]

for w, ix in word_to_ix.items():
    try:
        word_embedding[ix] = word_embedding_dict[w]
    except:
        continue
weights = numpy.array(word_embedding, dtype='float32')


class LSTMTagger(nn.Module):
    
    def __init__(self, input_size, hidden_dim, vocab_size, tagset_size):
        super(LSTMTagger, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers
        self.weights = weights
        self.word_embeddings = nn.Embedding.from_pretrained(torch.from_numpy(self.weights))
        
        self.lstm = nn.LSTM(input_size, hidden_dim, num_layers, dropout=0.3, bidirectional=True)
        
        self.hidden2tag = nn.Linear(hidden_dim * 2, tagset_size)
        self.hidden = self.init_hidden()
    
    def init_hidden(self):
        if use_gpu:
            return (autograd.Variable(torch.zeros(self.num_layers * 2, 1, self.hidden_dim)).cuda(),
                    autograd.Variable(torch.zeros(self.num_layers * 2, 1, self.hidden_dim)).cuda())
        else:
            (autograd.Variable(torch.zeros(self.num_layers * 2, 1, self.hidden_dim)),
             autograd.Variable(torch.zeros(self.num_layers * 2, 1, self.hidden_dim)))
    
    def forward(self, x):
        self.init_hidden()
        embeds = self.word_embeddings(x)
        lstm_out, _ = self.lstm(embeds.view(len(x), 1, -1))
        tag_space = self.hidden2tag(lstm_out.view(len(x), -1))
        tag_scores = F.log_softmax(tag_space)
        return tag_scores


def prepare_sequence(seq, to_ix):
    """
    :param seq: 句子list
    :param to_ix: 索引，单词索引或者lable索引
    :return: 一个tensor
    """
    idxs = [to_ix[w] for w in seq]
    tensor = torch.LongTensor(idxs)
    if use_gpu:
        tensor = tensor.cuda()
    return autograd.Variable(tensor)


def train():
    model = LSTMTagger(input_size, hidden_size, len(word_to_ix), len(tag_to_ix))
    if use_gpu:
        model = model.cuda()  # torch.load(output_model_path + 'gpu')
    # else:
    #     model = torch.load(output_model_path)
    loss_function = nn.NLLLoss()
    optimizer = optim.SGD(model.parameters(), lr=learning_rate)
    if use_gpu:
        model = model.cuda()
        loss_function = loss_function.cuda()
    all_length = 0
    for sentence, tags in training_data:
        all_length += len(sentence)
    print("all length = ", all_length)
    
    for epoch in range(num_epochs):  # 我们要训练300次，可以根据任务量的大小酌情修改次数。
        right = 0
        process = 0
        for sentence, tags in training_data:
            if process % 2000 == 0:
                print("epoch ", epoch, " : processs = ", process * 1.0 / len(training_data))
            process += 1
            # 清除网络先前的梯度值，梯度值是Pytorch的变量才有的数据，Pytorch张量没有
            model.zero_grad()
            # 准备网络可以接受的的输入数据和真实标签数据，这是一个监督式学习
            sentence_in = prepare_sequence(sentence, word_to_ix)
            targets = prepare_sequence(tags, tag_to_ix)
            if use_gpu:
                setence_in = sentence_in.cuda()
                targets = targets.cuda()
            # 运行我们的模型，直接将模型名作为方法名看待即可
            tag_scores = model(sentence_in)
            
            outputs = torch.argmax(tag_scores, 1).tolist()
            for pre, tg in zip(outputs, targets):
                if pre == tg:
                    right += 1
            # 计算损失，反向传递梯度及更新模型参数
            loss = loss_function(tag_scores, targets)
            loss.backward()
            optimizer.step()
        print("epoch", epoch, ": accur = ", right * 1.0 / all_length)
    if use_gpu:
        torch.save(model, output_model_path + 'gpu')
    else:
        torch.save(model, output_model_path)


def predict(test_data):
    """
    :param test_data: 一个需要预测的二维数组，一行一个文本
    :return:
    """
    if use_gpu:
        model = torch.load(output_model_path + 'gpu')
    else:
        model = torch.load(output_model_path)
    results = []
    print("test data length == ", len(test_data))
    for dt in test_data:
        inputs = prepare_sequence(dt, word_to_ix)
        tag_scores = model(inputs)
        outputs = torch.argmax(tag_scores, 1).tolist()
        results.append(outputs)
    return results
