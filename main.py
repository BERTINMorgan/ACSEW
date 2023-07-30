# -*- coding: utf-8 -*-
"""
Created on Wed Jun 21 09:28:18 2023

@author: JALOUX Matisse, BERTIN Morgan, LAMONTAGNE Corentin
"""

from plane_object import Plane
import pygame
import numpy as np
import time
import simulation_environement as sim_env


sim = sim_env.Simulation()

Rafale = Plane(name="Rafale", pos = [500,500])
Mig = Plane(name="Mig",pos=[800,360],throttle = 0.2)
Paper = Plane(name="Paper",cap = -135)
Drone = Plane(name="Drone",cap = -135,pos = [30,30])
F22 = Plane(name="F22",cap = -135,pos = [-30,-30])
AWACS = Plane(name="AWACS",cap = -90,pos = [500,20])


#sim.add_plane(Rafale)
#sim.add_plane(Paper)
sim.add_plane(Mig)
#sim.add_plane(Drone)
#sim.add_plane(F22)
sim.add_plane(AWACS)

pygame.mixer.init()
crash_sound = pygame.mixer.Sound("data/sounds/shot.wav")

piloted_plane = AWACS

while sim.running: 
    
    Mig.cap += 25 * sim.dt    
    AWACS.cap -= 10 * sim.dt
    
    F22.cap = sim_env.target_direction(F22,Rafale)
    F22.throttle = sim_env.target_distance(F22,Rafale)/500
      
    sim.update()

    pygame.display.flip()
    
    if sim.pressed.get(pygame.K_SPACE):
        sim.player_canon(piloted_plane)
        pygame.mixer.Sound.play(crash_sound)
        pygame.mixer.music.stop()
    if sim.pressed.get(pygame.K_RETURN):
        sim.player_switch_radar(piloted_plane)
    if sim.pressed.get(pygame.K_LEFT):
        sim.turn_left(piloted_plane)
    elif sim.pressed.get(pygame.K_RIGHT):
        sim.turn_right(piloted_plane)
    else:
        sim.straight(piloted_plane)
    if sim.pressed.get(pygame.K_UP):
        sim.throttle_up(piloted_plane)
    if sim.pressed.get(pygame.K_DOWN):
        sim.throttle_down(piloted_plane)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sim.running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            sim.pressed[event.key] = True
        if event.type == pygame.KEYUP:
            sim.pressed[event.key] = False
            
        if event.type == pygame.MOUSEWHEEL:
            sim.scroll(event.y)


    time.sleep(sim.dt)
    
