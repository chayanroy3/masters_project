#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math as m


# In[2]:


class RDF:
    def __init__(self,filename):
        self.RDF=0
        self.filename=filename
        
    def system_parameters(self,filename):
        with open(filename,"r") as file:
            for i in range(5):
                file.readline()
            self.xlo,self.xhi=map(float,file.readline().split()[:2])
            self.ylo,self.yhi=map(float,file.readline().split()[:2])
            self.zlo,self.zhi=map(float,file.readline().split()[:2])
    
    def read_data(self,filename,skip=17):
        self.data=pd.read_csv(filename,sep=" ",skiprows=skip,names=["id","type","x","y","z"])
        self.data=self.data.set_index("id")
        
    def dist_range(self,left,right):
        self.dist=np.zeros((left[1]-left[0]+1,right[1]-right[0]+1))
        
        for i in range(left[0],left[1]+1):
            for j in range(right[0],right[1]+1):
                
                #relative distance componentwise
                xr=self.data.loc[j]["x"]-self.data.loc[i]["x"]
                yr=self.data.loc[j]["y"]-self.data.loc[i]["y"]
                zr=self.data.loc[j]["z"]-self.data.loc[i]["z"]
                
                #periodic boundary condition
                xr=xr-((self.xhi-self.xlo)*round(xr/(self.xhi-self.xlo)))
                yr=yr-((self.yhi-self.ylo)*round(yr/(self.yhi-self.ylo)))
                zr=zr-((self.zhi-self.zlo)*round(zr/(self.zhi-self.zlo)))
                
                #distace
                dr=m.sqrt(xr**2+yr**2+zr**2)
                self.dist[i-left[0],j-right[0]]=dr
                
    def RDF_cal(self,start,end,num):
        linear_value = np.linspace(start,end, num)
        result=np.zeros((num,2))
        for k,i in np.ndenumerate(linear_value):
            c=0
            for j in range(np.shape(self.dist)[0]):
                count=np.count_nonzero(np.logical_and(self.dist[j,:]<=i, self.dist[j,:]>0))
                c+=count
            area=4/3*m.pi*i**3
            result[k,0]=i
            result[k,1]=c/(area*np.shape(self.dist)[0])
        return result
            
        
        
        


# In[11]:

filename=""
a=RDF(filename)
a.read_data(filename)
a.system_parameters(filename)
a.dist_range([1089,1536],[1089,1536])
r=(a.RDF_cal(0.1,30,1200))
np.save("distance.npy",a.dist)

# In[20]:


plt.plot(r[:,0],r[:,1])
plt.xlabel("Distance")
plt.ylabel("RDF")
plt.savefig("RDF.png",dpi=600)
