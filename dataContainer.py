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
        # self.__delduplicategraph()  #this step lower the perform on the large amount of small graph data,
                                      # may improve perform on small amount of large graph data

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

    def __delduplicategraph(self):  ###used only when find out frequent subgraph, and data is small amount of large data
        i = 0
        while(i<len(self.graphList)):
            j = i + 1
            while(j<len(self.graphList)):
                if len(self.graphList[i]['Vertex']) < len(self.graphList[j]['Vertex']):
                    if self.__iscontain(self.graphList[i], self.graphList[j]):
                        del self.graphList[i]
                        i = i - 1
                        break
                elif len(self.graphList[i]['Vertex']) >= len(self.graphList[j]['Vertex']):
                    if self.__iscontain(self.graphList[j], self.graphList[i]):
                        del self.graphList[j]
                        j = j - 1

                j += 1

            i += 1
        return

    def __iscontain(self, graphsmall, graphbig):
        ls = len(graphsmall['Vertex'])
        lb = len(graphbig['Vertex'])
        iters = 0
        iterb = 0
        indexb = []
        while(iters<ls and iterb<lb):
            if graphsmall['Vertex'][iters] == graphbig['Vertex'][iterb]:
                indexb.append(iterb)
                iters += 1
                iterb += 1
            elif graphsmall['Vertex'][iters] > graphbig['Vertex'][iterb]:
                iterb += 1
            elif graphsmall['Vertex'][iters] < graphbig['Vertex'][iterb]:
                return False

        if iters < ls:
            return False

        judge = (graphbig['aM'][indexb, :][:, indexb] < graphsmall['aM'])
        if np.any(judge):
            return False
        return True

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

        return

    def saveddfreG(self, filename):
        fp = open(filename, 'w')
        json.dump(self.ddfreGDic, fp)
        fp.close()
        return

    def recordVIDinddfreG(self):
        recordset = set()
        for eachkey in self.ddfreGDic:
            recordset = recordset.union(self.ddfreGDic[eachkey])
        return recordset


