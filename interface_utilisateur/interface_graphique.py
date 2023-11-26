import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID
from pygame_gui.elements import UIButton

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 600))

background = pygame.Surface((800, 600))
background.fill(pygame.Color('#000000'))

manager = pygame_gui.UIManager((800, 600), 'theme.json')

hello_button = UIButton(relative_rect=pygame.Rect((350, 280), (-1, -1)),
                        text='Hello',
                        manager=manager,
                        object_id=ObjectID(class_id='@friendly_buttons',
                                           object_id='#hello_button'))

clock = pygame.time.Clock()
is_running = True

while is_running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
            
            time_delta = clock.tick(60)/1000.0
    
            
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == hello_button:
                print('Hello World!')            

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
