import numpy as np
import random

def weighted_choice(weight_dict):
    '''
    weight_dict is a dictionary whose keys are going to be chosen from randomly
    with a distribution given by the values.  
    weight_dict.values() should sum to 1.
    '''

    if sum(weight_dict.values()) != 1:
        print('error: dict_values should sum to 1.')
        return False
    cutoff = random.random()
    threshold = 0
    for choice in weight_dict:
        if threshold + weight_dict[choice] >= cutoff:
            break
        threshold += weight_dict[choice]
    return choice

class digraph():
    '''
    Class is called with a sequence parameter which is the collection of vertex labels.
    There is an optional parameter of a dict whose values should be subsets of
        the set of vertices.
    Things are implemented so that iterating over an instance iterates over the vertices.
    len(instance) = number of vertices.  
    an instance can be indexed using the name of a vertex to get the set of
        vertices that the key has an edge to.
    This is all so that I can hide the implementation via the dict from the user.  
    '''
    
    def __init__(self, verts, edge_dict = {}):
        self.ve_dict = dict([(v, edge_dict.get(v, set())) for v in verts])
        self.out_deg = dict([(v, 0) for v in verts])
        self.nv = len(verts)
        self.ne = sum(map(len, self.ve_dict.values()))

    def __iter__(self):
        return iter(self.ve_dict)

    def __getitem__(self, key):
        return self.ve_dict[key]

    def __len__(self):
        return self.nv

    def __repr__(self):
        '''What is a nice string representation for a graph?'''
        return self.ve_dict.__repr__()

    def add_edge(self, v, w):
        '''add a directed edge from vertex v to vertex w'''
        if v in self.ve_dict and w in self.ve_dict:
            if v == w:
                return False
            elif w not in self.ve_dict[v]:
                self.ne += 1
                self.out_deg[v] += 1
                self.ve_dict[v].add(w)
                return True
            else:
                return False
        else:
            return False

    def subgraph(self, some_verts):
        '''Return the subgraph of G on the vertices in some_verts.'''
        
        some_edges = dict(
                [(v, set([e for e in self.ve_dict[v] if e in some_verts]))
                    for v in some_verts])
        return graph(some_verts, some_edges)

    def add_rand_edge(self):
        '''
        use the weighted choice function to choose a vertex to add an edge to
        weighting vertex i with weight nv - degree(i) - 1 / some normalizing
        factor.  
        '''

        norm = self.nv*(self.nv - 1) - self.ne
        if norm:
            choice_dict = dict([(i, (self.nv - self.out_deg[i] - 1) / norm) 
                                for i in self.ve_dict]) 
            v = weighted_choice(choice_dict) 
            w = random.choice(
                    [e for e in self.ve_dict if 
                     e != v  and 
                     e not in self.ve_dict[v]])
            self.add_edge(v, w)
        else:
            print('error: graph complete, no more edges to add')

    def is_complete(self):
        if self.ne == self.nv * (self.nv - 1):
            return True
        else:
            return False

    def reverse(self):
        '''
        return a graph with same vertex set and with an edge from v to w
        whenever self has an edge from w to v.
        '''

        reverse_graph = digraph(self.ve_dict.keys())
        for v in self.ve_dict:
            for w in self.ve_dict[v]:
                reverse_graph.add_edge(w, v)
        return reverse_graph

    def adj_mat(self):
        '''
        Breaks with the addition of labels.  Now need to fix this so that it
        translates labels into appropriate indices for the matrices.  
        '''
        
        mat = np.zeros((self.nv, self.nv))
        for i in range(self.nv):
            for j in self.ve_dict[i]:
                mat[i, j] = 1
        return mat

def dfs(G):
    '''
    Depth first search through vertices of G.
    Returns a dict whose pairs are of the form 
        (vertex, [first time visited, last time left]).  
    I do not understand why I have to pass counter as a paramter to explore
        below in order to access it but I do not have to pass visited as a
        parameter.
    '''

    visited = dict([(v, False) for v in G])
    pre_post = dict([(v, []) for v in G])
    counter = 0
    
    def explore(v, counter):
        visited[v] = True
        pre_post[v].append(counter)
        counter += 1
        for u in G[v]:
            if not visited[u]:
                counter = explore(u, counter)
        pre_post[v].append(counter)
        counter += 1
        return counter

    for v in G:
        if not visited[v]:
            counter = explore(v, counter)
    return pre_post 

if __name__ == '__main__':
    G = digraph(range(6))
    for i in range(6):
        G.add_rand_edge()
    
    print(G)
    Gprime = G.reverse()
    print(Gprime)
