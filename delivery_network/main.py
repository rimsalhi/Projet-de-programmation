from graph import Graph, graph_from_file
from operator import itemgetter 



###### QUESTION 2

def explore(G,v,s):
    """A recursive function that updates a set s (initially empty) 
    adding each time a node that isn't in s but connected to v 
    then moves to explore the connections of the added node.

    Args:
        G (Graph): 
        v (integer): a node in the Graph G
        s (set): initially empty 

    Returns:
        set: containing all the nodes from G connected to v
    """
    for k in G.graph[v]:
        if (k[0] in s)==False:
            s.add(k[0])
            explore(G,k[0],s)
    return s 

def connected_components_set(G):
    """Uses the explore function to determine the connected component of each node.
    The type Set, being unordered, allows us to avoid redundancy.

    Args:
        G (Graph)

    Returns:
        list: a list containing sets, each set is a group of connected nodes 
        that are connected together and thus form a connected component
    """
    L=[]
    for v in G.nodes:
        s=set()
        if (explore(G,v,s) in L)==False:
            L.append(explore(G,v,s))
    return L 

"""Complexity analysis: With V: number of the graph's node and E: number of its edges
- explore runs through all the graph's nodes. Its complexity is O(V)
- In the worst-case scenerio, connected_components_set runs explore for each node in the graph.
Therefore, its complexity is O(V*E).
"""


###### QUESTION 3

def get_path_with_power(G,p,t):
    """Uses a Breadth-search first to look for t[1], 
    starting from t[0], while stocking the traversed nodes in path.

    Args:
        G (Graph): 
        p (integer): the power of the truck ;  
                     the maximal power of the edges the truck can traverse.
        t (tuple): the route (le trajet)

    Returns:
        list: a possible path for the truck to go from t[0] to t[1] if exists
        None: if not
    """
    queue=[[t[0]]]
    while queue!=[]:
        path=queue.pop()
        node=path[-1]
        if node==t[1]:
            return path
        for k in G.graph[node]:
            if (k[1]<=p) and (k[0] not in path):
                queue.append(path+[k[0]])
    return None

""" Complexity analysis: 
The worst-case scenerio is the case in whitch the function returns None.
In this case, the function explore for every node its edges. 
Therefore, it explore all the nodes and edges. 
We conclude that the complexity is O(V+E). 
"""


###### QUESTION 4

def graph_from_file_4(filename):
    """Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Args:
        filename (str): the path of the file

    Returns:
        Graph: a Graph object with the graph from the file
    """
    f=open(filename, 'r')
    lines=f.readlines()  
    L=[]
    for i in range(len(lines)):
        L.append(lines[i].split())
    M=[i for i in range(1,int(L[0][0])+1)]
    G=Graph(M)
    G.nb_edges=int(L[0][1])
    L.pop(0)
    for line in L:
        if len(line)==4: 
            d=int(line[3])
        else: 
            d=1

        G.add_edge(int(line[0]),int(line[1]),int(line[2]),d)
    return G


###### QUESTION 6

def edges(G):
    """Returns a list of sets, each set is an edge of the graph object G.

    Args:
        G (Graph): 
    """
    H=[]
    for node in G.graph: 
        for k in G.graph[node]:
            if (([k[0], node],k[1]) not in H) and (([node,k[0]],k[1]) not in H):
                H.append(([node,k[0]],k[1]))
    edges=[k[0] for k in H]
    return edges,H

def min_power(G,t):
    """Starts by determining the maximal power of the edges PMax. 
    Then, using a dichotomous search on [Pmin,PMax], looks for 
    the minimal power with which the journey t is possible. 

    Args:
        G (Graph): 
        t (tuple): the route

    Returns:
        tuple: composed of - the path with the minimal power and its power if a path exists.
                           - None and the median power
    """
    #PW is the list of disctinct powers in the graph sorted in an increasing order.
    PW=[]
    for edge in edges(G)[0]:
        edge2=list(edge)
        for k in G.graph[edge2[0]]:
            if (k[0]==edge2[1]) and (k[1] not in PW):
                PW.append(k[1])
    PW.sort()
    #The dichotomous search for the path with minimal power.
    if len(PW) > 1 :
        a=0
        b=len(PW)-1
        while a<b:
            if get_path_with_power(G, PW[int((b+a)/2)], t)==None:
            #There are no paths for t with a power smaller than (b-a)/2.
                a=int((b+a)/2)+1
            #Continues its search in [(b-a)/2,b].
            else: 
                b=int((b+a)/2)
            #Continue its search for a path with less power required.
        B=get_path_with_power(G, PW[b],t)
        p=PW[b]
    else:
        p=Pw[0]
        B=edge2
    return (B ,p)

