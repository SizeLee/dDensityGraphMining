import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
import dataContainer
import time

class Mining:
    def __init__(self, density, frequence, fileName):
        self.density = density
        self.frequence =frequence
        self.fileName = fileName
        self.gcf = []
        self.ddfGexist = False

    def mineddfG(self):
        self.ddfGexist = True
        self.gcf = []
        self.gcf.append(None)
        self.gcf.append(dataContainer.graphContainer(self.density, 1))
        self.gcf[1].loadFromFile(self.fileName)
        for i in range(1, self.frequence):
            self.gcf.append(self.gcf[i].generateHigherFrequenceDGraph())
            if self.gcf[i+1] is None:
                print('No Vertex subset fit the conditions')
                self.ddfGexist = False
                return False
            self.gcf[i] = None ###to release the former layer data, reduce memory use.
            print('Finish the frequence-{} layer and generate the next layer'.format(i))

        print('mining on the frequence-{} layer'.format(self.frequence))
        self.gcf[self.frequence].findOutCurrentDdenFreSubG()

        print('Find out {} D-density frequent vertex set(s):'.format(len(self.gcf[self.frequence].ddfreGDic)))
        print(self.gcf[self.frequence].ddfreGDic)
        print()
        return True

    def findtopk(self, k):
        if not self.ddfGexist:
            print('No Vertex subset fit the conditions,so there is no top k vertex subsets')
            return
        if k<1:
            print('invalid k value')
            return
        if k>= len(self.gcf[self.frequence].ddfreGDic):
            print('k value is larger or equal than the number of D-density frequent vertex sets, top k result is all the D-density frequent vertex sets')
            ##输出topk点集的表达方式，比如gkey集合
            for eachkey in self.gcf[self.frequence].ddfreGDic:
                print(eachkey)
            return

        vertexMaximum = len(self.gcf[self.frequence].recordVIDinddfreG())

        initlayer = dataContainer.topKfrequentVertexContainer(1, vertexMaximum)
        initlayer.getddfVDicFromGraphContainer(self.gcf[self.frequence])

        prelayer = initlayer
        nextlayer = initlayer
        # noneedcontinueflag = False
        for i in range(1, k):
            nextlayer = prelayer.generateHigherKvalueVUnionContainer()
            if prelayer.findAllVertexOfNextlayer:
                print('find k value of {}, these {} vertex sets already cover all the vertex in D-density frequent vertex sets'.format(i+1, i+1))
                ##输出topk点集的表达方式，比如gkey集合
                for eachVset in prelayer.findAllVertexOfNextlayer:
                    print(eachVset['gkey'])
                print('There are {} combine of top {} frequent D-density vertex sets cover all vertex'.format(len(prelayer.findAllVertexOfNextlayer), i+1))
                # noneedcontinueflag = True
                return
        # if noneedcontinueflag:
        #     return

        nextlayer.findCurrentlayerMaximum()
        ##输出topk点集的表达方式，比如gkey集合
        for eachVset in nextlayer.curlargest['vsetlist']:
            print(eachVset['gkey'])
        print('find {} combine of {} D-density frequent vertex sets maximize union vertex set'.format(len(nextlayer.curlargest['vsetlist']), k))


if __name__ == '__main__':   ##############code below is for testing the performance of mining algorithms
    timeoffrequence3 = []
    densityX = [i for i in range(3, 10)]
    for eachx in densityX:
        print('Mining with density={}, frequence = 3......'.format(eachx))
        start = time.clock()
        m = Mining(eachx, 3, ".\\data\\adjacencyMatrix.json")
        m.mineddfG()
        end = time.clock()
        timeoffrequence3.append(round(end - start, 3))
        # print(eachx)
        # print(timeoffrequence3)
        print()

    timeofdensity3 = []
    frequenceX = [i for i in range(3, 10)]
    for eachx in frequenceX:
        print('Mining with density=3, frequence = {}......'.format(eachx))
        start = time.clock()
        m = Mining(3, eachx, ".\\data\\adjacencyMatrix.json")
        m.mineddfG()
        end = time.clock()
        timeofdensity3.append(round(end - start, 3))
        # print(eachx)
        # print(timeofdensity3)
        print()

    fg1 = plt.figure(figsize=(8, 5))
    plt.plot(densityX, timeoffrequence3, 'b-')
    plt.xlabel('density')
    plt.ylabel('mining time cost (s)')
    plt.xlim(2, 10)
    # plt.ylim(0, 30)
    datadotxy = tuple(zip(densityX, timeoffrequence3))
    i = 0
    for dotxy in datadotxy:
        plt.annotate(str(timeoffrequence3[i]), xy=dotxy)
        i = i + 1
    plt.show()
    plt.close()

    fg2 = plt.figure(figsize=(8, 5))
    plt.plot(frequenceX, timeofdensity3, 'b-')
    plt.xlabel('frequence')
    plt.ylabel('mining time cost (s)')
    plt.xlim(2, 10)
    # plt.ylim(0, 30)
    datadotxy = tuple(zip(frequenceX, timeofdensity3))
    i = 0
    for dotxy in datadotxy:
        plt.annotate(str(timeofdensity3[i]), xy=dotxy)
        i = i + 1
    plt.show()
    plt.close()

#######################################
    timeofk = []
    ks = [i for i in range(1, 7)]
    m = Mining(3, 6, ".\\data\\adjacencyMatrix.json")##3,4; 4,4; 3,9
    m.mineddfG()
    for k in ks:
        print('Mining top k={} with density=3, frequence=6'.format(k))
        start = time.clock()
        m.findtopk(k)##2,3,4
        end = time.clock()
        timeofk.append(round(end-start, 3))

    fg3 = plt.figure(figsize=(8, 5))
    plt.plot(ks, timeofk, 'b-')
    plt.xlabel('k value')
    plt.ylabel('mining time cost (s)')
    plt.xlim(0, 7)
    # plt.ylim(0, 30)
    datadotxy = tuple(zip(ks, timeofk))
    i = 0
    for dotxy in datadotxy:
        plt.annotate(str(timeofk[i]), xy=dotxy)
        i = i + 1
    plt.show()
    plt.close()
############################################
    timeofk = []
    ks = [i for i in range(1, 7)]
    m = Mining(3, 9, ".\\data\\adjacencyMatrix.json")  ##3,4; 4,4; 3,9
    m.mineddfG()
    for k in ks:
        print('Mining top k={} with density=3, frequence=9'.format(k))
        start = time.clock()
        m.findtopk(k)  ##2,3,4
        end = time.clock()
        timeofk.append(round(end - start, 3))

    fg3 = plt.figure(figsize=(8, 5))
    plt.plot(ks, timeofk, 'b-')
    plt.xlabel('k value')
    plt.ylabel('mining time cost (s)')
    plt.xlim(0, 7)
    # plt.ylim(0, 30)
    datadotxy = tuple(zip(ks, timeofk))
    i = 0
    for dotxy in datadotxy:
        plt.annotate(str(timeofk[i]), xy=dotxy)
        i = i + 1
    plt.show()
    plt.close()