# load packages
import json
import random
import copy

# helper
def collapse(graph):

    # pick the first node
    keys = list(graph.keys())
    node1 = random.choice(keys)

    # pick the second node from the first node's list
    adjacent_nodes = graph[node1]
    node2 = random.choice(adjacent_nodes)

    # set up a new node,
    key = node1+"&"+node2
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
    # the kargers min cut. 10000 here is a place holder, it has to be big enough for the database
    result = 10000

    # the time to run the algorithm with. The usual choice would be n^2logn, but it takes too long to run.
    run = 1

    # run the karger
    for i in range(run):

        # make a copy of the original graph to keep myself from messing up the original one.
        copied_graph =  copy.deepcopy(graph)

        # when the graph is shrinked to 2 nodes, the algorithm ends.
        while len(copied_graph) > 2:

            # pick two node and collapse the graph
            collapse(copied_graph)

            cut = len(list(copied_graph.values())[0])
            if (result > cut): 
                result = cut
            print("Size of the graph is", len(copied_graph), ", and the current min is", result)
        print("End of round", i, ".")
            
    return result
        
# a dictionary to store the adjacency list 
graph = {}

# Opening JSON file
f = open('data.json')
 
# returns JSON object as
# a dictionary
data = json.load(f)
 
# Iterating through the json
for i in data:
    str_list = []
    for j in data[i]:
        if str(i)==str(j):
            continue
        str_list.append(str(j))
    if len(str_list) == 0:
        continue
    graph[str(i)] = str_list

 
# Closing file
f.close()

print(karger(graph))