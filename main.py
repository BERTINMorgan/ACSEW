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

Rafale = Plane(name="Rafale", pos = [10000,10000])
Mig = Plane(name="Mig",pos=[800,360],throttle = 0.2)
Paper = Plane(name="Paper",cap = -135)
Drone = Plane(name="Drone",cap = -135,pos = [30,30])


sim.add_plane(Rafale)
sim.add_plane(Mig)
sim.add_plane(Paper)
sim.add_plane(Drone)

last_mouse_button_statu = 0
pygame.mixer.init()
crash_sound = pygame.mixer.Sound("data/sounds/shot.wav")

while sim.running: 
    
    Mig.cap += 25 * sim.dt
    
    sim.update()

    pygame.display.flip()
    
    if sim.pressed.get(pygame.K_SPACE):
        sim.player_canon(Rafale)
        pygame.mixer.Sound.play(crash_sound)
        pygame.mixer.music.stop()
    if sim.pressed.get(pygame.K_RETURN):
        sim.player_switch_radar(Rafale)
    if sim.pressed.get(pygame.K_LEFT):
        sim.turn_left(Rafale)
    elif sim.pressed.get(pygame.K_RIGHT):
        sim.turn_right(Rafale)
    else:
        sim.straight(Rafale)
    if sim.pressed.get(pygame.K_UP):
        sim.throttle_up(Rafale)
    if sim.pressed.get(pygame.K_DOWN):
        sim.throttle_down(Rafale)

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
    
