# Importation des modules nécessaires
import pygame  # Bibliothèque pour la création de jeux-vidéos
import random  # Module pour la génération de nombres aléatoires
import math # Calculs du cercle à partir du rayon par exemple

from constantes import * # On importe les variables de constantes.py

import modes
import prevention

import le_cosmos 

class Individu:
    def __init__(self, x, y, taille, couleur, cosmos):
        self.x = x
        self.y = y
        self.taille = taille
        self.couleur = couleur
        # NB_INDIVIDUS AUGMENTE = NB OPÉS AUGMENTE = VITESSE PLUS LENTE = GUERISON PLUS LONGUE mais ça reste correct juste c'est pas beau
        # Vitesse + rapide pour un grand nombre
        self.vitesse_x = (random.uniform(-cosmos.constantes_parametrables["VITESSE_MAX"], cosmos.constantes_parametrables["VITESSE_MAX"]) * cosmos.constantes_parametrables["NB_INDIVIDUS"]) / 10
        self.vitesse_y = (random.uniform(-cosmos.constantes_parametrables["VITESSE_MAX"], cosmos.constantes_parametrables["VITESSE_MAX"]) * cosmos.constantes_parametrables["NB_INDIVIDUS"]) / 10
        self.temps_infecte = 0
        # Guérison + courte pour un grand nombre
        self.temps_guerison = random.randint(200000, 600000) * (1/cosmos.constantes_parametrables["NB_INDIVIDUS"])
        self.gueri = False

        self.reperage_quarantaine = random.randint(80000, 200000) * (1/cosmos.constantes_parametrables["NB_INDIVIDUS"])
        self.est_en_quarantaine = False

        self.asymptomatique = False
        # Utiliser random.random() pour générer un nombre entre 0 et 1
        if random.random() < cosmos.constantes_parametrables["TAUX_ASYMPTOMATIQUES"]:
            self.asymptomatique = True

        self.dissident = False
        # Utiliser random.random() pour générer un nombre entre 0 et 1
        if random.random() < cosmos.constantes_parametrables["TAUX_DISSIDENTS"]:
            self.dissident = True

        self.vie = True

        self.est_dans_ville_centrale = (EMPLACEMENT_VILLE_X <= self.x <= EMPLACEMENT_VILLE_X + TAILLE_VILLE) and \
                           (EMPLACEMENT_VILLE_Y <= self.y <= EMPLACEMENT_VILLE_Y + TAILLE_VILLE)

    def dessiner(self):
        pygame.draw.circle(le_cosmos.ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    
    def bouger(self, cosmos):
        # Si le mode "Ville centrale" est activé + pas en quarantaine, vérifier si l'individu doit se déplacer
        if not(self.est_en_quarantaine) and cosmos.constantes_parametrables["VILLE_CENTRALE"] \
            and random.random() < cosmos.constantes_parametrables["PROBABILITE_VOYAGE_VERS_VILLE"]:
            modes.Ville_Centrale.voyager(self)

        # Si le mode "Communautés" est activé + pas en quarantaine, vérifier si l'individu doit changer de communauté
        elif not(self.est_en_quarantaine) and cosmos.constantes_parametrables["COMMUNAUTES"] \
            and random.random() < cosmos.constantes_parametrables["PROBABILITE_VOYAGE_VERS_COMMUNAUTE"]:
            modes.Communautes.changer_de_communaute(self, cosmos)

        else:
            self.x += self.vitesse_x
            self.y += self.vitesse_y

    def rebondir_sur_murs(self, cosmos):
        # Vérifier si l'individu atteint les bords du cadre et les fait rebondir en conséquence
        # Utiliser la ou les méthodes adaptées
        if not self.est_en_quarantaine:
            
            if cosmos.constantes_parametrables["COMMUNAUTES"]:
                modes.Communautes.rebondir_sur_murs_communautes(self, cosmos)

            if self.x - self.taille < EMPLACEMENT_CARRE_X:
                self.x = EMPLACEMENT_CARRE_X + self.taille
                self.vitesse_x = -self.vitesse_x
            elif self.x + self.taille > EMPLACEMENT_CARRE_X_CONJ:
                self.x = EMPLACEMENT_CARRE_X_CONJ - self.taille
                self.vitesse_x = -self.vitesse_x

            if self.y - self.taille < EMPLACEMENT_CARRE_Y:
                self.y = EMPLACEMENT_CARRE_Y + self.taille
                self.vitesse_y = -self.vitesse_y
            elif self.y + self.taille > EMPLACEMENT_CARRE_Y_CONJ:
                self.y = EMPLACEMENT_CARRE_Y_CONJ - self.taille
                self.vitesse_y = -self.vitesse_y

        else:
            prevention.Quarantaine.rebondir_sur_murs_quarantaine(self)

        

        
    

    def detecter_collision(self, autre_individu):
        # Calculer la distance entre deux individus et tester s'ils entrent en collision
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

    def infecter(self):
        self.couleur = (255, 0, 0) # Couleur d'un individu qui est infecté (en rouge)
        self.gueri = False # Perd le statut de guéri

    def appliquer_distanciation(self, individus):
        # Si on est pas dissident soi-même et pas à l'intérieur de la ville
        if not self.dissident and not self.est_dans_ville_centrale:

            # Pour chaque individu différent de nous-mêmes
            autres_individus = list(individus)
            autres_individus.remove(self)
            for autre in autres_individus:

                # Si l'autre n'est pas dissident non plus
                if not autre.dissident:

                    # Calculer la distance entre deux individus
                    distance = ((self.x - autre.x) ** 2 + (self.y - autre.y) ** 2) ** 0.5
                    # Si la distance est en-dessous de 10 on fait des changements de direction
                    # Difficile de mettre une valeur autre que 10
                    if distance < 10:
                        angle = random.uniform(0, 2 * math.pi)
                        deplacement_x = 10 * math.cos(angle)
                        deplacement_y = 10 * math.sin(angle)
                        self.x += deplacement_x
                        self.y += deplacement_y