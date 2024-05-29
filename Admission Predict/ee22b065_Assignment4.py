# Importing the necessary libraries to open the csv file and to perform linear regression
import numpy as np
import csv

# Extracting the data from the csv file into different lists according to the parameters
gre,toefl,rating,sop,lor,cgpa,research,chance = [],[],[],[],[],[],[],[]
f = open('Admission_Predict_Ver1.1.csv','r')
csv_reader = csv.reader(f)
for i in csv_reader:
    gre.append(i[1]),toefl.append(i[2]),rating.append(i[3])
    sop.append(i[4]),lor.append(i[5]),cgpa.append(i[6])
    research.append(i[7]),chance.append(i[8])
    
# Updating the lists by ignoring the header
gre,toefl,rating,sop = gre[1:],toefl[1:],rating[1:],sop[1:]
lor,cgpa,research,chance = lor[1:],cgpa[1:],research[1:],chance[1:]

# Converting the elements in the lists into corresponding int or float
gre,toefl,rating = [int(x) for x in gre],[int(x) for x in toefl],[int(x) for x in rating]
sop,lor,cgpa = [float(x) for x in sop],[float(x) for x in lor],[float(x) for x in cgpa]
research,chance = [int(x) for x in research],[float(x) for x in chance]

# Building a matrix M of order no.of datapoints and 8
# 1st column = Gre score, 2nd column =  toefl score.......8th column with ones
# Equation: Mp = chance, 'p' contains the coefficients of the parameters
M = np.column_stack([gre,toefl,rating,sop,lor,cgpa,research,np.ones(len(chance))])
p,_,_,_ = np.linalg.lstsq(M,chance,rcond=None)

print("Coefficients of the parameters in linear model")
print(f"GRE Score: {p[0]}\nTOEFL Score: {p[1]}\nUniversity Rating: {p[2]}\nSOP: {p[3]}\nLOR: {p[4]}")
print(f"CGPA: {p[5]}\nResearch: {p[6]}\nConstant term in Linear Function: {p[7]}")

# 'predict' is a list of getting chance to admit on the basis of estimated model
# Also calculating RMS Error, Mean Error
predict = []
sqerror = 0
avg = 0
for i in range(len(chance)):
    exp = p[0]*gre[i]+p[1]*toefl[i]+p[2]*rating[i]+p[3]*sop[i]+p[4]*lor[i]+p[5]*cgpa[i]+p[6]*research[i]+p[7]
    predict.append(exp)
    sqerror += (exp-chance[i])**2
    avg += ((abs(exp-chance[i])))
print("*******************************************************")
print(f"Root Mean Square Error : {(sqerror/len(chance))**0.5}")
print(f"Mean Absolute Error : {avg/len(chance)}")

# Finding the average ratio of estimated chance to given chance of admit
y = 0
for i in range(len(chance)):
    y+=(chance[i]/predict[i])
print(f"Average Ratio of Estimated Chance to the given Chance: {y/len(chance)}")