"""Complexity analysis: If we consider P to be the number of distinct powers in the graph:
the complexity of the construction of PW is O(P) and
the complexity of the dichotomous search is O(log2(P)*(V+E)).
Therefore, the complexity of the whole algorithm is O(P*(V+E)). 
If we only consider V and E, we conclude that the complexity is O(V+E).
"""


###### QUESTION 7 

# import graphviz #installed with conda install python-graphviz
# import os
# os.environ["PATH"]+=os.pathsep+'C:\Program Files\Graphviz\bin' #to be replaced with the path of the bin of Graphviz on the desktop once dowloaded.

# def G_rep(G,t):
#     P= min_power(G,t)[0]
#     v=t[0]
#     u=t[1]
#     f = graphviz.Graph('rep_graph00')
#     H=[]
#     for node in G.graph:
#         for k in G.graph[node]:
#             if ({node,k[0]} in H)==False:
#                 if (node in P) and (k[0] in P):
#                     f.node(str(node), fillcolor='red', style='filled')
#                     f.node(str(k[0]), fillcolor='red', style='filled')
#                     f.edge(str(node), str(k[0]), label= str(k[1]), color='red') 
#                 else:
#                     f.edge(str(node), str(k[0]), label= str(k[1]))
#                 H.append({node,k[0]})
#     f.node(str(v), label=str(v)+': Start', fillcolor='red', style='filled')
#     f.node(str(u), label=str(u)+': Finish', fillcolor='red', style='filled')
#     f.view()

#The representation of the graph and the minimal power path of network00: rep_graph00.gv.pdf
# g=graph_from_file_4("/home/onyxia/work/Projet-de-programmation/input/network.00.in")
# G_rep(g,(1,5))


###### QUESTION 10

def route_from_file(filename):
    """Reads a text file and returns a list of routes. 

    The file should have the following format: 
        The first line of the file is 'n' : number of routes
        The next n lines have 'node1 node2 utility of the route (node1,node2)'.
        All values are integers.

    Args:
        filename (str): the path of the file

    Returns:
        dict: The keys are routes : tuples of nodes. 
              The value of each key is its utility.
    """
    f=open(filename, 'r')
    lines=f.readlines()  
    L=[]
    for i in range(len(lines)):
        L.append(lines[i].split())
    L.pop(0)
    routes={}
    for line in L:
        if line[0]!=line[1]:
            routes[(int(line[0]),int(line[1]))]=int(line[2])
    return routes

import time

def necessary_time(filename1,filename2):
    """Returns the necessary time to find all the minimal power path if exists 
    for all the routes in the graph.

    Args:
        filename (str): the path of the graph file 

    Returns:
        float: the necessary time
    """
    G=graph_from_file_4(filename1)
    routes=route_from_file(filename2)
    a=time.perf_counter()
    for t in routes:
        mP=min_power(G,t)
    b=time.perf_counter()
    return b-a

#print(necessary_time("/home/onyxia/work/Projet-de-programmation/input/network.1.in",
#                    "/home/onyxia/work/Projet-de-programmation/input/routes.1.in"))
# Determining the minimal power of all routes in route.1 and their associated paths takes about 0,38s.

# print(necessary_time("/home/onyxia/work/Projet-de-programmation/input/network.2.in",
#                      "/home/onyxia/work/Projet-de-programmation/input/routes.2.in"))
# Determining the minimal power of all routes in route.2 and their associated paths takes more than 1h. 
# Judging by the complexity, it should take up to several hours. 



###### QUESTION 12

class UnionFind:
    def __init__(self, nodes=[]):
        parent=dict()
        for n in nodes:
            parent[n]=n
        self.parent=parent
        self.rank=dict([(n,0) for n in nodes])
        
    def find(self,n):
        if self.parent[n]==n:
            return n
        else: 
            self.parent[n] = self.find(self.parent[n])
            return self.parent[n]
    def union(self, m, n):
        # find the root of the sets in which elements
        # `x` and `y` belongs
        x = self.find(m)
        y = self.find(n)
        if self.rank[x] > self.rank[y]:
            self.parent[y] = x
            self.rank[x] = self.rank[x] +  1
        else:
            self.parent[x] = y
            self.rank[y] = self.rank[y] +  1




