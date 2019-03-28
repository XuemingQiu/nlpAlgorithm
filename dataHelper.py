# _*_coding: utf-8_*_
"""
    @describe:
    @author: xuemingQiu
    @date 3/25/19
"""
import csv
import os

import cx_Oracle
import phoenixdb


class CsvOp:
    """
    1. 用来读去csv文件
    """
    
    def __init__(self):
        pass
    
    def csvReader(self, filePath):
        """
        :param filePath: 文件路径
        :return: 返回[[a,b,c...],[c,d,e..],[]]
        """
        dataset = []
        try:
            f = open(filePath)
            for line in csv.reader(f):
                dataset.append(line)
        except:
            print("the file is not exist or the file's content is wrong!")
        return dataset


class TextOp:
    """
    2. 读取文本文件txt
    """
    
    def __init__(self):
        pass
    
    def textReader(self, filePath):
        """
        :param filePath: 文件路径
        :return: [line1,line2.....]
        """
        datasets = []
        with open(filePath, "r") as f:
            for lines in f.readlines():
                datasets.append(lines.strip())
        return datasets


class OracleOp:
    
    def __init__(self, HOSTNAME, PORT, DATABASE_NAME, USER_NAME, PASSWORD):
        self.hostname = HOSTNAME
        self.port = PORT
        self.sid = DATABASE_NAME
        self.username = USER_NAME
        self.password = PASSWORD
    
    def getConn(self):
        os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'  # 解决乱码问题：
        dsn = cx_Oracle.makedsn(self.hostname, self.port, self.sid)
        conn = cx_Oracle.connect(self.username, self.password, dsn)
        cursor = conn.cursor()  # 返回连接的游标对象
        # print()
        return conn, cursor
    
    # 读取数据库
    def readOracle(self, conn, cursor, sql):
        cursor.execute(sql)
        result = cursor.fetchall()
        conn.commit()
        return result
    
    # 写入数据库 格式要求  dataList = [{字典数据},{}.....]
    def writeOracle(self, conn, cursor, sql, dataList):
        cursor.prepare(sql)
        cursor.executemany(None, dataList)
        conn.commit()
    
    # 更新操作
    def updateOracle(self, conn, cursor, sql):
        cursor.execute(sql)
        conn.commit()
    
    #  关闭连接
    def close(self, conn, cursor):
        cursor.close()
        conn.close()


class HbaseOp:
    """
     主要是通过phoenix读取hbase数据
     phoenix是一个将hbase抽象成oracle的插件，sql语句和oracel类似
    """
    
    def getConn(self, DATABASE_URL):
        """
        :param DATABASE_URL:phoenix 服务的地址 ，记得启动phoenix的querysever.py 服务
        :return:
        """
        conn = phoenixdb.connect(DATABASE_URL, autocommit=True)
        cursor = conn.cursor()
        return conn, cursor
    
    def upSert(self, conn, cursor, sql, data=None):
        """
        :param conn:
        :param cursor:
        :param sql: 插入或者更新语句
        :param data: 数据为空，即是更新操作
        :return:
        """
        if data is None:
            # update datas
            cursor.execute(sql)
        else:
            # insert the datas
            cursor.executemany(sql, data)
    
    def search(self, conn, cursor, sql):
        cursor.execute(sql)
        return cursor.fetchall()
    
    def close(self, conn, cursor):
        cursor.close()
        conn.close()


if __name__ == '__main__':
    # csv 测试
    # csvop = CsvOp()
    # print(csvop.csvReader("test.csv")[:10])
    
    # txt 测试
    # textop = TextOp()
    # print(textop.textReader("a.txt")[:10])
    
    '''oracle 测试
    读数据库设置'''
    # READ_HOSTNAME = "localhost"
    # READ_PORT = "1521"
    # READ_DATABASE_NAME = "orcl"
    # READ_USERNAME = "epoint"
    # READ_PASSWORD = "11111"
    # CASE_INFO_TABLE_NAME = "CASE_INFO"
    # oracle = OracleOp(READ_HOSTNAME, READ_PORT, READ_DATABASE_NAME, READ_USERNAME, READ_PASSWORD)
    # sql = "select * from {}".format(CASE_INFO_TABLE_NAME)
    # conn, cursor = oracle.getConn()
    # result = oracle.readOracle(conn, cursor, sql)  # [(*,*,* ....),()]
    # oracle.close(conn, cursor)
    
    # 测试hbase读取
    DATABASE_URL = "http://linux:8765"
    hb = HbaseOp()
    conn, cursor = hb.getConn(DATABASE_URL)
    sql = "select COUNT(*) from CASE_INFO"
    result2 = hb.search(conn, cursor, sql)
    print(result2
          
          
          
          
          )
    hb.close(conn, cursor)
