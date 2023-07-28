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
        