# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:28:18 2023

@author: JALOUX Matisse, BERTIN Morgan, LAMONTAGNE Corentin
"""

import plane_object
import pygame
import numpy
import time
pygame.init()

#Génération de la fênetre du jeu
icon = pygame.image.load("data/IHM/rafale.ico")

pygame.display.set_caption("ACSEW Simulation")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode((1080,720))

background = pygame.image.load("data/IHM/bg.png")


#Chargement des avions
paper = plane_object.Plane(pos=[0,0],cap = -135,speed = [25,25])

rafale = plane_object.Plane(pos=[540,0],cap = -180,speed = [0,100])
rafale.image_init = pygame.image.load("data/plane/skins/rafale.png")
rafale.image = rafale.image_init
rafale.rect = rafale.image.get_rect()

mig = plane_object.Plane(pos=[540,128],cap = -180,speed = [0,100])
mig.image_init = pygame.image.load("data/plane/skins/mig.png")
mig.image = mig.image_init
mig.rect = mig.image.get_rect()

running = True

while running: 
    
    paper.update(1/60)
    rafale.update(1/60)
    mig.update(1/60)
    
    screen.blit(background, (0,0))
    
    screen.blit(paper.image,paper.rect)
    screen.blit(rafale.image,rafale.rect)
    screen.blit(mig.image,mig.rect)

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    time.sleep(1/60)
    
