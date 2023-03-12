from graph import Graph, graph_from_file


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
            if ({node,k[0]} in H)==False:
                H.append({node,k[0]})
    return H

def min_power(G,t):
    """Starts by determining the maximal power of the edges PMax. 
    Then, using a dichotomous search on [Pmin,PMax], looks for 
    the minimal power with whitch the journey t is possible. 

    Args:
        G (Graph): 
        t (tuple): the route

    Returns:
        tuple: composed of - the path with the minimal power and its power if a path exists.
                           - None and the median power
    """
    #PW is the list of disctinct powers in the graph sorted in an increasing order.
    PW=[]
    for edge in edges(G):
        edge2=list(edge)
        for k in G.graph[edge2[0]]:
            if (k[0]==edge2[1]) and (k[1] not in PW):
                PW.append(k[1])
    PW.sort()
    #The dichotomous search for the path with minimal power.
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

    return (get_path_with_power(G, PW[b],t) ,PW[b])

"""Complexity analysis: If we consider P to be the number of distinct powers in the graph:
the complexity of the construction of PW is O(P) and
the complexity of the dichotomous search is O(log2(P)*(V+E)).
Therefore, the complexity of the whole algorithm is O(P*(V+E)). 
If we only consider V and E, we conclude that the complexity is O(V+E).
"""


###### QUESTION 7 

import graphviz #installed with conda install python-graphviz
import os
os.environ["PATH"]+=os.pathsep+'C:\Program Files\Graphviz\bin' #to be replaced with the path of the bin of Graphviz on the desktop once dowloaded.

def G_rep(G,t):
    P= min_power(G,t)[0]
    v=t[0]
    u=t[1]
    f = graphviz.Graph('rep_graph00')
    H=[]
    for node in G.graph:
        for k in G.graph[node]:
            if ({node,k[0]} in H)==False:
                if (node in P) and (k[0] in P):
                    f.node(str(node), fillcolor='red', style='filled')
                    f.node(str(k[0]), fillcolor='red', style='filled')
                    f.edge(str(node), str(k[0]), label= str(k[1]), color='red') 
                else:
                    f.edge(str(node), str(k[0]), label= str(k[1]))
                H.append({node,k[0]})
    f.node(str(v), label=str(v)+': Start', fillcolor='red', style='filled')
    f.node(str(u), label=str(u)+': Finish', fillcolor='red', style='filled')
    f.view()

#The representation of the graph and the minimal power path of network00: rep_graph00.gv.pdf
# g=graph_from_file_4("/home/onyxia/work/Projet-de-programmation/input/network.00.in")
# G_rep(g,(1,5))


###### QUESTION 10

def graph_from_file_route(filename):
    """Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n'
        The next n lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
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
    x=L.pop(0)
    s0={int(line[0]) for line in L}
    s1={int(line[1]) for line in L}
    M=list(s1.union(s0))
    G=Graph(M)
    G.nb_edges=int(x[0])
    for line in L:
        if line[0]!=line[1]:
            G.add_edge(int(line[0]),int(line[1]),int(line[2]))
    return G

import time
import itertools

def necessary_time(filename):
    """Returns the necessary time to find all the minimal power path if exists 
    for all the routes in the graph.

    Args:
        filename (str): the path of the graph file 

    Returns:
        float: the necessary time in seconds
    """
    G=graph_from_file_route(filename)
    a=time.perf_counter()
    for t in itertools.combinations(G.graph, 2):
        mP=min_power(G,t)
    b=time.perf_counter()
    return b-a

#print(necessary_time("/home/onyxia/work/Projet-de-programmation/input/routes.1.in"))
# Determining the minimal power of all routes in route.1 and their associated paths takes about 26s.


###### QUESTION 12

def find(parent,n):
    """ Returns the parent of n; the representative of the connected component it belongs to."""
    if parent[n]==n:
        return n
    else:
         return find(parent, parent[n])

def union (parent,n,m):
    """ Modifies the dictionary parent in order the make n the parent of m 
    when they belong to the same connected component."""
    parent[m]=n
def tri_edges(L): #trier les edges !!!!!!!!!!!!!!!!!

def kruskal(G):
    """Returns the minimal spanning tree of the graph G using the Kruskal algorithm.
    """
    G_mst=Graph(G.nodes)
    parent={n: n for n in G.nodes} # Initially, each node is its parent.
    for edge in tri(edges(G)): # We go through the edges in an increasing order of power 
        edge2=list(edge)
        node1=edge2[0]
        node2=edge2[1]
        a=find(parent,node1)
        b=find(parent,node2)
        if a!=b: # if a and b have diffrent parents, so adding the edge won't create a cycle.
            for k  in G.graph[node1]:
                if k[0]==node2:
                    p=k[1] # p is the power of the edge.
                    d=k[2] # d is the distance of the edge.
            G_mst.add_edge(node1,node2,p,d)
            union(parent,node1,node2) # Since node1 and node2 are related by edge, 
                                      # they're in the same component and they should have the same parent
    return G_mst

""" Complexity analysis: 
"""


###### QUESTION 14

def rank(A,v):
    if v==A.nodes[0]:
        return 0
    for i in range(len(A.nodes)):
        for k in A.graph[A.nodes[i]]:
            if k[0]==v:
                return 1 + rank(A,A.nodes[i])

def youngest_common_ancestor(A,t):
    a=t[0]
    b=t[1]
    while a!=b:
        if rank(A,b) >= rank(A,a):
            for k in A.graph[b]:
                if rank(A,k[0]) < rank(A,b):
                    b=k[0]
        else: 
            a,b=b,a
    return a

def min_power_tree(A,t):
    a1,a2=t[0],t[1]
    L1,L2=[a1],[a2]
    x=youngest_common_ancestor(A, t)
    while (a1!=x) or (a2!=x):
        for k in G.graph[a1]:
            if rank (A,a1) > rank(A,k[0]):
                L1.append(k[0])
                a1=k[0]
        for k in G.graph[a2]:
            if rank(A,a2) > rank(A,k[0]):
                L2.append(k[0])
                a2=k[0]
    L2.pop()
    return L1+L2[::-1]
#ajouter la puissance 


###### QUESTION 15 

""" Complexity analysis: 
"""

def necessary_time_tree(filename):
    """Returns the necessary time to find all the minimal power path if exists 
    for all the routes in the graph using the minimal spanning tree.

    Args:
        filename (str): the path of the graph file 

    Returns:
        float: the necessary time in seconds
    """
    G=graph_from_file_route(filename)
    a=time.perf_counter()
    A=kruskal(G)
    for t in itertools.combinations(G.graph, 2):
        mP=min_power_tree(A,t)
    b=time.perf_counter()
    return b-a


#print(necessary_time_tree("/home/onyxia/work/Projet-de-programmation/input/routes.1.in"))
# Determining the minimal power of all routes in route.1 and their associated paths takes about 26s.





        


















###### Fonctions utilisées dans les questions 3, 5 et 6
"""The following code returns, given two nodes v and u and a Graph G
    all the paths the truck could possibly cover starting its journey from v looking for u.
    The journey could end - in the destination u 
                          - in the starting point v (we spot those with 'STOP')
                          - in the end of a road (a node with one connexion)
