# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:29:09 2023

@author: morga
"""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.collections import PatchCollection
import numpy as np
import json


#Class RADAR
#Set by a cone and a range
#child for EW (electronic warfare) class
class Radar:
    def __init__(self):
        self.cone = 35      #cone angle in °
        self.range = 15000  #range in meters

    def load_radar(self,radar_name):
                # Read JSON file
        with open("data/plane/EWS/radar/radar.json") as fp:
          radar_dict = json.load(fp)
        
        self.range = radar_dict[radar_name]["range"]
        self.cone = radar_dict[radar_name]["cone"]
                
    def print_data(self):
        print(f"-Range of the radar: {self.range} m\n-Cone of the radar : {self.cone}°")
        
#Class passiveEW
#Set by a range
#child for EW (electronic warfare) class
class PassiveEW:
    def __init__(self):
        self.range = 10000 #Range in meters
        
    def load_passiveEW(self,passiveEW_name):
        with open("data/plane/EWS/passiveEW/passiveEW.json") as fp:
         PEW_dict = json.load(fp)
        
        self.range = PEW_dict[passiveEW_name]["range"]
        
        
    def print_data(self):
        print(f"-Range of the passive electronic warfare : {self.range} m")
        
class ElectronicWarfareSystem:
    def __init__(self):
        self.Radar = Radar()
        self.PassiveEW = PassiveEW()
        
    def print_data(self):
        print("RADAR :")
        self.Radar.print_data()
        print("Passive EW :")
        self.PassiveEW.print_data()
        
    def shema(self):
        # PASSIVE EW DATA
        passiveEWcircle = plt.Circle((0,0),self.PassiveEW.range,color='r')
        
        # RADAR DATA
        patches = []
        wedge = mpatches.Wedge((0, 0), self.Radar.range, -self.Radar.cone/2+90, self.Radar.cone/2+90)
        patches.append(wedge)
        colors = [0,255,0]
        collection = PatchCollection(patches,alpha = 0.5)
        collection.set_array(np.array(colors))
        # MISSILE DATA
        ## TODO
        
        # DISP DATA
        fig, ax = plt.subplots() # note we must use plt.subplots, not plt.subplot        
        ax.add_patch(passiveEWcircle)
        ax.add_collection(collection)
        
        super_xy = max([self.Radar.range,self.PassiveEW.range])*1.1
        
        ax.set_xlim([-super_xy, super_xy])
        ax.set_ylim([-super_xy, super_xy])
        ax.set_aspect('equal', adjustable='box')
        
class Plane:
    def __init__(self,pos=np.array([0,0]),cap=0):
        self.EWS = ElectronicWarfareSystem()
        self.pos = pos #Plane position in meters
        self.cap = cap # Plane cap in degrees
        
    def print_data(self):
        print("Plane data :")
        print(f"-Position : x={self.pos[0]}, y={self.pos[1]}")
        print(f"-Cap : {self.cap}°\n")
        print("Electronic Warfare System : \n")
        self.EWS.print_data()
    
        
Rafale = Plane()
Rafale.EWS.shema()
Rafale.EWS.Radar.load_radar("RBE-2")
Rafale.EWS.PassiveEW.load_passiveEW("PGE-1")
Rafale.EWS.shema()