def kruskal(G):
    """Returns the minimal spanning tree of the graph G using the Kruskal algorithm.
    """
    E=sorted(edges(G)[1], key=itemgetter(1),reverse=False)
    edges_sorted=[k[0] for k in E]

    s=0 # number of edges of the minimal spanning tree
    G_mst=Graph(G.nodes)
    parent=UnionFind(G.nodes) # Initially, each node is its parent.
    for edge in edges_sorted: # We go through the edges in an increasing order of power 
        node1=edge[0]
        node2=edge[1]
        a=parent.find(node1)
        b=parent.find(node2)
        if a!=b: 
            # if a and b have diffrent parents, so adding the edge won't create a cycle.
            for k  in G.graph[node1]:
                if k[0]==node2:
                    p=k[1] # p is the power of the edge.
                    d=k[2] # d is the distance of the edge.
            s+=1
            G_mst.add_edge(node1,node2,p,d)
            parent.union(node1,node2) # Since node1 and node2 are related by edge, 
                                      # they're in the same component and they should have the same parent
    G_mst.nb_edges=s
    return G_mst

""" Complexity analysis: 
The time complexity of kruskal's algorithm is O(E*logV).
"""
G=graph_from_file_4("/home/onyxia/Projet-de-programmation/input/network.1.in")

###### QUESTION 13

# Testing the kruskal method on the small graphs

# for i in ['0','1','2','3','4']:
#     graphname="/home/onyxia/work/Projet-de-programmation/input/network.0"+i+".in"
#     G=graph_from_file_4(graphname)
#     print(kruskal(G))

# We have the results we expected. 

###### QUESTION 14


def rank(A):
    R=dict(dict([(n, 0) for n in A.nodes]))
    max_nodes=0
    for v in A.nodes:
        if len(A.graph[v]) > max_nodes:
            root=v
            max_nodes=len(A.graph[v])
    L=[root]
    while L!=[]:
        L2=[]
        for a in L:
            for k in A.graph[a]:
                if (R[k[0]] ==0) and (k[0]!=root):
                    R[k[0]] = R[a] + 1
                    L2.append(k[0])
        L=L2
    return R





""" Complexity analysis:
The complexity of rank is O(E*V).
"""

# def smallest_common_ancestor(A,t):
#     a=t[0]
#     b=t[1]
#     while a!=b:
#         if rank(A)[b] >= rank(A)[a]:
#             for k in A.graph[b]:
#                 if rank(A)[k[0]] < rank(A)[b]:
#                     b=k[0]
#         else: 
#             a,b=b,a
#     return a

""" Complexity analysis:
In worst case scenerios, we calculate the rank of all nodes, V times.
The complexity is therefore O(E²*V).
"""

def min_power_tree(A,R,t):
    a1,a2=t[0],t[1]
    L1,L2=[a1],[a2]
    p=0
    if R[a1] > R[a2]:
        a1,a2=a2,a1
    while R[a1]!=R[a2]:
        for k in A.graph[a2]:
            if R[a2] > R[k[0]]:
                L2.append(k[0])
                a2=k[0]
                if k[1] > p:
                    p=k[1]

    while a1!=a2:
        for k in A.graph[a1]:
            if R[a1] > R[k[0]]:
                L1.append(k[0])
                a1=k[0]
                if k[1] > p:
                    p=k[1]
        for k in A.graph[a2]:
            if R[a2] > R[k[0]]:
                L2.append(k[0])
                a2=k[0]
                if k[1] > p:
                    p=k[1]
    L2.pop()
    path = L1+L2[::-1]
    return path,p



###### QUESTION 15

""" Complexity analysis:
According to the previous analysis, the complexity of min_power_tree is still O(V) if we only consider V. 
"""

import sys 
sys.setrecursionlimit(10**9)


# Time estimation 

def necessary_time_tree(filename1,filename2):
    """Returns the necessary time to find all the minimal power path if exists 
    for all the routes in the graph using the minimal spanning tree.

    Args:
        filename (str): the path of the graph file 

    Returns:
        float: the necessary time in seconds
    """
    G=graph_from_file_4(filename1)
    routes=route_from_file(filename2)
    A=kruskal(G) # We don't count the pre-processing time. 
    a=time.perf_counter()
    for t in routes:
        mP=min_power_tree(A, t)
    b=time.perf_counter()
    return b-a

# print(necessary_time_tree("/home/onyxia/Projet-de-programmation/input/network.1.in",
#                      "/home/onyxia/Projet-de-programmation/input/routes.1.in"))

