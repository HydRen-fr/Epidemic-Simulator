# Constantes définissant les paramètres du programme

LARGEUR_ECRAN = 1600  # Largeur de la fenêtre de la simulation
HAUTEUR_ECRAN = 1000  # Hauteur de la fenêtre de la simulation
COULEUR_MUR = (0, 0, 0)  # Couleur des bords de la fenêtre de la simulation (en noir)
COULEUR_FOND = (255, 255, 255)  # Couleur du fond de la fenêtre de la simulation (en blanc)

TAILLE_INDIVIDU = 4  # Taille des individus représentés par des points
NB_INDIVIDUS = 200  # Nombre total d'individus dans la simulation
VITESSE_MAX = 0.15  # Vitesse maximale des individus. Influence la propagation.

TAUX_INFECTIOSITE = 0.2  # La probabilité d'être infecté. Entre 0 et 1.
TAUX_ASYMPTOMATIQUES = 0.1  # La probabilité d'être asymptomatique et jamais envoyé en quarantaine. Entre 0 et 1.
LETALITE = 0.3 # Chances de mourir du virus

LA_QUARANTAINE = True # Quarantaine ou pas

RAYON_DISTANCIATION = False # Distanciation sociale ou pas (difficile de le faire modulable)
TAUX_DISSIDENTS = 0.05  # La probabilité d'être un individu qui n'écoute pas les consignes de distanciation



# Grand carré
TAILLE_CARRE = 600
EMPLACEMENT_CARRE_X = (LARGEUR_ECRAN - TAILLE_CARRE) // 2
EMPLACEMENT_CARRE_Y = (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 - 100
# Conjugués des emplacements (signe inverse)
EMPLACEMENT_CARRE_X_CONJ = (LARGEUR_ECRAN + TAILLE_CARRE) // 2
EMPLACEMENT_CARRE_Y_CONJ = (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - 100

# Carré de quarantaine - proportionnel au grand carré
TAILLE_QUARANTAINE = TAILLE_CARRE * 0.28
EMPLACEMENT_QUARANTAINE_X = EMPLACEMENT_CARRE_X + (TAILLE_CARRE * 1.085)
EMPLACEMENT_QUARANTAINE_Y = EMPLACEMENT_CARRE_Y



# Modes de simulation
VILLE_CENTRALE = False # Activer le mode "Ville centrale"
TAILLE_VILLE = TAILLE_CARRE // 7
EMPLACEMENT_VILLE_X = (EMPLACEMENT_CARRE_X + EMPLACEMENT_CARRE_X_CONJ - TAILLE_VILLE) // 2
EMPLACEMENT_VILLE_Y = (EMPLACEMENT_CARRE_Y + EMPLACEMENT_CARRE_Y_CONJ - TAILLE_VILLE) // 2
PROBABILITE_VOYAGE_VERS_VILLE = 0.009 # Probabilité de voyage vers la ville
                                      # Doit être très basse car les tours de boucle s'enchaînent très vite
COMMUNAUTES = False  # Activer le mode "Communautés"
TAILLE_COMMUNAUTE = TAILLE_CARRE // 3 # Donne du 3x3
PROBABILITE_VOYAGE_VERS_COMMUNAUTE = 0.0006 # Probabilité de voyage vers une autre communauté
                                           # Doit être très basse car les tours de boucle s'enchaînent très vite