class topKfrequentVertexContainer:
    def __init__(self, unionedVertexSubsetNumkk, vertexmaximum):
        self.unionedVsetNumk = unionedVertexSubsetNumkk
        self.ddfVDic = {}
        self.vertexSetIDDic = {}
        self.vertexmaximum = vertexmaximum  ###频繁点集所包含的所有点的种类的数量
        self.findAllVertexOfNextlayer = []
        self.curlargest = {}

    def getddfVDicFromGraphContainer(self, frequentLayerGraphContainer):
        self.ddfVDic = frequentLayerGraphContainer.ddfreGDic
        count = 0
        self.vertexSetIDDic = {}
        self.vertexSetIDDic['vsetlist'] = []
        for eachKey in self.ddfVDic:
            vdictemp = {}
            vdictemp['ID'] = [count]
            vdictemp['gkey'] = [eachKey]
            vdictemp['vset'] = self.ddfVDic[eachKey]
            self.vertexSetIDDic['vsetlist'].append(vdictemp)
            count += 1
        return

    def generateHigherKvalueVUnionContainer(self):
        ##在之前的词典vertexSetIDDic上融合后同时将词典拓展一层赋值给result返回
        resultContainer = topKfrequentVertexContainer(self.unionedVsetNumk + 1, self.vertexmaximum)
        resultContainer.vertexSetIDDic = self.vertexSetIDDic ##不用copy,直接在上一层基础上改,改完把上一层抛弃,加快速度,节省空间

        self.__gothroughDic(resultContainer.vertexSetIDDic)

        return resultContainer  ##k每一加一层,都可以检查一下上一层的findallvertex,如果有则已发现包含所有可能点最大集合(k可能还没达标),
                                 # 如果加了新一层,其vertexSetIDDic已空,则上一层的findallvertex必然有集合,因为只有发现了allvertexset才可能让下层iddic变为空

    def __gothroughDic(self, dicpointer):
        if 'vsetlist' not in dicpointer:
            deletelist = []
            for eachkey in dicpointer:
                self.__gothroughDic(dicpointer[eachkey])
                if dicpointer[eachkey] == {}:
                    deletelist.append(eachkey)

            for eachkey in deletelist:
                del dicpointer[eachkey]

            return

        else:
            for i in range(len(dicpointer['vsetlist'])-1):
                for j in range(i+1, len(dicpointer['vsetlist'])):
                    mergetemp = self.__merge2vertexSet(dicpointer['vsetlist'][i], dicpointer['vsetlist'][j])##merge to vertex subset,
                    # if merged set is no more larger, cut the merged vertex set.
                    # In other words check if one of these two set for merge contain another
                    if mergetemp is None:
                        continue
                    if len(mergetemp['vset']) == self.vertexmaximum: ###merge出全点图,则这些全点图在下一层中必然merge消除同时拥有所有点,所以不必等到下一层出现merge消除再判定是否全点图,每次merge即可判定。
                        self.findAllVertexOfNextlayer.append(mergetemp)
                    if mergetemp['ID'][-2] not in dicpointer:
                        dicpointer[mergetemp['ID'][-2]] = {}
                        dicpointer[mergetemp['ID'][-2]]['vsetlist'] = []
                    dicpointer[mergetemp['ID'][-2]]['vsetlist'].append(mergetemp)

            del dicpointer['vsetlist']
            return

    def __merge2vertexSet(self, vset1, vset2):
        newv = self.__union2sortedlist_noContainEachOther(vset1['vset'], vset2['vset'])
        if newv:
            resultv = {}
            resultv['vset'] = newv
            # resultv['gkey'] = vset1['gkey'] + vset2['gkey']
            if vset1['ID'][-1] < vset2['ID'][-1]:
                resultv['ID'] = vset1['ID'].copy()
                resultv['ID'].append(vset2['ID'][-1])
                resultv['gkey'] = vset1['gkey'].copy()
                resultv['gkey'].append(vset2['gkey'][-1])
            else:
                resultv['ID'] = vset2['ID'].copy()
                resultv['ID'].append(vset1['ID'][-1])
                resultv['gkey'] = vset2['gkey'].copy()
                resultv['gkey'].append(vset1['gkey'][-1])

            return resultv

        else:
            return

    def __union2sortedlist_noContainEachOther(self, vlists, vlistb):  ##if one contains each another, return empty list
        if len(vlists)>len(vlistb):
            temp = vlistb
            vlistb = vlists
            vlists = temp

        indexs = 0
        indexb = 0
        containflag = True
        unionlist = []
        while(indexs < len(vlists) and indexb < len(vlistb)):
            if vlistb[indexb] < vlists[indexs]:
                unionlist.append(vlistb[indexb])
                indexb += 1
            elif vlistb[indexb] == vlists[indexs]:
                unionlist.append(vlistb[indexb])
                indexb += 1
                indexs += 1
            else:
                containflag = False
                unionlist.append(vlists[indexs])
                indexs += 1

        if indexs < len(vlists):
            # containflag = False
            unionlist = unionlist + vlists[indexs:]

        elif indexb < len(vlistb):
            if containflag:
                return []
            unionlist = unionlist + vlistb[indexb:]

        else:
            if containflag:
                return []

        return unionlist

    def findCurrentlayerMaximum(self): ###从当前层找到最大的k图并
        self.curlargest = {}
        self.curlargest['vnum'] = 0
        self.curlargest['vsetlist'] = []
        self.__gothroughDicAndfindLagest(self.vertexSetIDDic)
        return self.curlargest

    def __gothroughDicAndfindLagest(self, dicpointer):
        if 'vsetlist' not in dicpointer:
            for eachkey in dicpointer:
                self.__gothroughDicAndfindLagest(dicpointer[eachkey])
            return

        else:
            for eachVset in dicpointer['vsetlist']:
                if len(eachVset['vset']) > self.curlargest['vnum']:
                    self.curlargest['vnum'] = len(eachVset['vset'])
                    self.curlargest['vsetlist'] = []
                    self.curlargest['vsetlist'].append(eachVset)
                elif len(eachVset['vset']) == self.curlargest['vnum']:
                    self.curlargest['vsetlist'].append(eachVset)

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


