# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:28:18 2023

@author: JALOUX Matisse, BERTIN Morgan, LAMONTAGNE Corentin
"""

import plane_object
import pygame
import numpy as np
import time
pygame.init()

#Génération de la fênetre du jeu
icon = pygame.image.load("assets/ui/rafale.ico")

pygame.display.set_caption("ACSEW Simulation")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load("assets/ui/bg.png")


#Chargement des avions
paper = plane_object.Plane(pos=[0,0],cap = -135,speed = 25)

drone = plane_object.Plane(pos=[-40,-60],cap = -135,speed = 25)
drone.image_init = pygame.image.load("assets/planes/IA.png")
drone.rcs = 1e-6

rafale = plane_object.Plane(pos=[0,720],cap = -180,speed = 100)
rafale.image_init = pygame.image.load("assets/planes/rafale.png")
rafale.image = rafale.image_init
rafale.rect = rafale.image.get_rect()

mig = plane_object.Plane(pos=[540,128],cap = -180,speed = 150)
mig.image_init = pygame.image.load("assets/planes/mig.png")
mig.image = mig.image_init
mig.rect = mig.image.get_rect()

running = True

items = []

while running: 
    
    mig.cap = mig.cap + 60 * 1/60
    rafale.cap = -np.arctan2(mig.pos[0]-rafale.pos[0],+rafale.pos[1]-mig.pos[1])*180/np.pi
    


    

    
    paper.update([],1/60)
    drone.update([], 1/60)
    rafale.update([mig,paper],1/60)
    mig.update([rafale],1/60)
    
    screen.blit(background, (0,0))
    
    screen.blit(drone.image,drone.rect)
    screen.blit(paper.image,paper.rect)
    screen.blit(rafale.image,rafale.rect)
    screen.blit(mig.image,mig.rect)
    
    for k_item in items:
        k_item.update(1/60)
        screen.blit(k_item.image, k_item.rect)
        
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                items.append(rafale.shoot())
            if event.key == pygame.K_RETURN:
                rafale.switch_radar()
    time.sleep(1/60)
    
