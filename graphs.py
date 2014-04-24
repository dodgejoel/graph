import numpy as np
import random

def weighted_choice(weight_dict):
    '''
    weight_dict is a dictionary whose keys are going to be chosen from randomly
    with a distribution given by the values.  
    weight_dict.values() should sum to 1.
    '''

    w = sum(weight_dict.values())
    cutoff = random.random()
    threshold = 0
    for choice in weight_dict:
        if threshold + weight_dict[choice] >= cutoff:
            break
        threshold += weight_dict[choice]
    return choice

class graph():
    '''
    Class is called with a sequence parameter which is the colection of vertex labels.
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
        self.degs = dict([(v, 0) for v in verts])
        self.nv = len(verts)
        self.ne = sum(map(len, self.ve_dict.values())) / 2

    def __iter__(self):
        return iter(self.ve_dict)

    def __getitem__(self, key):
        return self.ve_dict[key]

    def __len__(self):
        return self.nv

    def add_edge(self, i, j):
        if i in self.ve_dict and j in self.ve_dict:
            if i == j:
                return False
            elif i not in self.ve_dict[j]:
                self.ne += 1
                self.degs[i] += 1
                self.degs[j] += 1
                self.ve_dict[i].add(j)
                self.ve_dict[j].add(i)
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

        norm = self.nv*(self.nv - 1) - 2 * self.ne
        if norm:
            choice_dict = dict([(i, (self.nv - self.degs[i] - 1) / norm) 
                                for i in self.ve_dict]) 
            i = weighted_choice(choice_dict) 
            j = random.choice(
                    [e for e in self.ve_dict if 
                     e != i  and 
                     e not in self.ve_dict[i]])
            self.ve_dict[i].add(j)
            self.ve_dict[j].add(i)
            self.ne += 1
            self.degs[i] += 1
            self.degs[j] += 1
        else:
            print('error: graph complete, no more edges to add')

    def is_complete(self):
        if self.ne == self.nv * (self.nv - 1) / 2:
            return True
        else:
            return False

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

    
def sf_explore(G, v, visited, sf):
    '''Utility explore function used in the constructio of a spanning forest below.'''
    visited[v] = True
    for u in G[v]:
        if not visited[u]:
            sf.add_edge(u, v)
            sf_explore(G, u, visited, sf)

def spanning_forest(G):
    '''Perform a dfs and returns a spanning forest of G.'''

    visited = dict([(v, False) for v in G])
    sp_forest = graph(G)
    for v in G:
        if not visited[v]:
            sf_explore(G, v, visited, sp_forest)
    return sp_forest

def explore(G, v, visited, pre_post, count):

    visited[v] = True
    pre_post[v].append(count)
    count += 1

    for u in G[v]:
        if not visited[u]:
            count = explore(G, u, visited, pre_post, count)
    pre_post[v].append(count)
    count += 1
    return count

def dfs(G, visited = []):
    '''
    Depth first search through vertices of G.
    Returns the number of connected components of G.
    '''

    visited = dict([(v, False) for v in G])
    pre_post = dict([(v, []) for v in G])
    count = 0

    for v in G:
        if not visited[v]:
            count = explore(G, v, visited, pre_post, count)
    return pre_post 

def connected_components(G):
    '''
    Would like to take the pre_post data and return a list of the connected
    components of G.
    Seems ridiculous to not just do this during the depth first search.
    Can easily collect components inside the loop in dfs above.  
    '''
    pass      


if __name__ == '__main__':
    G = graph(range(2500))
    for i in range(1000):
        G.add_rand_edge()

    stack = dfs(G)
    print(stack)


