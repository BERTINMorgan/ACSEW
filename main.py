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

Rafale = Plane(name="Rafale", pos = [1080,0])
Mig = Plane(name="Mig",pos=[500,500],throttle = 0.2)
Paper = Plane(name="Paper",cap = -135)
Drone = Plane(name="Drone",cap = -135,pos = [30,30])


sim.add_plane(Rafale)
sim.add_plane(Mig)
sim.add_plane(Paper)
sim.add_plane(Drone)

last_mouse_button_statu = 0

while sim.running: 
    
    
    Mig.cap = Mig.cap + 60 * 1/60
    Rafale.cap = sim_env.target_direction(Rafale, Mig)
    Rafale.throttle = sim_env.target_distance(Rafale, Mig)/800
    
    sim.update()

    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sim.running = False
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                sim.player_canon(Rafale)
            if event.key == pygame.K_RETURN:
                sim.player_switch_radar(Rafale)
        if event.type == pygame.MOUSEWHEEL:
            sim.scroll(event.y)



    time.sleep(sim.dt)
    
