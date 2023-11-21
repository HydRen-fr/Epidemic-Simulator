import pygame
import pygame_gui
import sys
pygame.init()

# Initialisation de Pygame
pygame.display.set_caption('Interface Utilisateur')
window_surface = pygame.display.set_mode((800, 600))

# Initialisation du gestionnaire d'interface Pygame GUI
manager = pygame_gui.UIManager((800, 600))
img = pygame.image.load('gear_icon.png')


img1 = pygame_gui.elements.UIImage(pygame.Rect((50, 50), (50, 50)),
                                   img,
                                   manager)
img2 = img1.set_image(img) 


# Ajout d'un bouton avec une image d'engrenage
settings_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((50, 50), (50, 50)),
                                               text='',
                                               manager=manager,
                                               container=None)
settings_button.set_image(img2)  # Assure-toi d'avoir une image nommée 'gear_icon.png'

# Liste des noms pour les boutons supplémentaires
button_names = ['Bouton {}'.format(i) for i in range(1, 11)]

# Positions initiales des boutons supplémentaires
button_positions = [(50, 150 + i * 40) for i in range(10)]

# Création des boutons supplémentaires
buttons = [pygame_gui.elements.UIButton(relative_rect=pygame.Rect(position, (100, 30)),
                                       text=name,
                                       manager=manager,
                                       container=None) for position, name in zip(button_positions, button_names)]

# Boucle principale
clock = pygame.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Gestion des événements pour le gestionnaire d'interface
        manager.process_events(event)

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Action à effectuer lorsque l'un des boutons est pressé
                if event.ui_element == settings_button:
                    print('Bouton "Réglages" pressé.')
                elif event.ui_element in buttons:
                    print(f'Bouton "{event.ui_element.text}" pressé.')

    # Mise à jour de l'interface
    manager.update(time_delta)

    # Rendu de l'interface
    window_surface.fill((255, 255, 255))
    manager.draw_ui(window_surface)

    pygame.display.update()

pygame.quit()
