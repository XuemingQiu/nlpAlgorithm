## 该项目只要总结自己在研究生阶段项目开发中应用到的部分常用的代码 
     主要包含了：数据挖掘和自然语言处理的算法，还有机器学习的代码等等......
# 环境说明：
     python 3.7.6
    
# 传统自然语言处理算法 
 1. dataHelper.py:常见的数据处理的函数
     1>. csv文件读取类: CsvOp类     
     参数：文件地址      
     返回值：[[],[].....]    
     用法：     
            csvop = CsvOp()  
            print(csvop.csvReader("test.csv")[:10])  
  
    2>. txt文件读取类 TextOp类：     
    参数：文件地址  
    返回值：[line1,line2.....]  
    用法：  
            textop = TextOp()  
            print(textop.textReader("a.txt")[:10])  
    3>. oracle数据库读取类：OracleOp类  
    类说明：  
            def __init__(HOSTNAME, PORT, DATABASE_NAME, USER_NAME, PASSWORD): #初始化数据库，如用法介绍  
            def getConn(): #获得连接和游标  
            def readOracle(conn,cursor,sql): #读取数据，返回[(),(),()....]  
            def writeOracel(conn,cursor,sql,dataList): #写入数据库，dataList为[{},{}..]  
            def updateOracle(conn,cursor,sql): #更新数据库  
            def close(conn,sursor): #关闭数据库连接   
    用法:     
            READ_HOSTNAME = "localhost"   
            READ_PORT = "1521"  
            READ_DATABASE_NAME =  "orcl"  
            READ_USERNAME = "xueming"  
            READ_PASSWORD = "****"  
            CASE_INFO_TABLE_NAME = "CASE_INFO"  
            oracle = OracleOp(READ_HOSTNAME, READ_PORT, READ_DATABASE_NAME, READ_USERNAME, READ_PASSWORD)  
            sql = "select * from {}".format(CASE_INFO_TABLE_NAME)    
            conn, cursor = oracle.getConn()      
            result = oracle.readOracle(conn, cursor, sql)  # [(*,*,* ....),()]    
            oracle.close(conn, cursor)    
    4>. hbase读取类：HbaseOp类:目前主要是通过phoenix读取hbase     
    类说明：   
            def getConn(DATABASE_URL): #phoenix 的服务器地址，返回conn，cursor  
            def upsert(conn,cursor,sql,data=None): #插入和更新语句，插入是data不为None,格式[(),()..]  
            def search(conn,cursor,sql): # 查询数据，返回[(),()]  
            def close(conn,cursor): #关闭连接  
    用法：      
            DATABASE_URL = "http://linux:8765"    
            hb = HbaseOp()    
            conn, cursor = hb.getConn(DATABASE_URL)     
            sql = "select COUNT(*) from CASE_INFO"      
            result2 = hb.search(conn, cursor, sql)      
            print(result2)    
2. apriori算法：关联规则挖掘算法 apriori.py  
	1>. 算法描述：找到所有大于等于支持度的频繁项集   
	    输入：datas = [  
                   ['1', '2', '3', '4', '5'],  
                   ['3', '2', '1'],  
                   ['1', '2', '3', '4'],  
                   ['5', '6', '7', '8'],  
                   ['1', '2', '5', '8']  
               ]  
           可以是这种格式的文件,需要自己写好读取函数  
        输出：  
             [('项集','支持度')......]  
	2>. 用法：见apriori.py文件      
	 
3. 朴素的LDA算法  
        算法描述： 无监督的概率主题模型，使用了Gibbs sampling  
        输入：已经分好词，去停词之后中文英文都可以，或者经过tfidf提取特征之后的单词文档是具体如testDatas/ldatest.txt  
        输出：主要有两个文件：  
                         文档和主题概率文档doc-topic-theta.txt  
                         主题和单词概率文件topic-word-phi.txt  
        类: modelLDA  
            def __init__(self, doc_set, doc_dic, K, alpha, beta, iter_number):  
                    """  
                    :param doc_set: 文档集合  
                    :param doc_dic: 文档字典  
                    :param K: 整体个数  
                    :param alpha: 超参数alpha  
                    :param beta: 超参数beta  
                    :param iter_number: 迭代次数  
                    """  
            def initial(self): # 初始化，  
            def ldaIteration(self): # 迭代  
            def gettheta(self): # 获得theta文件  
            def getphi(self): # 获得phi文件  
            def cumulative(self):  # 采样计算累计函数  
            def save(self): # 保存对应的两个相应的文件  
        用法：  
            参见lda.py文件  
        Tips：  
            对输出不满意可以重新输出保存，在phi文件是进行了排序之后输出的          

 # 深度学习，神经网络，机器学习算法     
  - 序列标注问题，见 MechingLearningMethods/SequenceLable/ 下的README.md
  



