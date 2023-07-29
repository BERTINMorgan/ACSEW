# -*- coding: utf-8 -*-
"""
Created on Sat Jul 29 16:15:40 2023

@author: morga
"""

import plane_object
import pygame
import numpy as np


def target_direction(plane1,plane2):
    return -np.arctan2(plane2.pos[0]-plane1.pos[0],+plane1.pos[1]-plane2.pos[1])*180/np.pi

def target_distance(plane1,plane2):
    return np.linalg.norm(plane2.pos-plane1.pos)

class Simulation:
    def __init__(self):
        
        pygame.init()

        #Génération de la fênetre du jeu
        icon = pygame.image.load("assets/ui/rafale.ico")

        pygame.display.set_caption("ACSEW Simulation")
        pygame.display.set_icon(icon)
        self.screen = pygame.display.set_mode((1280,720))

        self.background = pygame.image.load("assets/ui/bg.png")
        self.running = True
        
        self.planes = []
        self.items = []
        
        self.dt = 1/30
        self.scroll_value = 0.95
        self.distortion = 1
        
        self.pressed = {}
        
    def add_plane(self,plane):
        self.planes.append(plane)
        
    def add_item(self,item):
        self.items.append(item)
        
    def update(self):
        self.screen.blit(self.background, (0,0))
        self.update_planes()
        self.update_items()
        
        pygame.display.flip()
        
    def update_planes(self):
        for i_plane in self.planes:
            i_plane.update(self.planes,self.dt)
            self.screen.blit(i_plane.image,i_plane.rect)
    
    def update_items(self):
        for i_item in self.items:
            i_item.update(self.dt)
            self.screen.blit(i_item.image, i_item.rect)
            
    def player_canon(self,player_plane):
        self.items.append(player_plane.shoot())
    
    def player_switch_radar(self,player_plane):
        player_plane.switch_radar()
    
    def turn_left(self,player_plane):
        player_plane.turn = 1
    
    def turn_right(self,player_plane):
        player_plane.turn = -1
    
    def straight(self,player_plane):
        player_plane.turn = 0
    
    def throttle_up(self,player_plane):
        if player_plane.throttle<=0.950001:
            player_plane.throttle += 0.05
    
    def throttle_down(self,player_plane):
        if player_plane.throttle>=0.2:
            player_plane.throttle -= 0.05
    
    def scroll(self,zoom_dir):
        self.distortion = self.scroll_value**zoom_dir
        
        for i_plane in self.planes:
            i_plane.pos = i_plane.pos * self.distortion
            i_plane.max_speed = i_plane.max_speed * self.distortion
        
        for i_item in self.items:
            i_item.pos = i_item.pos * self.distortion
            i_item.max_speed = i_plane.max_speed * self.distortion
            
        
        