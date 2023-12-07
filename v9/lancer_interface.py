import pygame
import pygame_gui
from pygame_gui.elements import UIHorizontalSlider, UIButton, UILabel
from constantes import LARGEUR_ECRAN, HAUTEUR_ECRAN
import le_cosmos


# Définition des paramètres par défaut en attendant une modification
# Via l'interface utilisateur
parametres_de_base = {
        "NB_INDIVIDUS": 135,  # Nombre total d'individus dans la simulation
        "VITESSE_MAX": 0.5,  # Vitesse maximale des individus. Influence la propagation.
        "TAUX_INFECTIOSITE": 0.5,  # La probabilité d'être infecté. Entre 0 et 1.
        "TAUX_ASYMPTOMATIQUES": 0.55,  # La probabilité d'être asymptomatique et jamais envoyé en quarantaine. Entre 0 et 1.
        "LETALITE": 0.2,  # Chances de mourir du virus
        "LA_QUARANTAINE": True,  # Quarantaine ou pas
        "RAYON_DISTANCIATION": False,  # Distanciation sociale ou pas (difficile de le faire modulable)
        "TAUX_DISSIDENTS": 0.2,  # La probabilité d'être un individu qui n'écoute pas les consignes de distanciation
        # Modes de simulation
        "VILLE_CENTRALE": False,  # Activer le mode "Ville centrale"
        "COMMUNAUTES": False,  # Activer le mode "Communautés"
        "PROBABILITE_VOYAGE_VERS_VILLE": 0.5,  # Probabilité de voyage vers la ville
        # Doit être très basse car les tours de boucle s'enchaînent très vite --> 10**-2
        "PROBABILITE_VOYAGE_VERS_COMMUNAUTE": 0.6,  # Probabilité de voyage vers une autre communauté
        # Doit être très basse car les tours de boucle s'enchaînent très vite --> 10**-3
        }


class Lancement:
    def __init__(self, params):
        # Création d'une instance de la classe Cosmos pour gérer la simulation
        self.cosmos = le_cosmos.Cosmos(params)
        self.cosmos.simulation()


class Parametres:
    def __init__(self, derniers_params_utilises):
        pygame.init()

        # Police pour écrire
        self.font = pygame.font.Font(None, 60)

        self.ui_manager = pygame_gui.UIManager((LARGEUR_ECRAN, HAUTEUR_ECRAN))
        self.ui_manager.get_theme().load_theme('v9/horizontal_slider.json')
        self.ui_manager.get_theme().load_theme('v9/slider_label.json')
        self.ui_manager.get_theme().load_theme('v9/bool_button.json')
        

        self.label_mini_maxi = [
            ("Nombre d'individus", 1, 270),
            ("Vitesse maximale", 0.1, 1),
            ("Taux d'infectiosité", 0.1, 1),
            ("Taux d'asymptomatiques", 0.1, 1),
            ("Létalité", 0.1, 1),
            ("Quarantaine", None, None),
            ("Distanciation", None, None),
            ("Taux de dissidents", 0.1, 1),
            ("Ville centrale", None, None),
            ("Communautés", None, None),
            ("Probabilité de voyage vers la ville", 0, 1),
            ("Probabilité de voyage vers une autre communauté", 0, 1)
        ]

        self.constantes_liste = [
            (param, label, mini, maxi, derniers_params_utilises[param]) \
            for param, (label, mini, maxi) in zip(derniers_params_utilises.keys(), self.label_mini_maxi)
        ]

        # Dictionnaire pour stocker les valeurs du moment avec leur nom de variable
        self.nvar_current_values = {nvar: default_val for (nvar, _, _, _, default_val) in self.constantes_liste}

        # Chargement de l'image de la flèche retour et redimensionnement
        original_arrow_image = pygame.image.load("v9/imgs/go_back_arrow.png")
        new_width = 100
        new_height = 100
        self.arrow_image = pygame.transform.scale(original_arrow_image, (new_width, new_height))

        # Utilisation des constantes pour placer l'image en haut à droite
        self.arrow_rect = self.arrow_image.get_rect()
        self.arrow_rect.topright = (130, 10)

        self.create_ui()

    def create_ui(self):
        self.y_offset = 120
        self.elements = []

        for index, (nvar, label, min_val, max_val, default_val) in enumerate(self.constantes_liste):
            label_text = f"{label}: {nvar}"

            if isinstance(default_val, bool):
                button_rect = pygame.Rect((380, self.y_offset), (350, 30))
                button_value = default_val
                button = UIButton(button_rect, f"{label} - {'OUI' if button_value else 'NON'}", self.ui_manager, None, object_id=f'#bool_button_{index}')
                self.elements.append((button, None, index, label, nvar))
            else:
                slider_rect = pygame.Rect((380, self.y_offset), (300, 30))
                slider = UIHorizontalSlider(slider_rect, default_val, (min_val, max_val), self.ui_manager, None, object_id='#horizontal_slider')
                slider.set_current_value(default_val)

                value_label_rect = pygame.Rect((630, self.y_offset), (830, 30))
                value_label = UILabel(value_label_rect, label_text, self.ui_manager, None, object_id='#slider_label')
                self.elements.append((slider, value_label, index, label, nvar))

                min_label_rect = pygame.Rect((345, self.y_offset), (30, 30))
                min_label = UILabel(min_label_rect, str(min_val), self.ui_manager, None, object_id='#slider_label')

                max_label_rect = pygame.Rect((685, self.y_offset), (30, 30))
                max_label = UILabel(max_label_rect, str(max_val), self.ui_manager, None, object_id='#slider_label')

            self.y_offset += 60


    def update_ui(self):
        for element_data in self.elements:
            element = element_data[0]
            label = element_data[3]
            nvar = element_data[4]
            value_label = element_data[1]  # Que pour UIHorizontalSlider
            
            if isinstance(element, UIButton):
                if element.check_pressed():
                    # Inverser le booléen
                    self.nvar_current_values[nvar] = not self.nvar_current_values[nvar]
                    element.set_text(f"{label} - {'OUI' if self.nvar_current_values[nvar] else 'NON'}")
            elif isinstance(element, UIHorizontalSlider):
                self.nvar_current_values[nvar] = round(element.get_current_value(), 2)
                value_label.set_text(f"{label}: {self.nvar_current_values[nvar]}")


    def run(self):
        clock = pygame.time.Clock()
        is_running = True

        while is_running:
            time_delta = clock.tick(60) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    is_running = False

                self.ui_manager.process_events(event)

                # Vérifier si le clic de souris a eu lieu sur l'image de flèche
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.arrow_rect.collidepoint(event.pos):
                        # Relancer la simulation avec de nouveaux paramètres
                        Lancement(self.nvar_current_values)


            self.ui_manager.update(time_delta)
            self.update_ui()

            # Écran blanc
            le_cosmos.ecran.fill((255, 255, 255))
            # Dessiner la flèche retour
            le_cosmos.ecran.blit(self.arrow_image, self.arrow_rect)
            # Titre explicite
            titre = self.font.render("Paramètres modulables", True, (0, 0, 0))
            le_cosmos.ecran.blit(titre, (LARGEUR_ECRAN//2 - 230, 30))
            # Le reste
            self.ui_manager.draw_ui(le_cosmos.ecran)

            pygame.display.flip()

        pygame.quit()


if __name__ == '__main__':
    Lancement(parametres_de_base)