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
    
    def __init__(self,pos,cap,max_speed):
        super().__init__()
        self.pos = pos
        self.cap = cap
        self.max_speed = max_speed
        
        self.image, self.rect = rot_center(pygame.image.load("assets/items/bullet.png"), self.cap, self.pos[0], self.pos[1])
  
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
    def update(self,dt):
        speed_u = self.max_speed * np.array([np.sin(-self.cap*np.pi/180),-np.cos(self.cap*np.pi/180)])
        self.pos = self.pos + speed_u*dt
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
    
    

class Gun:
    
    def __init__(self,n_bullet = 300, max_speed = 1000):
        self.name = ""
        self.n_bullet = n_bullet
        self.max_speed = max_speed
        
    def load(self, gun_name):
                # Read JSON file
        with open("data/plane/Guns/guns.json") as fp:
          gun_dict = json.load(fp)
        
        self.n_bullet = gun_dict[gun_name]["ammo"]
        self.max_speed = gun_dict[gun_name]["max_speed"]
        
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
        self.name = ""
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
                print(f"DETECTION : {received_power}")
                
                n_detection += 1
                detection[n_detection] = poi.pos
                
        if len(detection)!=0:
            print(f"{len(detection)} plane(s) detected")
                
        return detection

    def load(self,radar_name):
                # Read JSON file
        with open("data/plane/EWS/radar/radar.json") as fp:
          radar_dict = json.load(fp)
        
        self.name = radar_name
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
        self.name = ""
        self.range = 10000 #Range in meters
        
    def load(self,passiveEW_name):
        with open("data/plane/EWS/passiveEW/passiveEW.json") as fp:
         PEW_dict = json.load(fp)
        
        self.range = PEW_dict[passiveEW_name]["range"]
        self.name = passiveEW_name
        
    def print_data(self):
        print(f"-Range of the passive electronic warfare : {self.range} m")
        
class Plane(pygame.sprite.Sprite):
    
    def __init__(self,pos=[0,0],cap=0, speed=0,rcs = 10, max_speed = 530, max_g = 9,name="Paper",throttle = 0.5):
        self.name = name
        self.gun = Gun()
        self.radar = Radar()
        self.passiveEW = PassiveEW()
        self.pos = np.array(pos)
        self.cap = cap
        self.speed = speed
        self.load(name)
        
        self.throttle = throttle
        self.turn = 0
        
        self.turn_rate = 180
        
        super().__init__()
        self.operational = True # Boolean for the statut of the plane (True = living, False = dead)
        self.detection = {}
        self.image = self.image_init
        self.rect = self.image.get_rect()
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
    
    def load(self,name_plane):
        with open("data/plane/planes.json") as fp:
         planes_dict = json.load(fp)
        
        self.name = name_plane
        self.rcs = planes_dict[name_plane]["rcs"]
        self.max_speed = planes_dict[name_plane]["V_max"]
        self.max_g = planes_dict[name_plane]["g_max"]
        self.image_init = pygame.image.load("assets/planes/"+planes_dict[name_plane]["skin"])
        
        gun = Gun()
        radar = Radar()
        passiveEW = PassiveEW()
        
        gun.load(planes_dict[name_plane]["gun"])
        radar.load(planes_dict[name_plane]["radar"])
        passiveEW.load(planes_dict[name_plane]["passiveEW"])
        
        self.gun = gun
        self.radar = radar
        self.passiveEW = passiveEW
    
    def update(self,planes,dt):
        
        if self.throttle >=1 :
            self.throttle = 1
        
        self.speed = self.max_speed * self.throttle
        self.cap = self.cap + self.turn * self.turn_rate * dt
        
        self.image, self.rect = rot_center(self.image_init, self.cap, self.pos[0],self.pos[1])
        speed_u = self.speed * np.array([np.sin(-self.cap*np.pi/180),-np.cos(self.cap*np.pi/180)])
        self.pos = self.pos + speed_u * dt
        self.rect.x = self.pos[0]
        self.rect.y = self.pos[1]
        
        self.ews_check(planes)
        
    def switch_radar(self):
        self.radar.statut = not(self.radar.statut)
        print(f"Radar activated : {self.radar.statut}")
        
    def ews_check(self,planes):
        if self.radar.statut:
            self.detection = self.radar.seek_objects(self, planes)
        
    def shoot(self):
        if self.gun.shoot():
            print(self.gun.n_bullet)
            return Bullet(self.pos+np.array(self.rect.size)/2, self.cap, self.gun.max_speed)
        else:
            print("no amo")
        
    def print_data(self):
        print("Plane data : ")
        print(f"-Position : x={self.pos[0]}, y={self.pos[1]}")
        print(f"-Cap : {self.cap}°")
        print(f"-radar cross section : {self.rcs} m^2")
        print("\nElectronic Warfare System :")
        self.radar.print_data()
        self.passiveEW.print_data()
    

