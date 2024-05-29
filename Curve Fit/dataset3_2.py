# Importing necessary libraries
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
from scipy import constants

# Values of c,T are declared, the goal here is to estimate the values of h and k
c,T = constants.speed_of_light, 4998.813308041924

# File opening to extract the datapoints from dataset3.txt and then added to two different lists
f = open('DataSets\dataset3.txt','r')
x,y = [],[]
for i in f.readlines():
    a = float(i.split()[0])
    b = float(i.split()[1].split('\n')[0])
    x.append(a),y.append(b)
f.close()

# A typical model of the function having the output y, unknown parameters: h and k
def handk(x,h,k):
    n = (2*h*(x**3))
    d = (np.exp((h*x)/(k*T))-1)*(c**2)
    return n/d

# Initialization of starting points to make the curve converge and then used in estimating the value of h and k
start,end = 2200, 2700

# An initial guess of h and k were given, thus it can estimate the approximate values of h and k 
# using curve_fit
est,_ = curve_fit(handk,x[start:end],y[start:end],p0 = [constants.h, constants.k])

print(f"Planck's Constant: {est[0]}")
print(f"Boltzmann Constant: {est[1]}")

# New list of intensities by putting the estimated data into the intensity equation
exp_y = []
for i in range(len(x)):
    p,q = (2*est[0]*(x[i]**3))/(c**2), np.exp((est[0]*x[i])/(est[1]*T))-1
    exp_y.append(p/q)

###### New list of intensities by putting the estimated Temperature in dataset3_1.py ######
# It is written in this file to just plot all the curves at once.
exy = []
for i in x:
    num = (2*(constants.h)*(i**3))/((constants.c)**2)
    den = np.exp(((constants.h)*i)/((constants.k)* 4998.813308041924))-1
    exy.append(num/den)

plt.plot(x,y,label="Original",color="#93FFE8")
plt.plot(x,exy,label="Part 1",color="#EB5406")
plt.plot(x,exp_y,label="Part 2",color="#FDBD01")
plt.legend()
plt.show()
plt.savefig('dataset3.png')

