# -*- coding: utf-8 -*-

from .screen import screen, screen_width, screen_height, monitor_diagonal
from .write import *
from .meta import *

import os
import pygame
import time as builtin_time
import numpy as np
import datetime


def fill_form(questions, size = 1.0):
    
    #font = pygame.font.Font(None, 32)
    
    font = Font.get('RobotoRegular.ttf', int(size*screen_width/35.0))
    
    clock = pygame.time.Clock()
    input_box = pygame.Rect(500, 100, 140, 32)
    color_inactive = pygame.Color('grey')
    color_active = pygame.Color('black')
    
    text = ''
      
    pygame.mouse.set_visible(True)
    answers = {}

    x_plus = Coordinates.to_pygame(x= 2)
    x_minus = Coordinates.to_pygame(x= -5)
    
    input_box_y = [Coordinates.to_pygame(y= -(i+1)*1.5 + 2) for i in range (len(questions))]
    
    for i, question in enumerate(questions):
        

        
        input_box = pygame.Rect(x_plus, 
                                input_box_y[i], 
                                140, 50)
        done = False
        
        while not done:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
  
                    if event.key == pygame.K_RETURN:
                        answers[question] = text
                        text = ''
                        done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
    
            screen.fill(color('white'))

            write('\n\n Veuillez compléter les informations suivantes :', size=1.0, long_text=True)
            write('\n\n\n\n (Appuyez sur ENTRER pour valider votre saisie)', size=0.8, long_text=True)
                    
            surface = font.render(question, True, color_active)
            screen.blit(surface, (x_minus, input_box.y +5))            
            
            
            for j, askd_question in enumerate(answers.keys()):
           
                surface = font.render(askd_question, True, color_inactive)
                screen.blit(surface, (x_minus, input_box_y[j] + 5))       
            
                surface = font.render(answers[askd_question], True, color_inactive)
                screen.blit(surface, (x_plus, input_box_y[j] + 5))             
            
            txt_surface = font.render(text, True, color_active)

            width = max(200, txt_surface.get_width()+10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x+5, input_box.y+5))

            pygame.draw.rect(screen, color_active, input_box, 2)
    
            pygame.display.flip()  
            clock.tick(30) 
          
    return answers
    
    
    
    
    
    