def maximiser_profit_réaliste(filename):
    C=[]
    for i in range(3):
        f=open("/home/onyxia/Projet-de-programmation-1/input/trucks."+str(i)+".in", 'r')
        lines=f.readlines()
        L=[]
        for i in range(1,len(lines)):
           L.append(lines[i].split())
        L.pop(0)
        for j in range(1,len(L)):
            C.append(((i,j),L[j][0],L[j][1]))
    C1=C.sort(key=lambda x:x[2])
    P=[]
    f=open(filename,'r')
    lines=f.readlines()
    L=[]
    for i in range(1,len(L)):
        L.append(lines[i].split())
    L.pop(0)
    for j in range(1,len(L)):
        P.append((j,L[j][2],L[j][3]))
    P1=P.sort(reverse=True)

    M=[[[0 for i in range(len(P1))] for j in range(len(C1))]for k in range(3)]
    w=0
    i=0
    j=0
    while w<=B and j<len(P1):
        k=C1[i][0]
        g=P1[i][0]
        if C1[i][1]>=P1[j][2]:
            M[g][k[1]][k[0]]+=1
            w+=C1[i][2]
            i+=1
            j+=1
            
        else:
            M[g][k[1]][k[0]]==0
            j+=1

    return M
