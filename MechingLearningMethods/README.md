# 该目录主要用来实现机器学习的相关的方法

# 环境
     python 3.6  
     torch 1.1.0
     torchvision 0.3.0
     gensim 3.7.3
     

## SequenceLable文件夹 
- 描述  
     该目录实现的是序列标注的问题  
- 文件介绍   
     - settings.py:  包含文件基本的路径和模型的基本的参数
     - data_helper.py: 主要预处理训练数据，预处理数据格式见testDetas/Sequencelable_train.txt  
         + def get_train_lable(): 将训练数据切成数据和词性两个文件，分别为 train_data.txt文件和train_lable.txt文件  
         return train_data,lable 均为二维数组，一行代表一个文本，一行代表每个单词的lable
     - lstmmodel.py: 双向的lstm网路搭建代码
         + class LSTMTagger(nn.Module)  : 构建模型的类,继承了pytorch的神经网络的累
         + def train()  : 训练的函数
         + def predict(test_data): 预测函数，test_data为二维list,每行为代表分好词的文本
           return： 二维list,每行为每个单词对应的tag 
     - main.py：整个模型的程序入口，如果出错，请建立相对的目录即可
     
- 训练文件介绍
     Sequencelable_train.txt： 一行代表一个文本，数字类似与汉字，每个字的词性用了/a,/b,/c等来表示，字与字之间用下划线隔开来
     
