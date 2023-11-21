# Constantes définissant les paramètres du programme

LARGEUR_ECRAN = 1300  # Largeur de la fenêtre de la simulation
HAUTEUR_ECRAN = 800  # Hauteur de la fenêtre de la simulation
COULEUR_MUR = (0, 0, 0)  # Couleur des bords de la fenêtre de la simulation (en noir)
COULEUR_FOND = (255, 255, 255)  # Couleur du fond de la fenêtre de la simulation (en blanc)

TAILLE_INDIVIDU = 4  # Taille des individus représentés par des points
NB_INDIVIDUS = 100  # Nombre total d'individus dans la simulation
VITESSE_MAX = 0.1  # Vitesse maximale des individus. Influence la propagation.
TAUX_INFECTIOSITE = 0.3  # La probabilité d'être infecté
TAUX_ASYMPTOMATIQUES = 0.2  # La probabilité d'être asymptomatique et jamais envoyé en quarantaine. Entre 0 et 1.
RAYON_DISTANCIATION = True # Distanciation sociale ou pas (difficile de le faire modulable)
LETALITE = 0.3 # Chances de mourir du virus


# Pour le grand carré
TAILLE_CARRE = 400  # Taille du cadre où les individus évoluent
EMPLACEMENT_CARRE_X = (LARGEUR_ECRAN - TAILLE_CARRE) // 2
EMPLACEMENT_CARRE_Y = (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 - 100
# Conjugués des emplacements (signe inverse)
EMPLACEMENT_CARRE_X_CONJ = (LARGEUR_ECRAN + TAILLE_CARRE) // 2
EMPLACEMENT_CARRE_Y_CONJ = (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - 100

# Pour le carré de quarantaine - proportionnel au grand carré
TAILLE_QUARANTAINE = TAILLE_CARRE * 0.28  # Taille du cadre de la quarantaine
EMPLACEMENT_QUARANTAINE_X = EMPLACEMENT_CARRE_X + (TAILLE_CARRE * 1.085)
EMPLACEMENT_QUARANTAINE_Y = EMPLACEMENT_CARRE_Y