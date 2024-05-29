# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
 
# File opening to extract the datapoints from dataset1.txt and then added to two different lists
f = open("DataSets\dataset1.txt", "r")
xcord,ycord = [],[]
for i in f.readlines():
    x = float(i.split()[0])
    y = float(i.split()[1].split('\n')[0])
    xcord.append(x)
    ycord.append(y)
f.close()

# Construction of matrix M with two columns
# First column with x coordinates, second column with ones
M = np.column_stack([xcord,np.ones(len(xcord))])

# np.linalg.lstsq() would estimate the unknown values m(slope) and c(intercept)
B = np.linalg.lstsq(M, ycord, rcond=None)

m = B[0][0]
c = B[0][1]

print(f"Slope of the line: {m}")
print(f"Intercept of the line: {c}")

# New list of data points formed by putting the estimated values into the equation for line
est_y = []
for i in xcord:
    est_y.append(m*i+c)
    
# Plotting
plt.plot(xcord,ycord,color="#93FFE8",label="Original")
plt.plot(xcord,est_y,color="#008000",label="Estimated")
plt.errorbar(xcord[::25], ycord[::25], fmt='o-r',ms=3.5,label="Error bar")
plt.legend()
plt.show()
plt.savefig('dataset1.png')