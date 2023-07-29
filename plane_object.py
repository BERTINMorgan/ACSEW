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
import pygame


def rot_center(image, angle, x, y):
    
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center = image.get_rect(center = (x, y)).center)

    return rotated_image, new_rect


class Bullet(pygame.sprite.Sprite):
    
    def __init__(self,pos,cap,speed):
        super().__init__()
        self.pos = pos
        self.cap = cap
        self.speed = speed
        
        self.image, self.rect = rot_center(pygame.image.load("assets/items/bullet.png"), self.cap, self.pos[0], self.pos[1])
  
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
    def update(self,dt):
        speed_u = self.speed * np.array([np.sin(-self.cap*np.pi/180),-np.cos(self.cap*np.pi/180)])
        self.pos = self.pos + speed_u*dt
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
    
    

class Gun:
    
    def __init__(self,n_bullet = 300, velocity = 1000):
        self.n_bullet = n_bullet
        self.velocity = velocity
        
    def shoot(self):
        if self.n_bullet >0 : 
            self.n_bullet -= 1
            return True
        else:
            return False

#Class RADAR
#Set by a cone and a range
#child for EW (electronic warfare) class
class Radar:
    def __init__(self):
        self.cone = 35      #cone angle in °
        self.range = 15000  #range in meters
        
        self.statut = False #Statut of the radar
        
        
    def seek_objects(self,porteur,objects):

        detection = {}
        n_detection = 0

        for poi in objects:
            
            distance_plane_to_poi = np.linalg.norm(poi.pos-porteur.pos)
            angle_plane_heading_to_poi = (np.arctan2(poi.pos[0]-porteur.pos[0],poi.pos[1]-porteur.pos[1])*180/np.pi-porteur.cap + 180) % 360
            received_power = poi.rcs * self.range**4 / distance_plane_to_poi**4
            
            if distance_plane_to_poi <= self.range and np.abs(angle_plane_heading_to_poi) <= self.cone/2 and received_power>=1:
                print("DETECTION :")
                print(distance_plane_to_poi)
                print(angle_plane_heading_to_poi)
                
                n_detection += 1
                detection[n_detection] = poi.pos
                
        if len(detection)!=0:
            print(f"{len(detection)} plane(s) detected")
                
        return detection

    def load_radar(self,radar_name):
                # Read JSON file
        with open("data/plane/EWS/radar/radar.json") as fp:
          radar_dict = json.load(fp)
        
        self.range = radar_dict[radar_name]["range"]
        self.cone = radar_dict[radar_name]["cone"]
                
    def print_data(self):
        print(f"-Range of the radar: {self.range} m\n-Cone of the radar : {self.cone}°")
        print(f"-Radar activated : {self.statut}")
        
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
        
class Plane(pygame.sprite.Sprite):
    
    def __init__(self,pos=[0,0],cap=0, speed=0,rcs = 10):
        self.EWS = ElectronicWarfareSystem()
        self.pos = np.array(pos) #Plane position in meters
        self.cap = cap # Plane cap in degrees
        self.speed = speed
        self.rcs = rcs
        self.gun = Gun()
        
        super().__init__()
        self.operational = True # Boolean for the statut of the plane (True = living, False = dead)
        self.detection = {}
        self.image_init = pygame.image.load("assets/planes/paper.png")
        self.image = self.image_init
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]

    
    def update(self,planes,dt):
        
        
        self.image, self.rect = rot_center(self.image_init, self.cap, self.pos[0],self.pos[1])
        speed_u = self.speed * np.array([np.sin(-self.cap*np.pi/180),-np.cos(self.cap*np.pi/180)])
        self.pos = self.pos + speed_u * dt
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
        self.ews_check(planes)
        
    def switch_radar(self):
        self.EWS.Radar.statut = not(self.EWS.Radar.statut)
        print(f"Radar activated : {self.EWS.Radar.statut}")
        
    def ews_check(self,planes):
        if self.EWS.Radar.statut:
            self.detection = self.EWS.Radar.seek_objects(self, planes)
        
    def shoot(self):
        if self.gun.shoot():
            print(self.gun.n_bullet)
            return Bullet(self.pos, self.cap, self.gun.velocity)
        else:
            print("no amo")
        
    def print_data(self):
        print("Plane data : ")
        print(f"-Position : x={self.pos[0]}, y={self.pos[1]}")
        print(f"-Cap : {self.cap}°")
        print(f"-radar cross section : {self.rcs} m^2")
        print("\nElectronic Warfare System :")
        self.EWS.print_data()
    

