# Importing the necessary libraries
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# File opening to extract the datapoints from dataset3.txt and then added to two different lists
f = open('DataSets\dataset3.txt','r')
x,y = [],[]
for i in f.readlines():
    a = np.float64(i.split()[0])
    b = np.float64(i.split()[1].split('\n')[0])
    x.append(a),y.append(b)
f.close()

# Values of h,c,k
h,c,k = 6.62607015e-34, 2.998e8, 1.380649e-23

# v1 is a new list of datapoints, the values of 's' were appended into this list and 
# thus used as an argument in curve_fit
v1 = []
for i in range(len(x)):
    s = (2*h*(x[i]**3)/((c**2)*(abs(y[i]))))
    v1.append(np.log(s+1))

# Typical model of the function having output 's', unknown parameters: T
def temp(x,t):
    return ((h*x)/(k*t))

# Initialization of starting points to make the curve converge and then used in estimating the value of T
start,end = 1900,2600
T,_ = curve_fit(temp,x[start:end],v1[start:end])
print("Temperature estimated is "+str(T[0]))             