# print(necessary_time_tree("/home/onyxia/Projet-de-programmation/input/network.2.in",
#                      "/home/onyxia/Projet-de-programmation/input/routes.2.in"))

# print(necessary_time_tree("/home/onyxia/Projet-de-programmation/input/network.3.in",
#                      "/home/onyxia/Projet-de-programmation/input/routes.3.in"))



# Creating the files containing the minimal powers of routes for route.1, route.2 and route.3
for i in [4]:
    f = open("/home/onyxia/Projet-de-programmation/delivery_network/route."+str(i), "w")
    graphname="/home/onyxia/Projet-de-programmation/input/network." + str(i) +".in"
    routename="/home/onyxia/Projet-de-programmation/input/routes." + str(i) +".in"
    G=graph_from_file_4(graphname)
    c=time.perf_counter()
    A=kruskal(G)    
    a=time.perf_counter()
    print(a-c)
    route=route_from_file(routename)
    d=time.perf_counter()
    R=rank(A)
    e=time.perf_counter()
    print(e-d)
    for t in route:
        mP=min_power_tree(A,R,t)[1]
        f.write(str(mP) + '\n')
    b=time.perf_counter()
    print(b-e)
    f.close()


""" Other methodes with higher complexities : 
The following code was the first thing we wrote for questions 3, 4, 5 and 6.
It works but we gave it up for its exponentinal complexity.
"""

# ###### Funcions used in questions 3, 5 et 6
# """The following code returns, given two nodes v and u and a Graph G
#     all the paths the truck could possibly cover starting its journey from v looking for u.
#     The journey could end - in the destination u 
#                           - in the starting point v (we spot those with 'STOP')
#                           - in the end of a road (a node with one connexion)
# """
# def end(G,u,H):
#     """Checks the stopping condition of the recursive function all_paths

#     Args:
#         G (Graph): the graph the truck is navigating
#         u (integer): the destination node
#         H (list): a list of partial paths the truck could cover 

#     Returns:
#         Boolean: True if there are no more paths the truck could cover and all_paths should stop:
#         All paths in H are either - ended in the destination u 
#                             or    - ended in 'STOP'
#                             or    - ended in a single connexion node

#         False otherwise.   
#     """
#     if len(H)==1:
#         return False
#     for L in H: 
#         if (L[-1]!=u) and (L[-1]!='STOP') and (len(G.graph[L[-1]])!=1):
#             return False
#     return True

# def all_paths(G,v,u,H):
#     """a recursive function that given all first n possible steps 
#     the truck could take starting from v and returns all first n+1 possible steps
#     and stops when end is True (no further possible steps that could lead to u).
#     It's a choice tree.
#     Args:
#         G (Graph): the graph the truck is navigating 
#         v (integer): the starting point
#         u (integer): the detination
#         H (list): list of partial paths

#     Returns:
#         H: a list of possible paths (lists) starting from v 
#     """
#     if end(G,u,H)==True:
#         return H
#     i=0
#     # i is the level of the branch in the choice tree
#     while (i <len(H)): 
#         if H[i][-1]==u:
#             i+=1
#             continue
#         elif (H[i][-1]==H[i][0]) and (len(H[i])>1):
#                 H[i].append('STOP')
#                 i+=1
#                 continue
#         elif H[i][-1]=='STOP':
#             i+=1
#             continue
#         s=0  
#         for k in G.graph[H[i][-1]]: 
#             if (k[0] in H[i][1:])==False: 
#                 # We only allow v to be repeated in a path in order to spot a path that leads to the starting point
#                 H.insert(i+1,H[i]+[k[0]])
#                 s+=1 #s is the number of the new branches 'les branches filles'
#         if s>0:        
#             H.pop(i) # 'les branches filles' replace 'la branche mère'
#             i+=s # we move on to the next 'branche mère'
#         else:
#             i+=1 
#     #print(H)
#     return all_paths(G,v,u,H)

# def all_paths_u(G,v,u):
#     """Uses all_paths to return all possible paths 
#     starting from v ending in u

#     Args:
#         G (Graph): the graph the truck is navigating
#         v (integer): the starting node
#         u (integer): the destination node 

#     Returns:
#         a list of possible paths relating the starting node v and the destination u
#     """
#     H=all_paths(G,v,u,[[v]])
#     P=[]
#     for L in H:
#         if L[-1]==u:
#             P.append(L)
#     return P

