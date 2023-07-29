# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 10:58:28 2023

@author: morga
"""

import json

def init_json():

    with open("data/plane/EWS/radar/radar.json", "w") as fp:
        json.dump({},fp,indent = 4)

    with open("data/plane/EWS/passiveEW/passiveEW.json", "w") as fp:
        json.dump({},fp,indent = 4) 

    with open("data/plane/planes.json", "w") as fp:
        json.dump({},fp,indent = 4) 

    with open("data/plane/Guns/guns.json", "w") as fp:
        json.dump({},fp,indent = 4) 
    

def create_radar():
    radarName = input("Name of the radar ?")
    radarRange = eval(input("Range of the radar (meters) ?"))
    radarCone = eval(input("Aperture of the radar (°) ?"))
    
    radar_data = {radarName : {'range':radarRange,'cone':radarCone}}
     
    # Read JSON file
    with open("data/plane/EWS/radar/radar.json") as fp:
      radar_dict = json.load(fp)
      
    radar_dict.update(radar_data)
    
    with open("data/plane/EWS/radar/radar.json", "w") as fp:
        json.dump(radar_dict,fp,indent = 4) 
       
        
def create_passiveEW():
    PassiveEWName = input("Name passive EW ?")
    PassiveEWRange = eval(input("Range of the passive EW (meters) ?"))
    
    PassiveEW_data = {PassiveEWName:{'range':PassiveEWRange}}
     
    # Read JSON file
    with open("data/plane/EWS/passiveEW/passiveEW.json") as fp:
      passiveEW_dict = json.load(fp)
    
    passiveEW_dict.update(PassiveEW_data)
    
    with open("data/plane/EWS/passiveEW/PassiveEW.json", "w") as fp:
        json.dump(passiveEW_dict,fp,indent = 6) 

def create_gun():
    gun_name = input("Name of the gun ?")
    n = eval(input("Number of bullet aviable ?"))
    velocity = eval(input("Velocity of the bullet ? (m/s)"))
    
    gun_data ={gun_name : {'ammo' : n,'velocity' : velocity}} 
    
    # Read JSON file
    with open("data/plane/Guns/guns.json") as fp:
      guns_dict = json.load(fp)
    
    guns_dict.update(gun_data)
    
    with open("data/plane/Guns/guns.json", "w") as fp:
        json.dump(guns_dict,fp,indent = 6) 
    
def create_plane():

    Name = input("Name of the plane : ")
    rcs = eval(input("Radar Cross Section of the plane (m^2)"))
    max_speed = eval(input("Max speed of the plane (m/s)"))
    max_g = eval(input("Max acceleration of the plane (g)"))
    skin = input("Enter the skin name")
    gun = input("Enter the name of the canon")
    passiveEW = input("Enter the name of the passive electronics warfare system")
    radar = input("Enter the name of the radar")
    
    plane_data = {Name : {"rcs" : rcs,"V_max" : max_speed,"g_max":max_g,"skin":skin,"gun":gun,"passiveEW":passiveEW,"radar":radar}}
     
    # Read JSON file
    with open("data/plane/planes.json") as fp:
      plane_dict = json.load(fp)
      
    plane_dict.update(plane_data)
    
    with open("data/plane/planes.json", "w") as fp:
        json.dump(plane_dict,fp,indent = 4) 