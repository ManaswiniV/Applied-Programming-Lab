# Importing required libraries to solve the system of linear equations
import numpy as np
import sys

# Global Parameters are defined to improve readability
RESISTOR,VCS,ICS,START,END = 'R','V','I','.circuit','.end'

# The below defined function converts a string to a float type number after ignoring the comments
def convs2f(n):
    a=0
    try:
        return float(n)
    except:
        for i in n:
            if i=='#':
                a+=n.index(i)
        if a==0: s=len(n)
        else: s=a
        return float(n[:s])

# Classes for Resistor, Voltage Source and Current Source
class resistor:
    def __init__(self,c,n1,n2,m):
        self.comp = c
        self.node1 = (n1)
        self.node2 = (n2)
        self.mag = convs2f(m)
class vcs:
    def __init__(self,c,n1,n2,m):
        self.comp = c
        self.node1 = (n1)
        self.node2 = (n2)
        self.mag = convs2f(m)
class ics:
    def __init__(self,c,n1,n2,m):
        self.comp = c
        self.node1 = (n1)
        self.node2 = (n2)
        self.mag = convs2f(m)
        
# 'evalSpice' - function to solve for node voltages and current through voltage sources in resistive and linear circuits
def evalSpice(filename):
    # Declaring the necessary empty dictionaries to store the node names and to store the component data
    cktnodes = {}
    components = {RESISTOR:[],VCS:[],ICS:[]}
    
    try:
        fileopen = open(filename,'r')
      # The input file must have the extension '.ckt', else it would raise a ValueError
       
      # All the lines in the input files are loading into a list 'filelines' by ignoring all the comments
        filelines = []
        for line in fileopen:
            filelines.append(line.split('#')[0].split('\n')[0])
            
      # If '.circuit' and '.end' are not found in the input file, then it is a malformed circuit
        try:
            t1,t2 = filelines.index(START),filelines.index(END)
        except ValueError:
            raise ValueError("Malformed circuit file")
        
      # Creating the body of the circuit
        body = []
        for i in range(t1+1,t2):
            if len(filelines[i])!=0:
                body.append(filelines[i])
                
      # Loading all the nodes in to a dictionary 'cktnodes' by applying appropriate assumptions
        for i in body:
            j = i.split()
            if j[0][0]!='#':
                if j[0][0]=='R' or j[0][0]=='V' or j[0][0]=='I':
                    if j[1] not in cktnodes:
                        cktnodes[j[1]] = 1
                    else:
                        cktnodes[j[1]]+=1
                    if j[2] not in cktnodes:
                        cktnodes[j[2]] = 1
                    else:
                        cktnodes[j[2]]+=1
                   
                  # Checking for the Ground Node, there must be a GND node in the circuit for reference
                    if 'GND' not in cktnodes: raise ValueError("No Ground Node")
                    
                  # Loading the data of the components into the 'components' dictionary
                    if j[0][0] == RESISTOR:
                        if j[3]!=0:
                            components[RESISTOR].append(resistor(j[0],j[1],j[2],j[3]))
                    elif j[0][0] == VCS:
                        components[VCS].append(vcs(j[0],j[1],j[2],j[4]))
                    elif j[0][0] == ICS:
                        components[ICS].append(ics(j[0],j[1],j[2],j[4]))
                        
                # Error : If there are components other than V,I,R
                else:
                    raise ValueError("Only V, I, R elements are permitted")
        
        fileopen.close()
        
      # Assigning the indices to the nodes to make the problem simpler
        nodeindex = {}
        index=0
        
        for i in cktnodes:
            if i=='GND':
                nodeindex[i]=index
                index+=1
        for i in cktnodes:
            if i!='GND':
                nodeindex[i]=index
                index+=1
        
      # Creating Matrices of appropriate sizes to find the node volatges and current through V sources
        numnodes,numvcs = len(cktnodes),len(components[VCS])
        d = numnodes + numvcs
        A = np.zeros((numnodes+numvcs,numnodes+numvcs))
        B = np.zeros(numnodes+numvcs)
        
      # Resistor Equations
        for r in components[RESISTOR]:
            A[nodeindex[r.node1]][nodeindex[r.node1]]+=(1/r.mag)
            A[nodeindex[r.node1]][nodeindex[r.node2]]-=(1/r.mag)
            A[nodeindex[r.node2]][nodeindex[r.node2]]+=(1/r.mag)
            A[nodeindex[r.node2]][nodeindex[r.node1]]-=(1/r.mag)
      # Current Sources equations
        for i in components[ICS]:
            B[nodeindex[i.node1]] = (1)*(i.mag)
            B[nodeindex[i.node2]] = (-1)*(i.mag)
      # Voltage Sources equations
        for v in components[VCS]:
            ind = components[VCS].index(v)
            A[numnodes+ind][nodeindex[v.node1]] = 1.0
            A[numnodes+ind][nodeindex[v.node2]] = -1.0
            A[nodeindex[v.node2]][numnodes+ind] = -1.0
            A[nodeindex[v.node1]][numnodes+ind] = 1.0
            B[numnodes+ind] = v.mag
            
     # Solving the linear equations using numpy.linalg.solve()
     # It will raise a LinAlgError if the pair of equations are unsolvable, implies circuit has some error
        try:
            x = np.linalg.solve(A[1:,1:],B[1:])
            final = np.insert(x,0,0)
        except np.linalg.LinAlgError:
            raise ValueError("Circuit error: no solution")
        
        nodev,nodec = {},{}
        
     # Loading the values into a 'nodev' and 'nodec' dictionaries
     # 'nodev' contains the node_volatges
     # 'nodec' contains the current through the voltage sources
        for n in nodeindex:
            nodev[n] = final[nodeindex[n]]
        for p in components[VCS]:
            nodec[p.comp] = final[numnodes+(components[VCS].index(p))]
        
        return (nodev,nodec)
    # FileNotFoundError : If a valid SPICE file is not given as input
    except FileNotFoundError:
        raise FileNotFoundError("Please give the name of a valid SPICE file as input")

# Example usage
# result = evalSpice(sys.argv[1])
# print(result)