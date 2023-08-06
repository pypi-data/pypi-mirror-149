import logging
from collections import defaultdict


class UnionFind:
    """

    O(1) find: Find if two nodes belong to the same set
    O(1) union: Combine two sets into 1 set
    """

    def __init__(self, nodes):
        """

        :param num_nodes:
        """
        # parent[i] means the father of the ith node.
        # initially every node's father is itself;
        # self.parent: List[int] = list(range(num_nodes))
        self.parent = {node: node for node in nodes}

        # rank[i] means how many nodes are there in the set where the i-th node is
        # located. When merging two nodes, we need to merge a single node to a majority
        # of nodes;
        # self.rank: List[int] = [0] * num_nodes
        self.rank = {node: 0 for node in self.parent}

    def find(self, node: int) -> int:
        """

        :param node:
        :return:
        """
        if self.parent[node] == node:
            return node
        self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, node_1: int, node_2: int):
        """

        :param node_1:
        :param node_2:
        :return:
        """
        node_1, node_2 = self.find(node_1), self.find(node_2)

        if node_1 != node_2:
            if self.rank[node_1] < self.rank[node_2]:
                node_1, node_2 = node_2, node_1

            self.parent[node_2] = node_1

            if self.rank[node_1] == self.rank[node_2]:
                self.rank[node_1] += 1

            return node_2
        else:
            logging.warning("Something went wrong in union find, attempting union of "
                            "nodes _already_ in the same set.")

    def disjoint_sets(self):
        result = defaultdict(list)
        for key in self.parent:
            result[self.find(key)].append(key)
        return result

    def non_roots(self):
        return {
            k: v for k, v in self.parent.items() if k != v
        }

    def roots(self):
        return {
            k: v for k, v in self.parent.items() if k == v
        }

    def supernode_size(self):
        temp = {k: [] for k in self.non_roots().values()}
        for k, v in self.parent.items():
            temp[v].append(k)
        return (len(v) for v in temp.values())
