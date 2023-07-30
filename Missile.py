from math import *
import json
import numpy as np
import colorama
from colorama import Fore
from colorama import Style

g = 9.81

#Calcule de la vitesse angulaire et du rayon de braquage.
def angle_of_rotation(Fact_charge, Speed):
    return ((Fact_charge * g * 180) / (np.pi * Speed)), ((Speed * Speed) / (Fact_charge * g))


def opendata(dataname):
    try:
        data_file = open(dataname)
        data = data_file.read()
        data = json.loads(data)
        return data
    except:
        print(Fore.RED + Style.BRIGHT + 'LOADING DATA - ' + dataname + " - FAILED - CODE ERROR : JSON CAN'T BE OPEN" + Style.RESET_ALL)

class Missile:
    def __init__(self):
        self.type = 'Missile'
        self.Fact_charge = 35
        
    def load_missile(self, Missile_name, data_path):
        data_missile = opendata(data_path)
        try:
            data_missile[Missile_name]
        except:
            print(Fore.RED + Style.BRIGHT + 'LOADING - ' + Missile_name + ' - FAILED - CODE ERROR : NAME INCORRECT' + Style.RESET_ALL)
            return
        try:
            self.mass = data_missile[Missile_name]['mass']
            self.speed = data_missile[Missile_name]['speed']
            self.no_escape_zone = data_missile[Missile_name]['no_escape_zone']
            self.cone = data_missile[Missile_name]['deg_cone']
            self.range = data_missile[Missile_name]['range_cone']
            print(Fore.GREEN + Style.BRIGHT + 'LOADING - ' + Missile_name + ' - SUCCESS' + Style.RESET_ALL)
        except:
            print(Fore.YELLOW + Style.BRIGHT + 'LOADING - ' + Missile_name + ' - INCOMPLETE - CODE ERROR : MISSILE DATA INCOMPLETE' + Style.RESET_ALL)

    
    
Missile_1 = Missile()
Missile_1.load_missile('Meteor_MBDA', 'data/json_missile.json')

