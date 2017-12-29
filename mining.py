import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json
import dataContainer

class Mining:
    def __init__(self, density, frequence, fileName):
        self.density = density
        self.frequence =frequence
        self.fileName = fileName
        self.gcf = []

    def mineddfG(self):
        self.gcf = []
        self.gcf.append(None)
        self.gcf.append(dataContainer.graphContainer(self.density, 1))
        self.gcf[1].loadFromFile(self.fileName)
        for i in range(1, self.frequence):
            self.gcf.append(self.gcf[i].generateHigherFrequenceDGraph())
            if self.gcf[i+1] is None:
                print('No Vertex subset fit the conditions')
                return False
            self.gcf[i] = None ###to release the former layer data, reduce memory use.
            print('Finish the frequence-{} layer and generate the next layer'.format(i))

        print('mining on the frequence-{} layer'.format(self.frequence))
        self.gcf[self.frequence].findOutCurrentDdenFreSubG()
        print(self.gcf[self.frequence].ddfreGDic)
        print(len(self.gcf[self.frequence].ddfreGDic))
        return True

    def findtopk(self, k):
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


if __name__ == '__main__':
    m = Mining(3, 10, ".\\data\\adjacencyMatrix.json")##3,4; 4,4; 3,9
    if m.mineddfG():
        m.findtopk(4)##2,3,4