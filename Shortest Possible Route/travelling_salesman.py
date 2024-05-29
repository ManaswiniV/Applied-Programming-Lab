# Importing the libraries we need
import numpy as np
import matplotlib.pyplot as plt
import sys

# Calculation of distance between two cities 
def dist(x1,y1,x2,y2):
    return np.sqrt((x1-x2)**2 + (y1-y2)**2)

# Calculation of total ditance in the given city order
def distance(cities,cityorder):
    d = []
    for i in range(len(cityorder)):
        ind1,ind2 = cityorder[i-1],cityorder[i]
        d.append(dist(cities[ind1][0],cities[ind1][1],cities[ind2][0],cities[ind2][1]))
    return sum(d)

# Extraction of coordinates of the cities from the given input file
f = open(sys.argv[1],'r')
numcities = []
cities = []
for i in f:
    j = i.split()
    if len(j) == 1:
        numcities.append(int(j[0]))
    else:
        cities.append((float(j[0]),float(j[1])))
f.close()
N = numcities[0]

# This function makes use of Simulated annealing algorithm to find the route with shortest total distance
def tsp(cities):
    global N
    x = [cities[i][0] for i in range(N)]
    y = [cities[j][1] for j in range(N)]

    # Creating a random order of cities for visiting and choosing any random city as starting point
    cp = list(range(N))
    start = np.random.choice(cp)

    # Ensures that the starting point is same for every iteration
    cp.remove(start)
    cp = [start]+cp

    # Best path and its distance gets updated if it finds any path with less total distance than the previous
    bp = cp
    bd = distance(cities,cp)

    # Temerature analog and its decay rate is defined
    t,r = 1000,0.99

    # Iterating it until it reaches the minimum threshold
    while t > 1e-15:

        # Random swap of two cities
        i,j = np.random.choice(range(1,N),2)
        newp = cp[:]
        newp[i],newp[j] = newp[j],newp[i]
        cd,newd = distance(cities,cp),distance(cities,newp)

        # Performs the algorithm and do changes to the best path
        if (newd<cd) or np.random.random_sample()<np.exp((cd-newd)/t):
            cp = newp
            cd = newd
            if newd<bd:
                bd = newd
                bp = newp
        t *= r
    return bp

xcities = [cities[i][0] for i in range(N)]
ycities = [cities[i][1] for i in range(N)]

# Generating a random order for visiting and plotting its path
randomorder = np.arange(N)
np.random.shuffle(randomorder)
xr = [cities[i][0] for i in randomorder]
yr = [cities[i][1] for i in randomorder]
xr.append(xr[0]), yr.append(yr[0])
tdr = distance(cities,randomorder)
print(f"City Order for Random Path Followed:\n{list(randomorder)}")
print(f"Total Distance travelled in Random Path: {tdr}")
plt.plot(xr,yr,label="Random Path Followed",marker='o',ms=6)
plt.scatter([xr[0]],[yr[0]],label="Starting City",s=100,c='red')
plt.title(f"Total Distance: {tdr}")
plt.legend()
plt.show()

# Generating best order for visiting using the simulated annealing algorithm and plotting its path
shortpath = tsp(cities)
xs = [cities[i][0] for i in shortpath]
ys = [cities[i][1] for i in shortpath]
xs.append(xs[0]),ys.append(ys[0])
tds = distance(cities,shortpath)
print(f"City Order for Shortest Path Followed:\n{list(shortpath)}")
print(f"Total Distance travelled in Shortest Path: {tds}")
plt.plot(xs,ys,label="Shortest Path Followed",marker='o',ms=6)
plt.scatter([xs[0]],[ys[0]],label="Starting City",s=100,c='red')
plt.title(f"Total Distance: {tds}")
plt.legend()
plt.show()

# Percentage improvement in visiting cities randomly and in short route
pi = (1-(tds/tdr))*100
print(f"Percentage Improvement in the Path: {round(pi,3)}%")