from graph import Graph, graph_from_file

###### QUESTION 2

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
#             #on va isoler chaque branche sortant de a
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

###### QUESTION 4
def graph_from_file_4(filename):
    """Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'm n'
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
    M=[i for i in range(1,int(L[0][1])+1)]
    print(M)
    G=Graph(M)
    G.nb_edges=int(L[0][0])
    L.pop(0)
    for line in L:
        if len(line)==4: 
            d=int(line[3])
        else: 
            d=1

        G.add_edge(int(line[0]),int(line[1]),int(line[2]),d)
    return G

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

###### QUESTION 7 
import graphviz
import os
os.environ["PATH"]+=os.pathsep+'C:\Program Files\Graphviz\bin'
def G_rep(G,v,u):
    P= min_power(G,v,u)[0]
    f = graphviz.Graph('rep_graph.png')
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

###### QUESTION 8











"""
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
B.add_edge(1,2,0)
B.add_edge(1,3,0)
B.add_edge(1,13,0)
print(B) 
print(all_paths(B,1,5,H))"""

