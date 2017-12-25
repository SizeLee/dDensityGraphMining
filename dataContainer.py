import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json

class graphContainer:
    def __init__(self, density, frequence):
        self.graphList = []
        self.density = density
        self.frequence = frequence
        self.combineIDDic = {}
        self.ddfreGDic = {}
        self.combDic = {}
        return

    def addGraph(self, graphDic):
        if graphDic is not None:
            self.graphList.append(graphDic)

        return

    def loadFromFile(self, fileName):
        fp = open(fileName)
        temp = json.load(fp)
        fp.close()
        self.graphList = []
        for eachgraph in temp:
            graphDic = {}
            graphDic['ID'] = eachgraph['ID']
            graphDic['Vertex'] = eachgraph['Vertex']
            graphDic['aM'] = np.array(eachgraph['adjacencyMatrix'])
            self.graphList.append(graphDic)

        self.dDensityPrune()
        return

    def dDensityPrune(self):  ##d-density prune all the graph
        # count = 0
        remainGraphList = []
        for eachGraphDic in self.graphList:
            if self.__dDensitySimplified(eachGraphDic):
                remainGraphList.append(eachGraphDic)
            # print(count)
            # count += 1
        self.graphList = remainGraphList

    def __dDensitySimplified(self, graphDic):   ##d-density simplified one graph
        flag = True

        while(flag):
            flag = False
            matrix = graphDic['aM']
            index = 0
            remainset = list(range(0, len(graphDic['Vertex'])))
            degree = np.sum(matrix, axis=1)
            for eachdegree in degree:
                if eachdegree < self.density:
                    del remainset[index]
                    del graphDic['Vertex'][index]
                    flag = True
                else:
                    index += 1

            graphDic['aM'] = matrix[:, remainset][remainset, :]

        # judge = np.logical_and(degree < self.density, degree != 0)
        # while(np.any(judge)):
        return graphDic['Vertex'] ##if this list is empty, it means false, else it means true

    def generateHigherFrequenceDGraph(self):
        result = graphContainer(self.density, self.frequence + 1)
        self.combineIDDic = {}
        for eachGraph in self.graphList:
            index = eachGraph['ID'].copy()
            temp = self.combineIDDic
            while(len(index) != 1):
                if not index[0] in temp:
                    temp[index[0]] = {}
                temp = temp[index[0]]
                del index[0]

            if 'g' not in temp: ##g means graphs
                temp['g'] = []

            temp['g'].append(eachGraph)

        self.__gothroughIDDicAndIntersect(self.combineIDDic, result)

        if result.graphList: ##if graphList is empty, means no further layer of ddensity graph of higer frequence, return None
            return result
        else:
            return None

    def __gothroughIDDicAndIntersect(self, iddic, output):
        if 'g' not in iddic:
            for eachkey in iddic:
                self.__gothroughIDDicAndIntersect(iddic[eachkey], output)

        else:
            l = len(iddic['g'])
            for i in range(0, l):
                for j in range(i+1, l):
                    output.addGraph(self.__intersect(iddic['g'][i], iddic['g'][j]))

        return

    def __intersect(self, grapha, graphb):
        ## 比较两个图公有点的邻接矩阵即可， 从Vertex入手，同时simplified，若simplified出空图，则返回None。
        rGraph = {}

        vtemp, indexa, indexb = self.__intersect2sortedlist(grapha['Vertex'], graphb['Vertex'])
        if vtemp == []:
            return None  ##return a new graphDic, if no intersect, return None.

        if grapha['ID'][-1] < graphb['ID'][-1]:
            idtemp = grapha['ID'].copy()
            idtemp.append(graphb['ID'][-1])
        else:
            idtemp = graphb['ID'].copy()
            idtemp.append(grapha['ID'][-1])

        rGraph['ID'] = idtemp
        rGraph['Vertex'] = vtemp

        ma = grapha['aM'][:, indexa][indexa, :]
        mb = graphb['aM'][:, indexb][indexb, :]

        rGraph['aM'] = ma * mb

        if self.__dDensitySimplified(rGraph):
            return rGraph ##return a new graphDic, if no intersect, or intersection exist no ddensity subgraph, return None.
        else:
            return None   ##return a new graphDic, if intersection exist no ddensity subgraph, return None.

    def __intersect2sortedlist(self, lista, listb):
        vl = []
        indexla = []
        indexlb = []
        la = len(lista)
        lb = len(listb)
        ia = 0
        ib = 0
        while(ia < la and ib < lb):
            if (lista[ia] == listb[ib]):
                vl.append(lista[ia])
                indexla.append(ia)
                indexlb.append(ib)
                ia += 1
                ib += 1
            elif (lista[ia] < listb[ib]): ia += 1
            else: ib += 1

        return vl, indexla, indexlb

    def saveGraph(self, saveDirectory, jsonfileName):

        writeinjson = []

        for eachgraph in self.graphList:

            graphtemp = {}
            graphtemp['ID'] = eachgraph['ID']
            graphtemp['Vertex'] = eachgraph['Vertex']
            graphtemp['adjacencyMatrix'] = eachgraph['aM'].tolist()
            writeinjson.append(graphtemp)

            self.__drawAndSaveGraphFromMatrix(eachgraph, saveDirectory, '{}.png'.format(eachgraph['ID']))

        fp = open(saveDirectory + '\\' + jsonfileName, 'w')
        json.dump(writeinjson, fp)
        fp.close()

        return

    def __drawAndSaveGraphFromMatrix(self, graphDic, saveDirectory, saveName):

        V = len(graphDic['Vertex'])

        graph = nx.Graph()
        for i in range(V):
            for j in range(i):
                # if i==j: continue
                if graphDic['aM'][i, j] == 1:
                    graph.add_edge(graphDic['Vertex'][i], graphDic['Vertex'][j])

        nx.draw(graph, with_labels=True)
        saveS = saveDirectory + '\\' + saveName
        # plt.show()
        plt.savefig(saveS)
        plt.clf()
        return

    def findOutCurrentDdenFreSubG(self):
        self.ddfreGDic = {}

        glmin = len(self.graphList[0]['Vertex'])
        glmax = glmin
        for eachgraph in self.graphList:
            if len(eachgraph['Vertex']) < glmin:
                glmin = len(eachgraph['Vertex'])
            elif len(eachgraph['Vertex']) > glmax:
                glmax = len(eachgraph['Vertex'])

        self.combDic = {}
        for i in range(glmin, glmax+1):
            self.combDic[i] = self.__gencomb(self.density, i)

        for eachgraph in self.graphList:
            strid = str(eachgraph['Vertex'])
            if strid not in self.ddfreGDic:
                self.ddfreGDic[strid] = eachgraph['Vertex']

            self.__findDdFsGinEachGraph(eachgraph)

        return

    def __findDdFsGinEachGraph(self, graph):
        glen = len(graph['Vertex'])
        comb = self.combDic[glen]  ##inquery glen combine from d+1 to glen
        vertexay = np.array(graph['Vertex'])
        for eachcomb in comb:
            index = list(eachcomb)
            testGraph = {}
            testGraph['Vertex'] = vertexay[index].tolist()
            teststrid = str(testGraph['Vertex'])
            if teststrid in self.ddfreGDic:
                continue
            testGraph['aM'] = graph['aM'][:, index][index, :]
            if self.__testDdenstiy(testGraph):
                self.ddfreGDic[teststrid] = testGraph['Vertex']

        return

    def __testDdenstiy(self, testgraph):
        degree = np.sum(testgraph['aM'], axis=1)
        if np.any(degree < self.density):
            return False
        else:
            return True

    def __gencomb(self, d, graphlen):
        combmap = []
        for i in range(d+1, graphlen):
            combmaptemp = []
            self.__combineFun(combmaptemp, i, graphlen, 0, 0, )
            combmap += combmaptemp

        return combmap

    def __combineFun(self, combmap, comblen, graphlen, considerFeatureNo, alreadyCombine, *combine):
        # print(*combine)
        if alreadyCombine == comblen:
            # print(combine)
            combmap.append(combine)
            return
        elif considerFeatureNo >= graphlen:
            return

        self.__combineFun(combmap, comblen, graphlen, considerFeatureNo + 1, alreadyCombine, *combine)

        self.__combineFun(combmap, comblen, graphlen, considerFeatureNo + 1, alreadyCombine + 1, *combine, considerFeatureNo)
        # self.__combineFun(considerFeatureNo + 1, alreadyCombine + 1, *combine + (considerFeatureNo,))

if __name__ == "__main__":
    gc = graphContainer(3, 1)
    gc.loadFromFile(".\\data\\adjacencyMatrix.json")
    # gc.saveGraph('.\\midData', 'adjacencyMatrix.json')
    tgc = gc.generateHigherFrequenceDGraph()
    # if ngc is not None:
    #     ngc.saveGraph('.\\midData', 'ngc.json')
    tgc.findOutCurrentDdenFreSubG()
    print(tgc.ddfreGDic)
    print(len(tgc.ddfreGDic))


