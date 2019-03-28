## 该项目只要总结自己在研究生阶段项目开发中应用到的部分常用的代码 
     主要包含了：数据挖掘和自然语言处理的算法，还有机器学习的代码等等......

# 1. dataHelper.py:常见的数据处理的函数\
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