"""
def end(G,u,H):
    """Checks the stopping condition of the recursive function all_paths

    Args:
        G (Graph): the graph the truck is navigating
        u (integer): the destination node
        H (list): a list of partial paths the truck could cover 

    Returns:
        Boolean: True if there are no more paths the truck could cover and all_paths should stop:
        All paths in H are either - ended in the destination u 
                            or    - ended in 'STOP'
                            or    - ended in a single connexion node

        False otherwise.   
    """
    if len(H)==1:
        return False
    for L in H: 
        if (L[-1]!=u) and (L[-1]!='STOP') and (len(G.graph[L[-1]])!=1):
            return False
    return True

def all_paths(G,v,u,H):
    """a recursive function that given all first n possible steps 
    the truck could take starting from v and returns all first n+1 possible steps
    and stops when end is True (no further possible steps that could lead to u).
    It's a choice tree.
    Args:
        G (Graph): the graph the truck is navigating 
        v (integer): the starting point
        u (integer): the detination
        H (list): list of partial paths

    Returns:
        H: a list of possible paths (lists) starting from v 
    """
    if end(G,u,H)==True:
        return H
    i=0
    # i is the level of the branch in the choice tree
    while (i <len(H)): 
        if H[i][-1]==u:
            i+=1
            continue
        elif (H[i][-1]==H[i][0]) and (len(H[i])>1):
                H[i].append('STOP')
                i+=1
                continue
        elif H[i][-1]=='STOP':
            i+=1
            continue
        s=0  
        for k in G.graph[H[i][-1]]: 
            if (k[0] in H[i][1:])==False: 
                # We only allow v to be repeated in a path in order to spot a path that leads to the starting point
                H.insert(i+1,H[i]+[k[0]])
                s+=1 #s is the number of the new branches 'les branches filles'
        if s>0:        
            H.pop(i) # 'les branches filles' replace 'la branche mère'
            i+=s # we move on to the next 'branche mère'
        else:
            i+=1 
    #print(H)
    return all_paths(G,v,u,H)

def all_paths_u(G,v,u):
    """Uses all_paths to return all possible paths 
    starting from v ending in u

    Args:
        G (Graph): the graph the truck is navigating
        v (integer): the starting node
        u (integer): the destination node 

    Returns:
        a list of possible paths relating the starting node v and the destination u
    """
    H=all_paths(G,v,u,[[v]])
    P=[]
    for L in H:
        if L[-1]==u:
            P.append(L)
    return P

def power(G,L):
    """Returns the minimal power a truck should have to be able to cover the path L"""
    max=0
    for i in range(len(L)-1): 
        for k in G.graph[L[i]]:
            if k[0]==L[i+1]:
                if k[1] > max:
                    max=k[1]
    return max

###### QUESTION 3
def get_path_with_power(G,p,t):
    H=all_paths_u(G,t[0],t[1])
    j=0
    while (p<power(G,H[j])) and (j<len(H)-1):
            j+=1
    if j==len(H):
        return None
    else:
        print("Le chemin est possible")
        return H[j]


###### QUESTION 5
def distance(G,L):
    """Returns the distance of the path L"""
    s=0
    for i in range(len(L)-1): 
        for k in G.graph[L[i]]:
            if k[0]==L[i+1]:
                s+=k[2]
    return s

def get_path_distance_min(G,p,t):
    if get_path_with_power(G,p,t)==None:
        return None
    H=all_path_u(G,t[0],t[1])
    d=distance(G,H[0])
    for L in H:
        if power(G,L)>p:
            continue
    else:
        if distance(G,L)<d:
            d=distance(G,L)
            j=H.index(L)
            return H[j]

###### QUESTION 6 
def min_power(G,v,u):
    Paths=all_paths_u(G,v,u)
    if Paths==[]:
        return "Le chemin n'est pas possible"
    else: 
        Powers=[power(G,L) for L in Paths]
        pw=min(Powers)
        i=Powers.index(pw) 
        return Paths[i],pw




A=Graph([0,1,3,4,5,6,7,12,13,10])
A.add_edge(0,3,0)
A.add_edge(0,1,0)
A.add_edge(4,3,0)
A.add_edge(4,12,0)
A.add_edge(5,3,0)
A.add_edge(10,5,0)
A.add_edge(13,5,0)
A.add_edge(6,1,0)
A.add_edge(7,1,0)
print(A)
print(rank(A,13))    
















print(min_power(B,1,5))
G_rep(B, 1, 5)

# problème s'il y a un cycle interne : voir B 
# La fonction fin a pour but de vérifier la condition d'arrêt de la fonction récursive
# S'il reste plus des choix à faire (on est tombé sur u ou on est tombé sur la case de départ)
        # on passe à la branche suivante, sinon on poursuit  
 
#Un exemple simple de graphe 
B=Graph([1,2,3,4,5,6,12])
B.add_edge(1,4,0)
B.add_edge(4,5,0)
B.add_edge(1,2,0)
B.add_edge(1,3,0)
B.add_edge(6,12,0)
print(B)       

s=set()
print(explore(B,1,s))           
print(connected_components_set(B))

print(graph_from_file_4("/home/onyxia/work/lost+found/network.04.in"))
# Les fichiers 00 01 02 et 03 présentent dans la première ligne
# le nombre de noeuds puis le nombre d'arêtes, c'est inversé dans le fichier 0' 
#Question 5

def explore2(G,v,L):
    for k in G.graph[v]:
        if (k[0] in L)==False:
            L.append(k[0])
            explore2(G,k[0],L)
    return L 

#g = graph_from_file("/home/onyxia/work/input /network.00.in")
#print(g)


H=[[1]]
# Prob de cycle interne : qui sépare le départ et l'arrivée
# le bonhomme soit se trouve perdu 
# (chemin qui finit par un noeud à plusieurs connexions qui n'est pas le départ ou l'arrivée ) : fin jamais true
# soit se trouve piégé dans une boucle infinie avec if (k[0]!=H[i][-1])==False:
# lorsqu'on autorise tout pas qui n'est pas de la marche arrière; ce n'est pas sufisant 
 
B=Graph([1,2,3,4,5,6,12,13,14])
B.add_edge(4,6,0)
B.add_edge(6,12,0)
B.add_edge(2, 5, 0)
B.add_edge(6, 5, 0)
#B.add_edge(4,2,0)
# on a chemin qui finit par 5 parce que pour revenir à la case de départ, il est obligé de passer par des chemins déjà parcourus
B.add_edge(14,1,0)
B.add_edge(13,14,0)
B.add_edge(1,4,0)
B.add_edge(1,2,10)
B.add_edge(1,3,0)
B.add_edge(1,13,0)
print(B) 
print(get_path_with_power(B,0,(1,5)))
print(min_power(B,(1,5)))
 
#import copy 
# def parcours_en_prof(A,a):
#     D=copy.deepcopy(A) 
#     if (A[a]==[]) or (not(a in A)) or (a==None):
#         return []
#     elif len(A[a])==1:
#         del D[a]
#         for k in A[A[a][0][0]]:
#             if k[0]==a:
#                 D[A[a][0][0]].remove(k)
#         return [a,A[a][0][0]]+parcours_en_prof(D,A[a][0][0])
#     else: 
#         L=[]
#         for i in range(len(A[a])): 
#             D=copy.deepcopy(A)
#             #We isolate each branch coming out of a
#             D[a]=[A[a][i]]
#             for j in range(len(A[a])):
#                 if j!=i:
#                     del D[A[a][j][0]]
#                     for k in A[A[a][j][0]]:
#                         if k[0]!=a:
#                             del D[k[0]]  
#             L+=parcours_en_prof(D,a)+parcours_en_prof(D,a)[-1:1:-1]
#         return L 
#print(parcours_en_prof(A.graph, 1))

