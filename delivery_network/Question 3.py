from python import Graph 
B=Graph([1,2,3,4,5])

B.add_edge(1,4,0)

B.add_edge(4,5,0)

B.add_edge(1,2,0)

B.add_edge(1,3,0)

print(B)


def get_path_with_power(p,t):
    s=0
    for i in t.graph:
        for j in t.graph[i]:
            if p<j[1]:
                return False
    print("Ce trajet est possible")
    return connected_components_sets(t.graph)

get_path_with_power(1000,B)