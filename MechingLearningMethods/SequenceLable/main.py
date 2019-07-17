# _*_coding: utf-8_*_
"""
    @describe:
    @author: xuemingQiu
    @date 19-7-17
"""

from data_helper import *
from lstmmodel import train

if __name__ == '__main__':
    get_train_lable()
    train()
