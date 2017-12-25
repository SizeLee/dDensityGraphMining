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

    def mine(self):
        gcf = []
        gcf.append(None)
        gcf.append(dataContainer.graphContainer(self.density, 1))
        gcf[1].loadFromFile(self.fileName)
        for i in range(1, self.frequence):
            gcf.append(gcf[i].generateHigherFrequenceDGraph())
            if gcf[i+1] is None:
                print('No Vertex subset fit the conditions')
                return
            gcf[i] = None ###to release the former layer data, reduce memory use.
            print('Finish the frequence-{} layer'.format(i))

        gcf[self.frequence].findOutCurrentDdenFreSubG()
        print(gcf[self.frequence].ddfreGDic)
        print(len(gcf[self.frequence].ddfreGDic))


if __name__ == '__main__':
    m = Mining(4, 4, ".\\data\\adjacencyMatrix.json")
    m.mine()