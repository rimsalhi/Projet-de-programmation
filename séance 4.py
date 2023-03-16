# Problème du sac à dos:
# x[i,j]==1 si le camion i correspond à une route j donc le problème revient à trouver le vecteur x=(x[1,1],..x[n,m])
# W-->B est la limite budgétaire
# w[i] est le coût du camion i
# Le profit de la route j que prend le camion est p[j]
# Il faut que sum(w[i]*x[i,j]<W) et maximiser sum(p[j]*x[i,j])
# On commence par trier les coûts

def maximiser_profit(filename):
    C=[]
    for i in range(3):
        f=open("trucks."+i+".in", 'r')
        lines=f.readlines()
        L=[]
        for i in range(1,len(lines)):
           L.append(lines[i].split())
        for j in range(len(L)):
            C.append[((i,j),L[j][0],L[j][1])]
    C1=C.sort(key=lambda x:x[2])
    P=[]
    f=open(filename,'r')
    lines=f.readlines()
    L=[]
    for i in range(1,len(L)):
        L.append(lines[i].split())
    for j in range(len(L)):
        P.append[(j,L[j][2])]
    P1=P.sort(reverse=True)
    
    

    

