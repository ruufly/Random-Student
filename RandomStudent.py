import random
import time

nameList = ["A","B","C","D","E",'F',"G"] # 名单
UPList = [] # UP列表
line = 7 # 抽取人数
Map = [3,3,3,3,3,3,3]

def SearchIndex(arr, res) -> int:
    for i in arr:
        if arr[i] == res:
            return i
    return -1

def StartRandom(isUP : bool) -> str:
    seed = time.time()
    random.seed = seed
    
    nowLine = random.randint(0,line-1)
    if isUP and SearchIndex(UPList, nameList[nowLine]) != -1:
        return nameList[nowLine]
    
    if(random.randint(1,4) == 3):  # 重复概率25%
        if Map[nowLine] == 0:
            Map[nowLine] += int(line * 0.65)
            for i in range(1, line):
                if Map[i] > 0:
                    Map[i] -= 1
            return nameList[nowLine]
    return StartRandom(isUP)


for i in range(20):
    print(StartRandom(False))