# _*_coding: utf-8_*_
"""
    @describe:
    @author: xuemingQiu
    @date 3/25/19
"""

# the minimal support
minSupport = 0.8


def getApriori(datas):
    """
        data sample:
        one line present a transactions just divide by space
            1 2 3 4 5
            3 2 1
            1 2 3 4
            5 6 7 8
            1 2 5 8
        find all items while the freqence >= minimal support
        :return: the all statisfied items.
        resultItem = [[(items,support),(items,support)....],[],[]
        result sample:
                [[('1', 0.8), ('2', 0.8)], [('1,2', 0.8)]]
    """
    
    transactions, totalTransaction = datas, len(datas)
    minsup = int(minSupport * totalTransaction)
    items = {}
    candidateItems = {}  # all candidate items
    for trans in transactions:
        for item in trans:
            candidateItems[item] = 1
            if item in items.keys():
                items[item] += 1
            else:
                items[item] = 1
    resultItem = []  # the result items
    step = 1
    while len(items) > 0:
        # select whether the freq is >= minsup
        # sort is for the make sure distinct items
        step += 1  # just for every step generate length = step items
        itemLeft = sorted(
            [(x, v * 1.0 / totalTransaction) for x, v in items.items() if v >= minsup],
            key=lambda x: x[0])
        if len(itemLeft) <= 0:
            break
        resultItem.append(itemLeft)
        items = {}
        # generate the new freq items
        for it1 in range(len(itemLeft) - 1):
            for it2 in range(it1 + 1, len(itemLeft)):
                key = sorted(set((itemLeft[it1][0] + "," + itemLeft[it2][0]).split(",")))
                tempKey = ",".join(key)
                if tempKey in candidateItems.keys() or len(key) != step:
                    continue
                else:
                    # find the freq of item if in original transactions
                    count = 0
                    for tr in transactions:
                        if len([c for c in tr if c in key]) == step:
                            count += 1
                    items[tempKey] = count
                    candidateItems[tempKey] = 1
    return resultItem


def main():
    datas = [
        ['1', '2', '3', '4', '5'],
        ['3', '2', '1'],
        ['1', '2', '3', '4'],
        ['5', '6', '7', '8'],
        ['1', '2', '5', '8']
    ]
    resultItem = getApriori(datas)
    print(resultItem)


if __name__ == "__main__":
    main()
