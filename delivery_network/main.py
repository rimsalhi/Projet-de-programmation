from graph import Graph, graph_from_file
from operator import itemgetter 



###### QUESTION 2

def explore(G,v,s):
    """Returns the connected component to which v belongs.
    Args:
        G (Graph): 
        v (integer): a node in the Graph G
        s (set): initially empty updated each time the function is called. 
    """
    s.add(v) # v marked as visited.
    for k in G.graph[v]:
        if (k[0] in s)==False:
            explore(G,k[0],s)
    return s 

def connected_components_set(G):
    """Uses the explore function to determine the connected component of each node.
    The type Set of each component, being unordered, allows us to avoid redundancy.

    Args:
        G (Graph)

    Returns:
        list: a list of sets, each set is a connected component.
    """
    L=[]
    for v in G.nodes:
        s=set()
        if (explore(G,v,s) in L)==False:
            L.append(explore(G,v,s))
    return L 


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
    """Returns a list of edges. Each edge is a list of two nodes.
    and a list of tuples (edge, power of the edge)

    Args:
        G (Graph) 
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
        G (Graph) 
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


###### QUESTION 7 

# import graphviz #installed with conda install python-graphviz
# import os
# os.environ["PATH"]+=os.pathsep+'C:\Program Files\Graphviz\bin' #to be replaced with the path of the bin of Graphviz on the desktop once dowloaded.

# def G_rep(G,t):
#     P= min_power(G,t)[0]
#     EP=[] # the edges of the minimal power path.
#     for i in range(len(P)-1):
#         EP.append({P[i],P[i+1]})
#     v=t[0]
#     u=t[1]
#     f = graphviz.Graph('Fig2')
#     H=[]
#     for node in G.graph:
#         for k in G.graph[node]:
#             if ({node,k[0]} in H)==False:
#                 if (node in P) and (k[0] in P):
#                     f.node(str(node), fillcolor='red', style='filled')
#                     f.node(str(k[0]), fillcolor='red', style='filled')
#                 if {node,k[0]} in EP:
#                     f.edge(str(node), str(k[0]), label= str(k[1]), color='red') 
#                 else:
#                     f.edge(str(node), str(k[0]), label= str(k[1]))
#                 H.append({node,k[0]})
#     f.node(str(v), label=str(v)+': Start', fillcolor='red', style='filled')
#     f.node(str(u), label=str(u)+': Finish', fillcolor='red', style='filled')
#     f.view()

# #The representation of the graph and the minimal power path of network00: rep_graph00.gv.pdf
# g=graph_from_file_4("/home/onyxia/Projet-de-programmation/input/network.1.in")
# G_rep(g,(2,20))


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
    nb_route=0
    for t in routes:
        mP=min_power(G,t)
        nb_route = nb_route + 1
        if nb_route == 10:
            b=time.perf_counter()
            return b-a

# print(necessary_time("/home/onyxia/Projet-de-programmation/input/network.1.in",
#                    "/home/onyxia/Projet-de-programmation/input/routes.1.in"))

# print(necessary_time("/home/onyxia/Projet-de-programmation/input/network.2.in",
#                      "/home/onyxia/Projet-de-programmation/input/routes.2.in"))


###### QUESTION 12

class UnionFind:
    def __init__(self, nodes=[]):
        parent=dict()
        for n in nodes:
            parent[n]=n
        self.parent=parent
        self.rank=dict([(n,0) for n in nodes])
        
    # # The naive find 
    # def find(self,n):
    #     if self.parent[n]==n:
    #         return n
    #     else: 
    #         return self.find(self.parent[n])
    
    def find_path_compression(self,n):
        if self.parent[n]==n:
            return n
        else: 
            self.parent[n] = self.find(self.parent[n])
            return self.parent[n]
    
    # # The naive union
    # def union(self, m, n):
    #     self.parent[m]= n

    def union_by_rank(self, m, n):
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
        a=parent.find_path_compression(node1)
        b=parent.find_path_compression(node2)
        if a!=b: 
            # if a and b have diffrent parents, so adding the edge won't create a cycle.
            for k  in G.graph[node1]:
                if k[0]==node2:
                    p=k[1] # p is the power of the edge.
                    d=k[2] # d is the distance of the edge.
            s+=1
            G_mst.add_edge(node1,node2,p,d)
            parent.union_by_rank(node1,node2) # Since node1 and node2 are related by edge, 
                                      # they're in the same component and they should have the same parent
    G_mst.nb_edges=s
    return G_mst


###### QUESTION 13

# Testing the kruskal method on the small graphs

# for i in ['0','1','2','3','4']:
#     graphname="/home/onyxia/work/Projet-de-programmation/input/network.0"+i+".in"
#     G=graph_from_file_4(graphname)
#     print(kruskal(G))

# We have the results we expected. 


###### QUESTION 14

def rank(A):
    """Returns a dictionary: the keys are the nodes of the tree A.
    The value associated to a node is its rank : 
    the number of edges between the node and the root."""

    R=dict(dict([(n, 0) for n in A.nodes]))
    # We choose the root to be a node of the most connexions to have minimal ranks.
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

def min_power_tree(A,R,t):
    """Returns the unique path relating the extremities of t and its power.

    Args:
        A (Graph): The minimal power spanning tree
        R (dict): The dictionary of ranks 
        t (tuple): the route
    """
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

import sys 
sys.setrecursionlimit(10**9)

# # Creating the files containing the minimal powers of routes for route.1, route.2 and route.3
# # with time estimations.

# for i in [1,2,3,4]:
#     f = open("/home/onyxia/Projet-de-programmation/delivery_network/route."+str(i), "w")
#     graphname="/home/onyxia/Projet-de-programmation/input/network." + str(i) +".in"
#     routename="/home/onyxia/Projet-de-programmation/input/routes." + str(i) +".in"
#     G=graph_from_file_4(graphname)
#     a=time.perf_counter()
#     A=kruskal(G)    
#     b=time.perf_counter()
#     print(b-a)
#     route=route_from_file(routename)
#     R=rank(A)
#     c=time.perf_counter()
#     for t in route:
#         mP=min_power_tree(A,R,t)[1]
#         f.write(str(mP) + '\n')
#     d=time.perf_counter()
#     print(d-c)
#     f.close()


###### QUESTION 18 

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


def natural(graphname, routesname):
    T=trucks_from_file()
    R=routes_from_file_2(routesname)
    G=graph_from_file_4(graphname)
    A=kruskal(G)
    Ranks=rank(A)
    D=dict([(t,[]) for t in range(len(T))])
    R_assigned=[]
    C=0
    u=0
    t=0
    while (C<=B) and (t <len(T)):
        for r in range(len(R)):
            if (T[t][0] >= min_power_tree(A, Ranks, (R[r][0],R[r][1]))[1]) and (r not in R_assigned):
                D[t].append((R[r][0],R[r][1]))
                R_assigned.append(r)
                C = C + T[t][1]
                u = u + R[r][2]
        t = t + 1
    return D,u

# a=time.perf_counter()
# print(natural("/home/onyxia/Projet-de-programmation/input/network.2.in",
#       "/home/onyxia/Projet-de-programmation/input/routes.2.in")[1])
# b=time.perf_counter()
# print(b-a)

def glouton(graphname,routesname):
    G=graph_from_file_4(graphname)
    T=trucks_from_file()
    R=routes_from_file_2(routesname)
    A=kruskal(G)
    Ranks=rank(A)
    Object=[]
    ratio=[]
    D=dict([(t,[]) for t in range(len(T))])
    u=0
    for t in range(len(T)):
        for r in range(len(R)):
            if T[t][0] >= min_power_tree(A, Ranks, (R[r][0],R[r][1]))[1]:
                ratio= R[r][2]/T[t][1]
                Object.append((t,r,ratio))
    O=sorted(Object, key=itemgetter(2), reverse=False)
    C=0
    i=0
    R_assigned=[]
    while (C<=B) and (i<len(O)):
        t=O[i][0]
        r=O[i][1]
        if r not in R_assigned:
            D[t].append((R[r][0],R[r][1]))
            C = C + T[t][1]
            i = i +1
            u = u + R[r][2]
    return D,u

# a=time.perf_counter()
# print(glouton("/home/onyxia/Projet-de-programmation/input/network.1.in",
#                "/home/onyxia/Projet-de-programmation/input/routes.1.in"))
# b=time.perf_counter()
# print(b-a)

def approx_50(graphname,routesname):
    (D1,V1)=natural(graphname, routesname)
    (D2,V2)=glouton(graphname, routesname)
    if V1 > V2:
        return (D1,V1)
    else:
        return (D2,V2)
def add(Object,o,L):
    if L==[]:
        return [([o], Object[o][0], Object[o][1])]
    else:
        H=[]
        for sol in L:
            if sol[1] >= B:
                continue
            l=sol[0]
            l2= l + [o]
            c=sol[1]
            c2= c + Object[o][0]
            u=sol[1]
            u2=u + Object[o][1]
            sol2=(l2,c2,u2)
            H.append (sol2)
        return H
def exact(graphname,routesname):
    G=graph_from_file_4(graphname)
    T=trucks_from_file()
    R=routes_from_file_2(routesname)
    A=kruskal(G)
    Ranks=rank(A)
    Object=dict()
    for t in range(len(T)):
        for r in range(len(R)):
            if T[t][0] >= min_power_tree(A, Ranks, (R[r][0],R[r][1]))[1]:
                Object[(t,r)]=(T[t][1],R[r][2])
    L=[]
    for o in Object:
        L= L + add(Object,o,L) 
    # for sol in L:
    #     if sol[1] > B:
    #         L.remove(sol)
        H=[]
        for sol in L:
            test=True
            for i in range(len(sol[0])):
                for j in range(len(sol[0])):
                    if  (sol[0][i][1]==sol[0][j][1]) and (sol[0][i][0]!=sol[0][j][0]):
                        test=False
                        break
                if test==False:
                    break
            if test==True:
                H.append(sol)
    S=sorted(L, key=itemgetter(2), reverse=True)
    return S[0][1], S[0][2]
a=time.perf_counter()
print(exact("/home/onyxia/Projet-de-programmation/input/network.1.in",
               "/home/onyxia/Projet-de-programmation/input/routes.1.in"))
b=time.perf_counter()
print(b-a)


# def rep(G,s):
#     f = graphviz.Graph('rep_graph'+str(len(s))+'png')
#     H=[]
#     for node in G.graph:
#         for k in G.graph[node]:
#             if node in s:
#                 f.node(str(node), fillcolor='red', style='filled')
            
#             if {str(node), str(k[0])} not in H:
#                 f.edge(str(node), str(k[0]))
#                 H.append({str(node), str(k[0])})
#     f.view()

# def explore(G,v,s):
#     if s=={1, 2, 3, 4, 5, 7, 10}:
#         rep(G,s)
#         print(s)
#     """A recursive function that updates a set s (initially empty) 
#     adding each time a node that isn't in s but connected to v 
#     then moves to explore the connections of the added node.

#     Args:
#         G (Graph): 
#         v (integer): a node in the Graph G
#         s (set): initially empty 

#     Returns:
#         set: containing all the nodes from G connected to v
#     """
#     s.add(v)
#     for k in G.graph[v]:
#         if (k[0] in s)==False:
#             explore(G,k[0],s)
#     return s 

# G=graph_from_file("/home/onyxia/Projet-de-programmation/input/network.00.in")
# explore(G,1,set())


# def rep_graph(G,ch):
#     f = graphviz.Graph('Fig3_network1'+ch)
#     H=[]
#     for node in G.graph:
#         for k in G.graph[node]:
#             if {str(node), str(k[0])} not in H:
#                 f.edge(str(node), str(k[0]))
#                 H.append({str(node), str(k[0])})
#     # f.view()

# Fig3
# G=graph_from_file_4("/home/onyxia/Projet-de-programmation/input/network.1.in")
# rep_graph(G, '')
# A=kruskal(G)
# rep_graph(A, '_tree')


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
