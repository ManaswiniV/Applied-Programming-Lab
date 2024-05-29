# Importing necessary libraries
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

# File opening to extract the datapoints from dataset2.txt and then added to two different lists
f = open('DataSets\dataset2.txt','r')
x,y = [],[]
for i in f.readlines():
    a = float(i.split()[0])
    b = float(i.split()[1].split('\n')[0])
    x.append(a),y.append(b)
f.close()

# Finding the x coordinate's of the points, which are far from the y axis, where the output of the signal would become zero.
l = []
for i in range(len(y)):
    if y[i]>0:
        l.append(i)
        break
for j in range(len(y)):
    if y[len(y)-j-1]<0:
        l.append(len(y)-j-1)
        break
        
# Hence the period becomes half of the difference between the x coordinates found out
period = (x[l[1]]-x[l[0]])*0.5

# Assuming the frequencies of the sine waves in the ration 1:3:5, hance the frequency becomes 2*pi/period,..
f1,f2,f3 = 2*np.pi/period, 6*np.pi/period, 10*np.pi/period

# Construction of matrix M, where the first column is filled with sin(f1*x), second with sin(f2*x),
# third with sin(f3*x)
M = np.column_stack([np.sin(f1*np.array(x)),np.sin(f2*np.array(x)),np.sin(f3*np.array(x))])

# np.linalg.lstsq() estimates the unknown parameters(a1,a2,a3)
(a1,a2,a3),_,_,_ = np.linalg.lstsq(M,y,rcond=None)

# New list of data points formed by putting the estimated values into the equation for signal
expy = []
for i in x:
    temp = a1*np.sin(f1*i)+a2*np.sin(f2*i)+a3*np.sin(f3*i)
    expy.append(temp)

# Typical model of the function having output y, unknown parameters: frequency, amplitudes
def signal(x,pc,ac1,ac2,ac3):
    value = ac1*np.sin(pc*x)+ac2*np.sin(pc*3*x)+ac3*np.sin(pc*5*x)
    return value

# curve_fit would give the estimated values of frequency and amplitudes for certain range of datapoints
(pc,ac1,ac2,ac3),_ = curve_fit(signal,x[390:654],y[390:654])

# New list of data points formed by putting the estimated values by using curve_fit into the equation for signal
expcy = []
for i in x:
    temp = ac1*np.sin(pc*i)+ac2*np.sin(pc*3*i)+ac3*np.sin(pc*5*i)
    expcy.append(temp)

print(f"Fundamental Period: {period}")
print(f"Amplitudes using Least Squares: {a1}, {a2}, {a3}")
print(f"Fundamental period estimated using Curve Fit: {2*np.pi/pc}")
print(f"Amplitudes using Curve Fit: {ac1}, {ac2}, {ac3}")

# Plotting
plt.plot(x,y,color="#93FFE8",label="Original")
plt.plot(x,expy,color="#EB5406",label="Least squares")
plt.plot(x,expcy,color="#FDBD01",label="Curve fit")
plt.legend()
plt.show()
plt.savefig('dataset2.png')