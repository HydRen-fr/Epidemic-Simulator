# Importation des modules nécessaires
import random  # Module pour la génération de nombres aléatoires

from constantes import * # On importe les variables de constantes.py

class Ville_Centrale:
    @staticmethod
    def voyager(individu):
        # Choisir une nouvelle position aléatoire dans la ville centrale
        individu.x = random.uniform(EMPLACEMENT_VILLE_X, EMPLACEMENT_VILLE_X + TAILLE_VILLE)
        individu.y = random.uniform(EMPLACEMENT_VILLE_Y, EMPLACEMENT_VILLE_Y + TAILLE_VILLE)


class Communautes:
    @staticmethod
    def initialiser_communautes(cosmos):
        return [(EMPLACEMENT_CARRE_X + x * TAILLE_COMMUNAUTE,
                 EMPLACEMENT_CARRE_Y + y * TAILLE_COMMUNAUTE) 
                for x in range(cosmos.nb_communautes_x) for y in range(cosmos.nb_communautes_y)]

    @staticmethod
    def choisir_communaute(cosmos):
        return random.choice(cosmos.communautes)

    @staticmethod
    def changer_de_communaute(individu, cosmos):
        communaute_x, communaute_y = Communautes.choisir_communaute(cosmos)
        individu.x = random.uniform(communaute_x + individu.taille, communaute_x + TAILLE_COMMUNAUTE - individu.taille)
        individu.y = random.uniform(communaute_y + individu.taille, communaute_y + TAILLE_COMMUNAUTE - individu.taille)

    @staticmethod
    def rebondir_sur_murs_communautes(individu, cosmos):
        for communaute_x, communaute_y in cosmos.communautes:
            if communaute_x <= individu.x <= communaute_x + TAILLE_COMMUNAUTE and communaute_y <= individu.y <= communaute_y + TAILLE_COMMUNAUTE:
                if individu.x - individu.taille < communaute_x:
                    individu.x = communaute_x + individu.taille
                    individu.vitesse_x = -individu.vitesse_x
                elif individu.x + individu.taille > communaute_x + TAILLE_COMMUNAUTE:
                    individu.x = communaute_x + TAILLE_COMMUNAUTE - individu.taille
                    individu.vitesse_x = -individu.vitesse_x

                if individu.y - individu.taille < communaute_y:
                    individu.y = communaute_y + individu.taille
                    individu.vitesse_y = -individu.vitesse_y
                elif individu.y + individu.taille > communaute_y + TAILLE_COMMUNAUTE:
                    individu.y = communaute_y + TAILLE_COMMUNAUTE - individu.taille
                    individu.vitesse_y = -individu.vitesse_y
