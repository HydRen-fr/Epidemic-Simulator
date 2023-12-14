# Constantes non paramétrables par l'utilisateur

LARGEUR_ECRAN = 1450  # Largeur de la fenêtre de la simulation
HAUTEUR_ECRAN = 800  # Hauteur de la fenêtre de la simulation
COULEUR_MUR = (0, 0, 0)  # Couleur des bords de la fenêtre de la simulation (en noir)
COULEUR_FOND = (255, 255, 255)  # Couleur du fond de la fenêtre de la simulation (en blanc)
TAILLE_INDIVIDU = 4  # Taille des individus représentés par des points

# Grand carré
TAILLE_CARRE = 500
EMPLACEMENT_CARRE_X = (LARGEUR_ECRAN - TAILLE_CARRE) // 2
EMPLACEMENT_CARRE_Y = (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 - 100
# Conjugués des emplacements (signe inverse)
EMPLACEMENT_CARRE_X_CONJ = (LARGEUR_ECRAN + TAILLE_CARRE) // 2
EMPLACEMENT_CARRE_Y_CONJ = (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - 100

# Carré de quarantaine - proportionnel au grand carré
TAILLE_QUARANTAINE = TAILLE_CARRE * 0.28
EMPLACEMENT_QUARANTAINE_X = EMPLACEMENT_CARRE_X + (TAILLE_CARRE * 1.085)
EMPLACEMENT_QUARANTAINE_Y = EMPLACEMENT_CARRE_Y

# Ville et communautés
TAILLE_VILLE = TAILLE_CARRE // 7
EMPLACEMENT_VILLE_X = (EMPLACEMENT_CARRE_X + EMPLACEMENT_CARRE_X_CONJ - TAILLE_VILLE) // 2
EMPLACEMENT_VILLE_Y = (EMPLACEMENT_CARRE_Y + EMPLACEMENT_CARRE_Y_CONJ - TAILLE_VILLE) // 2
TAILLE_COMMUNAUTE = TAILLE_CARRE // 3 # Donne une grille 3x3




