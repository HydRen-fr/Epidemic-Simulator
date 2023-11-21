from classes import *


# Importation des modules nécessaires
import pygame  # Bibliothèque pour la création de jeux-vidéos
import random  # Module pour la génération de nombres aléatoires
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interprétateur python
import math # Calculs du cercle à partir du rayon par exemple


# Initialisation des modules Pygame manuellement
pygame.display.init()
pygame.font.init()

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Epydemie")



# Création d'une liste d'individus pour la simulation
individus = [Individu(
    random.randint(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU),
    random.randint(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (255, 0, 0)  # Couleur pour le premier individu (en rouge)
)] + [Individu(
    random.randint(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU),
    random.randint(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (0, 0, 255)  # Couleur pour les autres individus (en bleu)
) for i in range(NB_INDIVIDUS - 1)]

    

# Boucle principale de la simulation
while True:
    # Quitter sans problèmes en fermant la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            

    # Dessiner le fond blanc
    ecran.fill(COULEUR_FOND)

    # Dessiner le cadre noir
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(EMPLACEMENT_CARRE_X, EMPLACEMENT_CARRE_Y, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Dessiner le cadre de la quarantaine
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(EMPLACEMENT_QUARANTAINE_X, EMPLACEMENT_QUARANTAINE_Y, TAILLE_QUARANTAINE, TAILLE_QUARANTAINE), 2)


    # Filtrer les individus en vie
    individus = [ind for ind in individus if ind.vie]

    # Appliquer la distanciation sociale si c'est demandé
    if RAYON_DISTANCIATION:
        for individu in individus:
            if individu.est_en_quarantaine == False:
                individu.appliquer_distanciation(individus)

    # Déplacer et faire rebondir les individus dans le cadre
    for individu in individus:
        individu.progresser_guerison()
        individu.placer_en_quarantaine()
        individu.gestion_quarantaine()
        individu.bouger()
        individu.rebondir_sur_murs()
        individu.dessiner()



    
    # Vérifier les collisions en cours
    collisions_en_cours = [(i, j) for (i, j) in collisions_en_cours if i.detecter_collision(j)]

    # Tester les collisions et mettre à jour les couleurs
    ind_no_quarantaine = [ind for ind in individus if ind.est_en_quarantaine == False]
    for i in range(len(ind_no_quarantaine)):
        for j in range(i + 1, len(ind_no_quarantaine)):
            if (ind_no_quarantaine[i], ind_no_quarantaine[j]) not in collisions_en_cours and ind_no_quarantaine[i].detecter_collision(ind_no_quarantaine[j]):
                collisions_en_cours.append((ind_no_quarantaine[i], ind_no_quarantaine[j]))
                # L'un des deux est rouge
                if ind_no_quarantaine[i].couleur == (255, 0, 0) or ind_no_quarantaine[j].couleur == (255, 0, 0):
                    # Utiliser random.random() pour générer un nombre entre 0 et 1
                    if random.random() < TAUX_INFECTIOSITE:
                        ind_no_quarantaine[i].infecter(), ind_no_quarantaine[j].infecter()  # Rouges tous les deux

    # Mettre à jour l'affichage
    pygame.display.flip()