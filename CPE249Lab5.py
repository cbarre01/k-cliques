from collections import defaultdict
from collections import deque
from operator import itemgetter
import operator
import sys
import queue



class Vertex:
    def __init__(self):
        self.adjacents = []
        self.degree = 0
        self.L = []
        self.visited = False


class Graph:

    def __init__(self, edges):
        self.adjacencytable = self.build_adj_list(edges)
        self.kCores = defaultdict(list)

    def build_adj_list(self, edges):
        adjacencies = defaultdict(Vertex)
        for i in range(len(edges)):
            adjacencies[edges[i][0]].adjacents.append(edges[i][1])
            v1Int = edges[i][0]
            adjacencies[edges[i][0]].weight = int(v1Int)
            adjacencies[edges[i][1]].degree += 1
            adjacencies[edges[i][1]].adjacents.append(edges[i][0])
            adjacencies[edges[i][0]].degree += 1
            v2Int = edges[i][1]
            adjacencies[edges[i][1]].weight = int(v2Int)
        return adjacencies


    def prune_neighbors(self, v, curCore):
        v.visited=True
        for curNeighb in v.adjacents:
            if self.adjacencytable[curNeighb].visited == False:
                if (v.degree < curCore):
                    self.adjacencytable[curNeighb].degree = self.adjacencytable[curNeighb].degree - 1
                self.prune_neighbors(self.adjacencytable[curNeighb], curCore)
                if self.adjacencytable[curNeighb].degree < curCore:
                    v.degree  = v.degree - 1

    def print_k_cores(self):
        for curCore in sorted(list(self.kCores.keys()))[0:len(self.kCores.keys()) -1]:
            print("Vertices in " + str(curCore) + "-cores:")
            curCoreVerts = self.kCores[curCore]
            curCoreVerts.sort(key=int)
            print(", ".join(curCoreVerts))
        

    def find_k_cores(self):
        lastCore = list(self.adjacencytable.keys())
        keysList = list(self.adjacencytable.keys())
        for curK in range(1,self.find_max_degree() + 2):
            pruneStart = self.adjacencytable[lastCore[0]]
            self.prune_neighbors(pruneStart, curK)
            for v in keysList:
                 if self.adjacencytable[v].degree >= curK:
                     self.kCores[curK].append(v)
                     self.adjacencytable[v].visited = False
            lastCore = self.kCores[curK]
            #pdb.set_trace()
            if lastCore== []:
                break


    def find_max_degree(self):
        curDegree = 1
        for v in self.adjacencytable.values():
            if v.degree > curDegree:
                curDegree = v.degree
        return curDegree
        



def load_graph(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    edges = ""
    for line in lines: 
        verts = line.split(", ") 
        vert1 = verts[0]
        vert2 = verts[1]
        edges = edges +  str(vert1) + " " + str(vert2) + " "
    if len(edges) > 3:
        edges = edges[:-1]
    graph = graphify(edges)
    return Graph(graph)

def graphify(s):
        v = s.split()
        return list(zip(v[::2], v[1::2]))


def main():

    if len(sys.argv) == 1:
         print("no file specified")
    else:
         g = load_graph(sys.argv[1])
   
         g.find_k_cores()
         g.print_k_cores()

         

if __name__ == "__main__":
    main()
