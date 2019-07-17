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
     - data_helper.py: 主要预处理训练数据，预处理数据格式见testDetas/Sequencelable_train.txt  
         + def get_train_lable(): 将训练数据切成数据和词性两个文件，分别为 train_data.txt文件和train_lable.txt文件  
         return train_data,lable 均为二维数组，一行代表一个文本，一行代表每个单词的lable
              

- 训练文件介绍
     Sequencelable_train.txt： 一行代表一个文本，数字类似与汉字，每个字的词性用了/a,/b,/c等来表示，字与字之间用下划线隔开来
     
