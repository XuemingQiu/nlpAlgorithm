# _*_coding: utf-8_*_
"""
    @describe:
    @author: xuemingQiu
    @date 3/28/19
"""
import random


class modelLDA:
    """
     输入：文档集(分词后)，K(主题数)，α，β，iter_number(迭代次数)
     输出：θmat(doc->topic)和mat(topic->word)、tassign文件(topic assignment）
    """
    
    def __init__(self, doc_set, doc_dic, K, alpha, beta, iter_number):
        """
        :param doc_set: 文档集合
        :param doc_dic: 文档字典
        :param K: 整体个数
        :param alpha: 超参数alpha
        :param beta: 超参数beta
        :param iter_number: 迭代次数
        nw[][]:number of instances of word/term i assigned to topic j,
        size V x K,V文档字典大小，K是主题个数
        nwsum[]:total number of words assigned to topic j，size K
        nd[][]:第i篇文档里被指定第j个主题词的次数， size M x K，M是文档数目
        ndsum[]:total number of words in document i，size M
        z[][]: 是int二维数组，topic assignment for each word，
               size M x per_doc_word_len表示第m篇文档第n个word被指定的topic index
        """
        self.K = K  # K个主题
        self.M = len(doc_set)  # 文档数
        self.V = len(doc_dic)  # 文档单词总数
        self.doc_set = doc_set  # 文档集合
        self.doc_dic = list(doc_dic)  # 文档字典集合
        self.alpha = alpha
        self.beta = beta
        self.item_number = iter_number
        self.p = []  # double类型
        self.Z = []  # M*doc.size()，文档中词的主题分布
        self.nw = []  # V*K，词i在主题j上的分布
        self.nwsum = []  # K，属于主题i的总词数
        self.nd = []  # M*K，文章i属于主题j的词个数
        self.ndsum = []  # M，文章i的词个数
        self.theta = []  # 文档-主题分布  大小:M*K
        self.phi = []  # 主题-词分布 大小:K*V
    
    # 初始化变量
    def initial(self):
        self.nw = [[0 for y in range(self.K)] for x in range(self.V)]
        self.nwsum = [0 for x in range(self.K)]
        self.nd = [[0 for y in range(self.K)] for x in range(self.M)]
        self.ndsum = [0 for x in range(self.M)]
        self.Z = [[] for x in range(self.M)]
        
        for m in range(self.M):
            self.Z[m] = [0 for y in range(len(self.doc_set[m]))]
            for n in range(len(self.doc_set[m])):
                topic_index = random.randint(0, self.K - 1)
                self.Z[m][n] = topic_index
                wordid = self.doc_dic.index(self.doc_set[m][n])
                self.nw[wordid][topic_index] += 1
                self.nwsum[topic_index] += 1
                self.nd[m][topic_index] += 1
                self.ndsum[m] += 1
        self.theta = [[0.0 for y in range(self.K)] for x in range(self.M)]
        self.phi = [[0.0 for y in range(self.V)] for x in range(self.K)]
    
    def ldaIteration(self):
        for iter in range(self.item_number):
            print(str(iter) + "次")
            for m in range(self.M):
                for n in range(len(self.doc_set[m])):
                    t = self.Z[m][n]
                    wordid = self.doc_dic.index(self.doc_set[m][n])
                    self.nw[wordid][t] -= 1
                    self.nwsum[t] -= 1
                    self.nd[m][t] -= 1
                    self.p = [0.0 for x in range(self.K)]
                    for k in range(self.K):
                        self.p[k] = (self.nw[wordid][k] + self.beta) / (self.nwsum[k] + self.V * self.beta)
                        self.p[k] *= ((self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha))
                    new_t = self.cumulative()
                    self.nw[wordid][new_t] += 1
                    self.nwsum[new_t] += 1
                    self.nd[m][new_t] += 1
                    self.Z[m][n] = new_t
        # 获取theta
        self.gettheta()
        # 获取phi
        self.getphi()
    
    def gettheta(self):
        for m in range(self.M):
            for k in range(self.K):
                self.theta[m][k] = (self.nd[m][k] + self.alpha) / (self.ndsum[m] + self.K * self.alpha)
    
    def getphi(self):
        for k in range(self.K):
            for v in range(self.V):
                self.phi[k][v] = (self.nw[v][k] + self.beta) / (self.nwsum[k] + self.V * self.beta)
    
    # 累积函数，计算p函数
    def cumulative(self):
        index = 1
        for index in range(1, len(self.p)):
            self.p[index] += self.p[index - 1]
        u = random.random() * self.p[-1]
        for index in range(0, len(self.p) - 1):
            if self.p[index] > u:
                break
        return index
    
    # 保存输出结果
    def save(self):
        # 保存phi文件，代表：每个主题下的单词概率文件大小K*V
        filename = "topic-word-phi" + str(self.K) + ".txt"
        ff = open(filename, "w", encoding="utf-8")
        for k in range(self.K):
            temp_word_probility = {}
            for v in range(self.V):
                temp_word_probility[self.doc_dic[v]] = self.phi[k][v]
            temp_word_probility = sorted(temp_word_probility.items(), key=lambda x: x[1], reverse=True)
            for i in range(10):
                tmp = temp_word_probility[i][0] + ":" + str(float(temp_word_probility[i][1]) * 100)[:5] + ";  "
                ff.write(tmp)
            ff.write("\n")
        ff.close()
        
        # 保存theta文件，代表每个文档的在主题下的个概率
        filename = "doc-topic-theta" + str(self.K) + ".txt"
        ff = open(filename, "w", encoding="utf-8")
        for doc in range(self.M):
            for k in range(self.K):
                ff.write(str(self.theta[doc][k])[:4] + " ")
            ff.write("\n")
        
        ff.close()


def get_raw_main():
    K = 5
    alpha = 0.2
    beta = 0.2
    item_number = 10
    filePath = "testDatas/ldatest.txt"
    import dataHelper
    doc_set = dataHelper.TextOp().textReader(filePath)
    doc_set = [line.strip().split(" ") for line in doc_set]
    print(doc_set[:10])
    doc_dic = []
    for line in doc_set:
        for a in line:
            doc_dic.append(a)
    doc_dic = set(doc_dic)
    print(doc_dic)
    print("主题个数为K=", K)
    ldamodel = modelLDA(doc_set, doc_dic, K, alpha, beta, item_number)
    ldamodel.initial()
    print("初始化完毕，开始迭代")
    ldamodel.ldaIteration()
    ldamodel.save()


# 用来测试程序
if __name__ == "__main__":
    get_raw_main()
