from graph_tool.all import *
import math
# import cairo
# import graphviz
# import os
# os.environ["PATH"] += os.pathsep + "c:/Program Files (x86)/Graphviz/bin"
# from graph_tool.all import *
# import graph_tool.all as gt
# import graph_tool.draw
# print(f"{dir(graph_tool.draw)}")
# from graph_tool.draw import graph_draw
import argparse
parser = argparse.ArgumentParser(description="Run Python code with user input")
parser.add_argument("input_value", help="Input value to process")
args = parser.parse_args()
args = args.input_value

storage = {}
graph_tool.openmp_enabled()
currentGraph = {}
'''********* Graph Creation **********'''
def createGraph(txt):
    g = graph_tool.Graph(directed=False)
    currentGraph["graph"] = g
    nodeColor = g.new_vertex_property("int")
    g.vertex_properties["color"] = nodeColor
    eWeight = g.new_edge_property("double")
    bot = g.add_vertex()
    storage["bot"] = bot
    nodeColor[bot] = 10
    top = g.add_vertex()
    storage["top"] = top
    nodeColor[top] = 11
    storage["weight"] = eWeight
    
    with open(txt,'r') as file:
        lines = file.readlines()
        metadata = lines[0].strip().split()
        x = int(metadata[0])
        y = int(metadata[1])
        previousRow = {}
        preNode = ""
        firstrow = lines[1].strip().split()
        for i in range(x): #creates bottom row of structure
            current = g.add_vertex()
            nodeColor[current] = int(firstrow[i])
            outer = g.add_edge(current,bot)
            eWeight[outer] = 1.0
            if(i==0):
                preNode = current
                previousRow[0] = current
            else:
                num = int(firstrow[i])
                edge = g.add_edge(current,preNode)
                eWeight[edge] = 1.0
                previousRow[i] = current
                preNode = current
        # for edge in g.edges():
        #     print(edge)

        for a in range(y+1):
            if(a==0 or a==1): #skips over the metadata and the first row of the graph, since those two lines have already been processed
                continue
            row = lines[a].strip().split()
            currentRow = {}
            for i in range(x):
                currentNode = g.add_vertex()
                nodeColor[currentNode] = int(row[i])
                currentRow[i] = currentNode
                if(a==y):
                    outer1 = g.add_edge(currentNode,top)
                    eWeight[outer1] = 1.0
                if(i==0):
                    preNode = currentNode
                    edge = g.add_edge(currentNode,previousRow[i])
                    eWeight[edge] = 1.0
                    if(i+1<x):
                       edge = g.add_edge(currentNode,previousRow[i+1])
                       eWeight[edge] = math.sqrt(2)
                elif(i==x-1): #last element of a row
                    edge = g.add_edge(preNode,currentNode)
                    eWeight[edge] = 1.0
                    edge = g.add_edge(currentNode, previousRow[i])
                    eWeight[edge] = 1.0
                    edge = g.add_edge(currentNode, previousRow[i-1])
                    eWeight[edge] = math.sqrt(2)
                    previousRow = currentRow #resets previous row for the next row
                else:
                    edge = g.add_edge(currentNode,preNode)
                    eWeight[edge] = 1.0
                    edge = g.add_edge(currentNode,previousRow[i])
                    eWeight[edge] = 1.0
                    edge1 = g.add_edge(currentNode,previousRow[i-1])
                    eWeight[edge1] = math.sqrt(2)
                    edge2 = g.add_edge(currentNode,previousRow[i+1])
                    eWeight[edge2] = math.sqrt(2)
                    preNode = currentNode
    return g

g = createGraph(args)
for edge in g.edges():
    print(edge,end="")
print('\n')


'''********* Filtering the Graph **********'''
def edge_filter(e):
    if(currentGraph["graph"].vertex_properties["color"][e.source()]==10 or currentGraph["graph"].vertex_properties["color"][e.target()]==10):
        return True
    if(currentGraph["graph"].vertex_properties["color"][e.target()]==11 or currentGraph["graph"].vertex_properties["color"][e.source()]==11):
        return True
    return currentGraph["graph"].vertex_properties["color"][e.source()] == currentGraph["graph"].vertex_properties["color"][e.target()]

def vertex_filter(v):
    return True
    

print("filtered graph edges:")
g_filtered = graph_tool.GraphView(g, vfilt=vertex_filter, efilt=edge_filter)
for edge in g_filtered.edges():
    print(edge, end="")
print('\r\n')

# print(g_filtered.num_edges)
# for edge in g_filtered.edges():
#     print(edge)

'''********* BFS **********'''

class VisitorExample(graph_tool.search.BFSVisitor): #this class 

    def __init__(self, name, pred, dist):
        self.name = name
        self.pred = pred
        self.dist = dist

    def discover_vertex(self, u):
        # print("-->", self.name[u], "has been discovered!")
        return

    def examine_vertex(self, u):
        # print(self.name[u], "has been examined...")
        return

    def tree_edge(self, e):
        self.pred[e.target()] = int(e.source())
        self.dist[e.target()] = self.dist[e.source()] + 1
vprop = g_filtered.new_vertex_property("int")
g_filtered.vertex_properties["vprop"] = vprop
interprop = g_filtered.vertex_properties["vprop"]
distBFS = g_filtered.new_vertex_property("int")
predBFS = g_filtered.new_vertex_property("int64_t",-1)
graph_tool.search.bfs_search(g_filtered,storage["bot"],VisitorExample(interprop,predBFS,distBFS))
def get_path(predecessor_map, start, end):
    path = []
    current = end
    while current != start and current != -1:
        path.append(current)
        current = predecessor_map[g.vertex(current)]
    if current == start:
        path.append(start)
    return path[::-1]
BFSpath = {}
for v in g_filtered.vertices():
    path = get_path(predecessor_map=predBFS, start=0, end=int(v))
    BFSpath[int(v)] = path
print("bfs - pathing")
print(BFSpath)
# print(distBFS.a)





print(11111111111111111111111111111111111111)


        


