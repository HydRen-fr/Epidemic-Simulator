# Importation des modules nécessaires
import random  # Module pour la génération de nombres aléatoires

from constantes import * # On importe les variables de constantes.py

import modes

class Guerison:
    @staticmethod
    def progresser_guerison_ou_mort(individu):
        # Vérifier quand l'individu infecté pourra être guéri ou devra mourrir
        if individu.couleur == (255, 0, 0):  # Si l'individu est infecté
            individu.temps_infecte += 1 # Actualise le temps
            if individu.temps_infecte >= individu.temps_guerison: # Si il est infecté depuis suffisamment longtemps
                if random.random() < LETALITE: # Petite chance de mourir en fonction du taux de létalité
                    individu.vie = False  # L'individu décède
                else:
                    individu.couleur = (0, 255, 0)  # Couleur de l'individu guéri (en vert)
                    individu.temps_infecte = 0
                    individu.gueri = True

class Quarantaine:
    @staticmethod
    def placer_en_quarantaine(individu):
        if (
            individu.couleur == (255, 0, 0) # Rouge donc infecté
            and individu.temps_infecte >= individu.reperage_quarantaine # Temps d'être repéré atteint
            and not individu.est_en_quarantaine # Pas déjà en quarantaine
            and not individu.asymptomatique # Pas asymptomatique
        ):
            # On le place donc en quarantaine
            individu.x = EMPLACEMENT_QUARANTAINE_X + TAILLE_QUARANTAINE / 2
            individu.y = EMPLACEMENT_QUARANTAINE_Y + TAILLE_QUARANTAINE / 2
            individu.est_en_quarantaine = True

    @staticmethod
    def gestion_quarantaine(individu, cosmos):
        if individu.est_en_quarantaine:
            if individu.gueri:
                individu.est_en_quarantaine = False

                if COMMUNAUTES:
                    # Réapparition aléatoire après guérison dans une communauté
                    communaute_x, communaute_y = modes.Communautes.choisir_communaute(cosmos)
                    individu.x = random.uniform(communaute_x, communaute_x + TAILLE_COMMUNAUTE)
                    individu.y = random.uniform(communaute_y, communaute_y + TAILLE_COMMUNAUTE)
                else:
                    # Réapparition aléatoire après guérison dans le grand carré noir
                    individu.x = random.uniform(
                        EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU,
                        EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU,
                    )
                    individu.y = random.uniform(
                        EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU,
                        EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU,
                    )


    @staticmethod
    def rebondir_sur_murs_quarantaine(individu):
        if individu.x - individu.taille < EMPLACEMENT_QUARANTAINE_X or individu.x + individu.taille > EMPLACEMENT_QUARANTAINE_X + TAILLE_QUARANTAINE:
            individu.vitesse_x = -individu.vitesse_x
        if individu.y - individu.taille < EMPLACEMENT_QUARANTAINE_Y or individu.y + individu.taille > EMPLACEMENT_QUARANTAINE_Y + TAILLE_QUARANTAINE:
            individu.vitesse_y = -individu.vitesse_y