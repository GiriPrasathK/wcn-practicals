import numpy as np
data = [2,3,4, 10, 11, 12, 20, 25, 30]
D = np.array(data)
k= 2
c1 = np.random.choice(D)
c2 = np.random.choice(D)


prev_k1= [0]
prev_k2 = []

k1 = []
k2 = []
j = 0
while prev_k1 != k1:
    prev_k1 = k1
    k1 = []
    k2 = []
    j = j+1
    print()
    print("Iteration ",j,":")
    for i in D:
        if abs(i - c1) < abs(i - c2):
            k1.append(i)
        else:
            k2.append(i)
    c1 = round(sum(k1)/len(k1))
    c2 = round(sum(k2)/len(k2))        
    
    print("k1: ", k1)
    print("k2: ", k2)
    print("c1: ", c1, ",c2: ", c2)
    
print()
print("Final clusters are: ")
print("k1: ", k1)
print("k2: ", k2)
        
        