# def power(G,L):
#     """Returns the minimal power a truck should have to be able to cover the path L"""
#     max=0
#     for i in range(len(L)-1): 
#         for k in G.graph[L[i]]:
#             if k[0]==L[i+1]:
#                 if k[1] > max:
#                     max=k[1]
#     return max

# ###### QUESTION 3
# def get_path_with_power(G,p,t):
#     H=all_paths_u(G,t[0],t[1])
#     j=0
#     while (p<power(G,H[j])) and (j<len(H)-1):
#             j+=1
#     if j==len(H):
#         return None
#     else:
#         print("Le chemin est possible")
#         return H[j]


# ###### QUESTION 5
# def distance(G,L):
#     """Returns the distance of the path L"""
#     s=0
#     for i in range(len(L)-1): 
#         for k in G.graph[L[i]]:
#             if k[0]==L[i+1]:
#                 s+=k[2]
#     return s

# def get_path_distance_min(G,p,t):
#     if get_path_with_power(G,p,t)==None:
#         return None
#     H=all_path_u(G,t[0],t[1])
#     d=distance(G,H[0])
#     for L in H:
#         if power(G,L)>p:
#             continue
#     else:
#         if distance(G,L)<d:
#             d=distance(G,L)
#             j=H.index(L)
#             return H[j]

# ###### QUESTION 6 
# def min_power(G,v,u):
#     Paths=all_paths_u(G,v,u)
#     if Paths==[]:
#         return "Le chemin n'est pas possible"
#     else: 
#         Powers=[power(G,L) for L in Paths]
#         pw=min(Powers)
#         i=Powers.index(pw) 
#         return Paths[i],pw

# Problème du sac à dos:
# x[i][j]==1 si le camion i correspond à une route j donc le problème revient à trouver le vecteur x=(x[1,1],..x[n,m])
# W-->B est la limite budgétaire
# w[i] est le coût du camion i
# Le profit de la route j que prend le camion est p[j]
# Il faut que sum(w[i]*x[i,j]<W) et maximiser sum(p[j]*x[i,j])
# On commence par trier les coûts


B=25*((10)**9)

def trucks_from_file(): 
    T=[]
    for i in range(3):
        graphname="/home/onyxia/Projet-de-programmation/input/trucks." + str(i) + ".in"
        f = open(graphname, "r")
        lines=f.readlines()
        L=[]
        for i in range(1,len(lines)):
            L.append(lines[i].split())
        L.pop(0)
        for line in L:
            T.append([int(line[0]),int(line[1])])

    T_sorted = sorted(T, key=itemgetter(1) , reverse=False)
    return T_sorted

def routes_from_file_2(graphname):
    R=[]
    f = open(graphname, "r")
    lines=f.readlines()
    L=[]
    for i in range(1,len(lines)):
        L.append(lines[i].split())
    L.pop(0)
    for line in L:
        R.append([int(line[0]),int(line[1]),int(line[2])])
    R_sorted = sorted(R, key=itemgetter(2),reverse=True)
    return R_sorted

T=trucks_from_file()
R=routes_from_file_2("/home/onyxia/Projet-de-programmation/input/routes.1.in")
G=graph_from_file_4("/home/onyxia/Projet-de-programmation/input/network.1.in")
def greedy(T,R):
    D=dict([(t,[]) for t in range(len(T))])
    R_assigned=[]
    C=0
    while C<=B:
        for t in range(len(T)):
            for r in range(len(R)):
                if (T[t][0] <= min_power(G, (R[r][0],R[r][1]))[1]) and (r not in R_assigned):
                    D[t].append((R[r][0],R[r][1]))
                    R_assigned.append(r)
                    C = C + T[t][1]
    return D

D=greedy(T,R)

def sac_à_dos(T,R):
    Object=[]
    ratio=[]
    for t in range(len(T)):
        for r in range(len(R)):
            if T[t][0] <= min_power(G, (R[r][0],R[r][1]))[1]:
                Object.append((t,r))
                ratio.append(R[r][2]/T[t][1])
    O=sorted(Object, key=ratio, reverse=False)
    L=[]
    C=0
    for combi in O:
        if C<=B:
            L.append(combi)
            C = C + T[t][1]
    return L

G=graph_from_file_4("/home/onyxia/Projet-de-programmation/input/network.1.in")
A=kruskal(G)
print(A)
route=route_from_file("/home/onyxia/Projet-de-programmation/input/routes.1.in")
for t in route:
    print(min_power_tree(A,t))
    


