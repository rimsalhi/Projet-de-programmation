from graph import Graph

def explore2(G,v1,v2,H):
    if H==[]:
        H.append([v1])
    H1=H
    for L in H1:
        if (v2 in L)==False:
            v=L[-1]
            for k in G.graph[v]:
                if (k in L)==False:
                     L2=L
                     L1=L2.append(k[0])

    return H1
       
C=Graph([1,2,3,4,5,6])   
C.add_edge(1,6,0)
C.add_edge(1,5,10)
C.add_edge(5,2,5)
C.add_edge(2,3,15)
C.add_edge(3,4,12)
C.add_edge(3,1,19)

print(C)
      
        
print(explore2(C,1,2,[]))