#!/usr/bin/env python
# coding: utf-8

# In[99]:


#importing all necessary libraries and modules

import numpy as np
#import pandas pd
import matplotlib.pyplot as plt
import pickle


# In[125]:


class lammpstrj_analysis:
    
    def __init__(self,filename,dt=1):
        self.filename=filename
        self.tstart,self.no_atoms,self.xlo,self.xhi,self.ylo,self.yhi,self.zlo,self.zhi=self.initialization()
        self.trj={}
        self.dr={}
        
    def initialization(self):
        file=open(self.filename,"r")
        file.readline() #itemline
        init_time=int(file.readline().replace("\n",""))
        file.readline() #item no of atoms
        no_atoms=int(file.readline().replace("\n",""))
        file.readline() # box bounds
        xlo,xhi=map(float,file.readline().replace("\n","").split(" "))
        ylo,yhi=map(float,file.readline().replace("\n","").split(" "))
        zlo,zhi=map(float,file.readline().replace("\n","").split(" "))
        file.close()
        return init_time,no_atoms,xlo,xhi,ylo,yhi,zlo,zhi
    
    def read_trj(self):
        tstart=-5
        tsecond=-5
        frames=0
        f=open(self.filename,"r")
        
        while f.read(2)!="": #condition of file ending
            f.readline().replace("\n","")  #skipping 1st line
            tstep=int(f.readline().replace("\n",""))#tstep
    
            # Calculate tdiff==================
            if tstart<0:
                tstart=tstep
            elif tstart>=0 and tsecond <0:
                tsecond = tstep
            self.tstop=tstep
            self.tdiff=tsecond-tstart
            #===================================
            #print("time step present",tstep)
            
            for i in range(7):
                f.readline().replace("\n","")   #skipping lines
        
            for i in range(0,self.no_atoms):            #loop to go through all atoms
                a=f.readline().replace("\n","").split(" ")  
                atom_id=int(a[0])
                atom_type=int(a[1])
                x=float(a[2])
                y=float(a[3])
                z=float(a[4])
                
                if atom_type not in self.trj:
                    self.trj[atom_type]={}
                    self.trj[atom_type][atom_id]={}
                else:
                    if atom_id not in self.trj[atom_type]:
                        self.trj[atom_type][atom_id]={}
                self.trj[atom_type][atom_id][tstep]=np.zeros(3,dtype=float)
    

                self.trj[atom_type][atom_id][tstep][0]=x
                self.trj[atom_type][atom_id][tstep][1]=y
                self.trj[atom_type][atom_id][tstep][2]=z
            frames+=1
        f.close()
        return frames
        
    def cal_dr(self,atom_type,atom_id,skip=1):
        temp=self.trj[atom_type][atom_id]
        dr={}
        for i in range(self.tstart,self.tstop-skip*self.tdiff+1,self.tdiff*skip):
            for j in range(i+self.tdiff*skip,self.tstop+1,self.tdiff*skip):
                dt=j-i
                dr2=(temp[j][0]-temp[i][0])**2+(temp[j][1]-temp[i][1])**2+(temp[j][2]-temp[i][2])**2
                if dt not in dr:
                    dr[dt]=[]
                dr[dt].append(dr2)
        return dr
    
    def mean_dr(self,dr):
        mean_dr=np.zeros((len(dr),2),dtype=float)
        j=0
        for i in dr:
            mean_dr[0+j,0]=i
            mean_dr[0+j,1]=sum(dr[i])/len(dr[i])
            j+=1
        return mean_dr
    
    def cal_msd(self,atom_type,atom_id,skip=1):
        msd=self.mean_dr(self.cal_dr(atom_type,atom_id,skip))
        self.save_output(msd,"id"+str(atom_id)+"msd.txt")
        return msd
        
    
    def save_dict_to_file(self,data_dict, file_path):
        with open(file_path, 'wb') as file:
            pickle.dump(data_dict, file)
            
    def save_output(self,data, file_path):
        np.savetxt(file_path,data)
            
    def plotting(self):
        pass
        
    def cal_all(self):
        for i in range(1,449):
            msd=self.mean_dr(self.cal_dr(1,i,20))
            
    def main(self):
        self.read_trj()
        for i in (1,449):
            msd=self.mean_dr(self.cal_dr(1,i))
            self.save_output(msd,"msd.txt")
            
    


# In[129]:


a=lammpstrj_analysis("prod600.lammpstrj")


# In[130]:


a.read_trj()
a.cal_msd(1,1,200)


# In[131]:


a.save_dict_to_file(a.trj,"trj.dat")


# In[ ]:




