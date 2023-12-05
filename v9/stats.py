# Importation des modules nécessaires
import pygame  # Bibliothèque pour la création de jeux-vidéos

from constantes import * # On importe les variables de constantes.py

# Initialisation du module Pygame font manuellement
pygame.font.init()

import le_cosmos

class Stats:
    def __init__(self):
        # Initialisation des listes pour les statistiques
        # On met la ligne des bleus de base à 160 pour que ça fasse pas vide au début
        self.historique_bleus = [160 for _ in range(LARGEUR_ECRAN)]
        self.historique_rouges = [0 for _ in range(LARGEUR_ECRAN)]
        self.historique_verts = [0 for _ in range(LARGEUR_ECRAN)]
        self.historique_morts = [0 for _ in range(LARGEUR_ECRAN)]
        # Police pour écrire
        self.font = pygame.font.Font(None, 36)

    def afficher_statistiques(self, nb_bleus, nb_rouges, nb_verts, nb_morts):
        # Afficher les statistiques en temps réel
        texte_bleus = self.font.render(f"Non exposés : {nb_bleus}", True, (0, 0, 255))
        texte_rouges = self.font.render(f"Infectés : {nb_rouges}", True, (255, 0, 0))
        texte_verts = self.font.render(f"Guéris : {nb_verts}", True, (0, 255, 0))
        texte_morts = self.font.render(f"Morts : {nb_morts}", True, (169, 169, 169))
        le_cosmos.ecran.blit(texte_bleus, (10, 10))
        le_cosmos.ecran.blit(texte_rouges, (10, 50))
        le_cosmos.ecran.blit(texte_verts, (10, 90))
        le_cosmos.ecran.blit(texte_morts, (10, 130))

    def actualiser_courbes(self, nb_bleus, nb_rouges, nb_verts, nb_morts, cosmos):
        # Ajouter les valeurs actuelles à l'historique
        self.historique_bleus.append(nb_bleus)
        self.historique_rouges.append(nb_rouges)
        self.historique_verts.append(nb_verts)
        self.historique_morts.append(nb_morts)

        # Coefficienter avec 160 pour garder un affichage stable peu importe NB_INDIVIDUS
        self.historique_bleus[-1] *= (160 / cosmos.constantes_parametrables["NB_INDIVIDUS"])
        self.historique_rouges[-1] *= (160 / cosmos.constantes_parametrables["NB_INDIVIDUS"])
        self.historique_verts[-1] *= (160 / cosmos.constantes_parametrables["NB_INDIVIDUS"])
        self.historique_morts[-1] *= (160 / cosmos.constantes_parametrables["NB_INDIVIDUS"])

        # Ne garder que les données qui apparaissent sur l'écran pour éviter de surcharger
        self.historique_bleus = self.historique_bleus[-LARGEUR_ECRAN:]
        self.historique_rouges = self.historique_rouges[-LARGEUR_ECRAN:]
        self.historique_verts = self.historique_verts[-LARGEUR_ECRAN:]
        self.historique_morts = self.historique_morts[-LARGEUR_ECRAN:]

    def afficher_courbes(self):
        # Dessiner les courbes statistiques en temps réel avec des points
        for i in range(len(self.historique_bleus)):
            x = i

            y_bleus = (HAUTEUR_ECRAN - self.historique_bleus[i] - 50)
            y_rouges = (HAUTEUR_ECRAN - self.historique_rouges[i] - 50)
            y_verts = (HAUTEUR_ECRAN - self.historique_verts[i] - 50)
            y_morts = (HAUTEUR_ECRAN - self.historique_morts[i] - 50)

            pygame.draw.circle(le_cosmos.ecran, (0, 0, 255), (x, y_bleus), 2) # Point bleu
            pygame.draw.circle(le_cosmos.ecran, (255, 0, 0), (x, y_rouges), 2) # Point rouge
            pygame.draw.circle(le_cosmos.ecran, (0, 255, 0), (x, y_verts), 2) # Point vert
            pygame.draw.circle(le_cosmos.ecran, (169, 169, 169), (x, y_morts), 2) # Point gris

        # Indications pour les valeurs des courbes
        text_100p = self.font.render("100%", True, (0, 0, 0))
        text_0p = self.font.render("0%", True, (0, 0, 0))
        # On les place proportionnellement à l'écran
        le_cosmos.ecran.blit(text_100p, (10, HAUTEUR_ECRAN - 250))
        le_cosmos.ecran.blit(text_0p, (10, HAUTEUR_ECRAN - 35))