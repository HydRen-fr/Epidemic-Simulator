import pygame
import pygame_gui
from pygame_gui.elements import UIWindow, UIButton, UIHorizontalSlider
from pygame_gui.windows import UIMessageWindow

# Constantes du jeu
LARGEUR_ECRAN = 1600
HAUTEUR_ECRAN = 1000
NB_INDIVIDUS = 200
VITESSE_MAX = 0.15

# Classe pour l'interface graphique
class InterfaceGraphique:
    def __init__(self):
        pygame.init()

        self.resolution = (800, 600)
        self.window_surface = pygame.display.set_mode(self.resolution)
        pygame.display.set_caption("Interface Graphique")

        self.ui_manager = pygame_gui.UIManager(self.resolution)

        self.create_main_window()
        self.create_ui()

    def create_main_window(self):
        # Fenêtre principale
        self.main_window = UIWindow(pygame.Rect((50, 50), (400, 300)),
                                    self.ui_manager,
                                    window_display_title="Menu Principal",
                                    object_id='#main_window',
                                    resizable=True)

        # Bouton pour ouvrir l'interface
        self.open_interface_button = UIButton(pygame.Rect((50, 50), (300, 50)),
                                              "Ouvrir l'Interface",
                                              self.ui_manager,
                                              container=self.main_window,
                                              object_id='#open_interface_button')

    def create_ui(self):
        # Fenêtre pour moduler les constantes
        self.constants_window = UIWindow(pygame.Rect((50, 50), (400, 300)),
                                         self.ui_manager,
                                         window_display_title="Modulateur de Constantes",
                                         object_id='#constants_window',
                                         resizable=True)

        # Slider pour le nombre d'individus
        self.nb_individus_slider = UIHorizontalSlider(pygame.Rect((50, 50), (300, 25)),
                                                      NB_INDIVIDUS,
                                                      (0, 500),
                                                      self.ui_manager,
                                                      container=self.constants_window,
                                                      object_id='#nb_individus_slider')

        # Bouton pour fermer l'interface
        self.close_interface_button = UIButton(pygame.Rect((50, 200), (300, 50)),
                                               "Fermer l'Interface",
                                               self.ui_manager,
                                               container=self.constants_window,
                                               object_id='#close_interface_button')

    def update(self, time_delta):
        self.ui_manager.update(time_delta)

        # Mettre à jour les constantes en temps réel
        if self.nb_individus_slider.has_moved_recently:
            NB_INDIVIDUS = int(self.nb_individus_slider.get_current_value())

    def run(self):
        clock = pygame.time.Clock()
        is_running = True
        open_interface = False

        while is_running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                self.ui_manager.process_events(event)

                # Gestion de l'ouverture de l'interface
                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.open_interface_button:
                            open_interface = True

                if event.type == pygame.USEREVENT:
                    if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self.close_interface_button:
                            open_interface = False

            self.window_surface.fill((255, 255, 255))

            # Affichage de l'interface appropriée
            if open_interface:
                self.constants_window.show()
                self.main_window.hide()
                self.update(time_delta)
            else:
                self.constants_window.hide()
                self.main_window.show()

            self.ui_manager.draw_ui(self.window_surface)

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    app = InterfaceGraphique()
    app.run()
