# load packages
import json
import random
import copy
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import math


# Defining the visual class
class GraphVisualization:

    def __init__(self):
        self.visual = []

    def addEdge(self, a, b):
        temp = [a, b]
        self.visual.append(temp)


# helper
def collapse(graph):
    # pick the first node
    keys = list(graph.keys())
    node1 = random.choice(keys)

    # pick the second node from the first node's list
    adjacent_nodes = graph[node1]
    node2 = random.choice(adjacent_nodes)

    # set up a new node,
    key = node1 + "&" + node2
    graph[key] = graph.pop(node2) + graph.pop(node1)

    # remove the keys that shouldn't be there anymore
    for i in graph.keys():
        copied_list = copy.copy(graph[i])
        for j in copied_list:
            if j == node1 or j == node2:
                graph[i].remove(j)
                if key != i:
                    graph[i].append(key)


# run the karger algorithm
def karger(graph):
    # the kargers min cut. 10000 here is a place holder, it has to be big enough for the
    # database
    result = 10000
    original_size = len(graph)

    # the time to run the algorithm with. The usual choice would be n^2logn,
    # but it takes too long to run.
    run = len(graph) ^ 2 * int(math.log(len(graph)))
    min_recorder = []
    current_cut = []

    # run the karger
    for i in range(run):

        # make a copy of the original graph to keep myself from messing up the
        # original one.
        copied_graph = copy.deepcopy(graph)

        temp_cut = 1000

        index = 0

        fig = plt.figure()
        # when the graph is shrinked to 2 nodes, the algorithm ends.
        while len(copied_graph) > 2:
            # pick two node and collapse the graph
            collapse(copied_graph)
            cut = len(list(copied_graph.values())[0])

            if i == (run - 1):

                m_size = math.sqrt(original_size)
                row_number = int(m_size)
                if m_size - int(m_size) > 0:
                    row_number += 1
                col_number = int((original_size - 1) / row_number)
                if (col_number * row_number < original_size - 1):
                    col_number += 1
                print("rows", original_size, col_number, row_number)
                plt.subplot(row_number, col_number, index + 1)
                plt.tight_layout()
                index += 1
                G = GraphVisualization()
                for m in copied_graph:
                    for n in copied_graph[m]:
                        G.addEdge(m, n)
                graph = nx.Graph()
                graph.add_edges_from(G.visual)
                nx.draw_networkx(graph)
                plt.title("Round: {}".format(index))
                plt.xticks([])
                plt.yticks([])

            if (result > cut):
                result = cut
            if (temp_cut > cut):
                temp_cut = cut
            print("Size of the graph is", len(copied_graph), ", and the current min is",
                  result)
        print("cut", cut)
        current_cut.append(temp_cut)

        min_recorder.append(result)
        print("End of round", i, ".")
        fig.savefig("demo1.png")

    print(min_recorder)
    print(current_cut)
    fig2 = plt.figure()
    plt.plot(min_recorder, color='red')
    plt.ylim([0, original_size])
    plt.xlabel('i-th run')
    plt.ylabel('number of min cut')
    plt.xticks(np.arange(0, len(min_recorder), 1))
    index = np.arange(len(current_cut))
    plt.bar(index, current_cut, color='green')
    plt.title("Min cut over runs")
    fig2.savefig("demo2.png")
    return result


# a dictionary to store the adjacency list
graph = {}

# Opening JSON file
f = open('sample2.json')

# returns JSON object as
# a dictionary
data = json.load(f)

# Iterating through the json
for i in data:
    str_list = []
    for j in data[i]:
        if str(i) == str(j):
            continue
        str_list.append(str(j))
    if len(str_list) == 0:
        continue
    graph[str(i)] = str_list

# Closing file
f.close()

print(karger(graph))
