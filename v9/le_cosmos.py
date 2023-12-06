# Importation des modules nécessaires
import pygame  # Bibliothèque pour la création de jeux-vidéos
import random  # Module pour la génération de nombres aléatoires
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interprétateur python

from constantes import * # On importe les variables de constantes.py

import modes
import les_individus
import prevention
import stats

import lancer_interface
from pygame.locals import MOUSEBUTTONDOWN # Checker les clics


# Initialisation du module pygame display manuellement. Peut éviter des bugs.
pygame.display.init()

# Création de la fenêtre de simulation
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Epydemie")


class Cosmos:
    def __init__(self, les_parametres):
        # On stocke en attribut les paramètres qui seront les constantes de la simulation
        # dict() évite une erreur mémoire
        self.constantes_parametrables = dict(les_parametres)
        # Ajustements pour la simulation
        self.constantes_parametrables["PROBABILITE_VOYAGE_VERS_VILLE"] *= 10**-2
        # Doit être très basse car les tours de boucle s'enchaînent très vite --> 10**-2
        self.constantes_parametrables["PROBABILITE_VOYAGE_VERS_COMMUNAUTE"] *= 10**-3
        # Encore plus ici --> 10**-3

        # Paramètres changés ou pas - condition while
        self.pas_de_changements = True
        
        # Si demandé on active la grille des communautés
        if self.constantes_parametrables["COMMUNAUTES"]:
            self.nb_communautes_x = TAILLE_CARRE // TAILLE_COMMUNAUTE
            self.nb_communautes_y = TAILLE_CARRE // TAILLE_COMMUNAUTE
            self.communautes = modes.Communautes.initialiser_communautes(self)

        # Liste des individus qui prendront part à la simulation
        self.individus = self.initialiser_individus()

        # Liste des couples d'individus en collision
        self.collisions_en_cours = []

        # Compteur des individus morts
        self.nb_morts = 0

        # Chargement de l'image du bouton et redimensionnement
        original_button_image = pygame.image.load("doc/parametres.png")
        new_width = 145
        new_height = 145
        self.button_image = pygame.transform.scale(original_button_image, (new_width, new_height))

        # Utilisation des constantes pour placer l'image en haut à droite
        self.button_rect = self.button_image.get_rect()
        self.button_rect.topright = (LARGEUR_ECRAN-10, 10)


        self.stats = stats.Stats()
        self.parametres = lancer_interface.Parametres(les_parametres)


    def initialiser_individus(self):
        # Création d'une liste d'individus pour la simulation
        individus = []

        if self.constantes_parametrables["COMMUNAUTES"]:
            for i in range(self.constantes_parametrables["NB_INDIVIDUS"]):
                communaute_x, communaute_y = modes.Communautes.choisir_communaute(self)
                x = random.uniform(communaute_x, communaute_x + TAILLE_COMMUNAUTE - TAILLE_INDIVIDU)
                y = random.uniform(communaute_y, communaute_y + TAILLE_COMMUNAUTE - TAILLE_INDIVIDU)
                couleur = (0, 0, 255)  # Bleu par défaut
                if i == 0:
                    couleur = (255, 0, 0)  # Rouge pour le premier individu infecté
                individus.append(les_individus.Individu(x, y, TAILLE_INDIVIDU, couleur, self))


            
        else:
            individus = [
                les_individus.Individu(
                    random.randint(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU),
                    random.randint(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU),
                    TAILLE_INDIVIDU,
                    (255, 0, 0),  # Rouge pour le premier individu infecté
                    self,
                )
            ] + [
                les_individus.Individu(
                    random.randint(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU),
                    random.randint(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU),
                    TAILLE_INDIVIDU,
                    (0, 0, 255),  # Bleu par défaut
                    self,
                ) for _ in range(self.constantes_parametrables["NB_INDIVIDUS"] - 1)
            ]
        
        return individus        


    def simulation(self):
        # Boucle principale de la simulation
        while self.pas_de_changements:

            # Permet de quitter sans problème en fermant la fenêtre
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == MOUSEBUTTONDOWN:
                    # Vérifier si le clic de souris a eu lieu sur le bouton
                    if self.button_rect.collidepoint(event.pos):
                        # On ouvre les paramètres
                        self.parametres.run()
                        self.pas_de_changements = False
                        # Une fois l'interface fermée ça repart avec les modifs

            
            # DESSINS

            # Dessiner le fond blanc
            ecran.fill(COULEUR_FOND)

            # Dessiner le bouton
            ecran.blit(self.button_image, self.button_rect.topleft)

            if self.constantes_parametrables["LA_QUARANTAINE"]:
                # Dessiner le cadre de la quarantaine
                pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(EMPLACEMENT_QUARANTAINE_X, EMPLACEMENT_QUARANTAINE_Y, TAILLE_QUARANTAINE, TAILLE_QUARANTAINE), 2)
            if self.constantes_parametrables["COMMUNAUTES"]:
                # Dessiner les communautés
                for communaute_x, communaute_y in self.communautes:
                    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(communaute_x, communaute_y, TAILLE_COMMUNAUTE, TAILLE_COMMUNAUTE), 2)
            else:
                # Dessiner le cadre noir
                pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(EMPLACEMENT_CARRE_X, EMPLACEMENT_CARRE_Y, TAILLE_CARRE, TAILLE_CARRE), 2)
                if self.constantes_parametrables["VILLE_CENTRALE"]:
                    # Dessiner la ville
                    pygame.draw.rect(ecran, (255, 165, 0), pygame.Rect(EMPLACEMENT_VILLE_X, EMPLACEMENT_VILLE_Y, TAILLE_VILLE, TAILLE_VILLE), 2)



            # ACTUALISATION DES VIVANTS ET MORTS + DISTANCIATION
                    
            # Filtrer les individus en vie
            self.individus = [ind for ind in self.individus if ind.vie]
            # Actualiser le nombre de morts
            self.nb_morts = self.constantes_parametrables["NB_INDIVIDUS"] - len(self.individus)

            # Appliquer la distanciation sociale si c'est demandé
            if self.constantes_parametrables["RAYON_DISTANCIATION"]:
                for individu in self.individus:
                    if not individu.est_en_quarantaine:
                        individu.appliquer_distanciation(self.individus)



            # ROUTINE
            # self en argument = donner accès aux attributs de Cosmos
            # Gérer le statut de chaque individu + déplacer et faire rebondir les individus dans le cadre
            for individu in self.individus:
                prevention.Guerison.progresser_guerison_ou_mort(individu, self)
                if self.constantes_parametrables["LA_QUARANTAINE"]:
                    prevention.Quarantaine.placer_en_quarantaine(individu)
                    prevention.Quarantaine.gestion_quarantaine(individu, self)
                individu.bouger(self)
                individu.rebondir_sur_murs(self)
                individu.dessiner()


            
            # COLLISIONS

            # Vérifier les collisions en cours
            self.collisions_en_cours = [(i, j) for (i, j) in self.collisions_en_cours if i.detecter_collision(j)]

            # Tester les collisions et mettre à jour les couleurs
            ind_no_quarantaine = [ind for ind in self.individus if not ind.est_en_quarantaine]
            for i in range(len(ind_no_quarantaine)):
                for j in range(i + 1, len(ind_no_quarantaine)):
                    if (
                        (ind_no_quarantaine[i], ind_no_quarantaine[j]) not in self.collisions_en_cours
                        and ind_no_quarantaine[i].detecter_collision(ind_no_quarantaine[j])
                    ):
                        self.collisions_en_cours.append((ind_no_quarantaine[i], ind_no_quarantaine[j]))
                        # L'un des deux est rouge
                        if ind_no_quarantaine[i].couleur == (255, 0, 0) or ind_no_quarantaine[j].couleur == (255, 0, 0):
                            # Utiliser random.random() pour générer un nombre entre 0 et 1
                            if random.random() < self.constantes_parametrables["TAUX_INFECTIOSITE"]:
                                # Si ça passe en-dessous du taux d'infectiosité on infecte
                                ind_no_quarantaine[i].infecter(), ind_no_quarantaine[j].infecter()




            # STATS

            # Compteurs pour les statistiques
            nb_bleus = sum(1 for ind in self.individus if ind.couleur == (0, 0, 255))
            nb_rouges = sum(1 for ind in self.individus if ind.couleur == (255, 0, 0))
            nb_verts = sum(1 for ind in self.individus if ind.couleur == (0, 255, 0))
            # nb_morts initialisé plus tôt et en attribut de la classe comme c'est linéaire

            self.stats.afficher_statistiques(nb_bleus, nb_rouges, nb_verts, self.nb_morts)
            self.stats.actualiser_courbes(nb_bleus, nb_rouges, nb_verts, self.nb_morts, self)
            self.stats.afficher_courbes()


            # MAJ AFFICHAGE
            pygame.display.flip()