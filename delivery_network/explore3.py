class Graph:
    def __init__(self, nodes=[]):
        self.nodes = nodes
        self.graph = dict([(n, []) for n in nodes])
        self.nb_nodes = len(nodes)
        self.nb_edges = 0
    

    def __str__(self):
        """Prints the graph as a list of neighbors for each node (one per line)"""
        if not self.graph:
            output = "The graph is empty"            
        else:
            output = f"The graph has {self.nb_nodes} nodes and {self.nb_edges} edges.\n"
            for source, destination in self.graph.items():
                output += f"{source}-->{destination}\n"
        return output
    
    def add_edge(self, node1, node2, power_min, dist=1):
        """
        Adds an edge to the graph. Graphs are not oriented, hence an edge is added to the adjacency list of both end nodes. 

        Parameters: 
        -----------
        node1: NodeType
            First end (node) of the edge
        node2: NodeType
            Second end (node) of the edge
        power_min: numeric (int or float)
            Minimum power on this edge
        dist: numeric (int or float), optional
            Distance between node1 and node2 on the edge. Default is 1.
        """
        self.graph[node1].append((node2, power_min, dist))
        self.graph[node2].append((node1, power_min, dist))

    

    def get_path_with_power(self, src, dest, power):
        raise NotImplementedError
    

    def connected_components(self):
        raise NotImplementedError

    def connected_components_set(self):
        """
        The result should be a set of frozensets (one per component), 
        For instance, for network01.in: {frozenset({1, 2, 3}), frozenset({4, 5, 6, 7})}
        """
        return set(map(frozenset, self.connected_components()))
    
    def min_power(self, src, dest):
        """
        Should return path, min_power. 
        """
        raise NotImplementedError

def graph_from_file(filename):
    """
    Reads a text file and returns the graph as an object of the Graph class.

    The file should have the following format: 
        The first line of the file is 'n m'
        The next m lines have 'node1 node2 power_min dist' or 'node1 node2 power_min' (if dist is missing, it will be set to 1 by default)
        The nodes (node1, node2) should be named 1..n
        All values are integers.

    Parameters: 
    -----------
    filename: str
        The name of the file

    Outputs: 
    -----------
    G: Graph
        An object of the class Graph with the graph from file_name.
    """
    f=open(filename, 'r')
    lines=f.readlines()  

    L=[]
    for i in range(len(lines)):
        L.append(lines[i].split())
    M=[i for i in range(1,int(L[0][0])+1)]
    print(M)
    G=Graph(M)
    G.nb_edges=int(L[0][1])

    L.pop(0)

    for line in L:
        G.add_edge(int(line[0]),int(line[1]),int(line[2]))
    return G
#g = graph_from_file("/home/onyxia/work/input /network.00.in")
#print(g)

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

#Un exemple simple de graphe 
B=Graph([1,2,3,4,5,6,12])
B.add_edge(1,4,0)
B.add_edge(4,5,0)
B.add_edge(1,2,0)
B.add_edge(1,3,0)
B.add_edge(6,12,0)
print(B)       

def explore(G,v,s):
    for k in G.graph[v]:
        if (k[0] in s)==False:
            s.add(k[0])
            explore(G,k[0],s)
    return s 
s=set()
print(explore(B,1,s))
def connected_components_set(G):
    L=[]
    for v in G.nodes:
        s=set()
        if (explore(G,v,s) in L)==False:
            L.append(explore(G,v,s))
    return L 
           
print(connected_components_set(B))

#Question 4
def graph_from_file_4(filename):
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




# def fin(G,u,H):
#     for L in H: 
#         if (L[-1]!=u) and (len(G.graph[L[-1]])!=1):
#             return False
#     return True
# H=[[1]]
# def explore3(G,v,u,H):
#     if fin(G,u,H)==True:
#         return H
#     i=0
#     while i <len(H):
#         if H[i][-1]==u:
#             i+=1
#             continue
#         s=0  
#         for k in G.graph[H[i][-1]]: 
#             if (k[0] in H[i])==False:
#                 H.insert(i+1,H[i]+[k[0]])
#                 s+=1
#         if s>0:        
#             H.pop(i)
#             i+=s
#         else:
#             i+=1
#         print(i)
#     return explore3(G,v,u,H)



# La fonction explore3 prend en paramètre un graphe G et deux villes u et v.
# Elle donne tous les chemins possibles sortant de v.
# Imaginons un bonhomme qui sort de v et prend des tournures aléatoires en espérant se trouver sur u
# soit il se trouve d'une certaine manière en v et à ce moment il s'arrête (1)
# soit il se trouve au bout de la route (sur un noeud avec un seul edge qu'ila déjâ parcouru) (2)
# et donc est obligé de s'arrêter
# soit il se retrouve sur la case de départ v et donc oest obligé de s'arrêter (3)
# D'une manière récursive, cette fonction construit un arbre de choix:
# On commence par [la case de départ], on la multiplie par le nombre de ses noeuds 
# et à chaque [cse de départ], on ajoute un noeud. On obtient une liste contenant tous les deux premiers pas possibles
# Puis on fait la même chose pour chaque [deux premiers pas possibles] 
# Le nième parcours de la fonction récursive explore3 donne tous les chemins possibles que le bonhomme aurait pu parcourir 
# au cours de ses premiers n pas (sous les conditions mentionnées)
# Le bonhomme arrête son exploration que lorsque le test fin est vrai
# et donc chaque chemin construit est l'un des cas mentionnés (1-3)
# Par conséquent, la liste de chemins et composés de chemins qui ont abouti (finissent par u) et les autres


def fin(G,u,H):
    if len(H)==1:
        return False
    for L in H: 
        if (L[-1]!=u) and (L[-1]!='FIN') and (len(G.graph[L[-1]])!=1):
            return False
    return True

# La fonction fin a pour but de vérifier la condition d'arrêt de la fonction récursive

def explore3(G,v,u,H):
    if fin(G,u,H)==True:
        return H
    i=0
    # i représente une des branches de l'arbre de choix 
    while (i <len(H)): 
        if H[i][-1]==u:
            i+=1
            continue
        elif (H[i][-1]==H[i][0]) and (len(H[i])>1):
                H[i].append('FIN')
                i+=1
                continue
        elif H[i][-1]=='FIN':
            i+=1
            continue
        # S'il reste plus des choix à faire (on est tombé sur u ou on est tombé sur la case de départ)
        # on passe à la branche suivante, sinon on poursuit  
        s=0  
        for k in G.graph[H[i][-1]]: 
            if (k[0] in H[i][1:])==False: 
            if k[0]!=H[i][-1]: 
                # on ne permet qu'à v de se répéter pour repérer le chemin comme un retour à la case de départ 
                # problème s'il y a un cycle interne : voir B 
                H.insert(i+1,H[i]+[k[0]])
                s+=1 #s est le nombre de nouvelles branches (filles) construites au niveau n
        if s>0:        
            H.pop(i) # les filles remplacent la mère (chemin incomplet)
            i+=s # on passe à la mère suivante, donc on saute les filles construites
        else:
            i+=1 
    print(H)
    return explore3(G,v,u,H)




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
print(explore3(B,1,12,H))

