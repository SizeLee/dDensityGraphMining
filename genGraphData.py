import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import json


def drawAndSaveGraphFromMatrix(adjacencyMatrix, saveDirectory, saveName):

    shape = adjacencyMatrix.shape
    V = shape[0]
    graph = nx.Graph()
    for i in range(V):
        for j in range(i):
            # if i==j: continue
            if adjacencyMatrix[i, j] == 1:
                graph.add_edge(i,j)

    nx.draw(graph, with_labels=True)
    saveS = saveDirectory + '\\' + saveName
    # plt.show()
    plt.savefig(saveS)
    plt.clf()
    return

def drawAndSaveGraphFromMatrix_allV(adjacencyMatrix, saveDirectory, saveName):
    graph = nx.from_numpy_matrix(np.matrix(adjacencyMatrix))
    nx.draw(graph, with_labels=True)
    saveS = saveDirectory + '\\' + saveName
    # plt.show()
    plt.savefig(saveS)
    plt.clf()
    return


V = 10
N = 100
edgeDensity = 0.6
graphList = list()

for i in range(N):
    x = np.random.rand(V,V)
    x = np.triu(x, 1)
    x = x + x.T
    y = np.diag(np.zeros((V)))
    x += y
    x = x - (1 - edgeDensity)
    x /= np.abs(x)
    x = (x + np.abs(x))/2

    drawAndSaveGraphFromMatrix_allV(x, '.\\data', '{}.png'.format(i))

    graphDic = {}
    graphDic['ID'] = [i]
    graphDic['Vertex'] = list(range(0, V))
    graphDic['adjacencyMatrix'] = x.tolist()
    graphList.append(graphDic)
    print(i)

# print(graphList)

fp = open('.\\data\\adjacencyMatrix.json', 'w')
json.dump(graphList, fp)
fp.close()
