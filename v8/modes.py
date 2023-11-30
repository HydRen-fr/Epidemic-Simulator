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
    def rebondir_sur_murs_communautes(self, cosmos):
        for communaute_x, communaute_y in cosmos.communautes:
            if communaute_x <= self.x <= communaute_x + TAILLE_COMMUNAUTE and communaute_y <= self.y <= communaute_y + TAILLE_COMMUNAUTE:
                if self.x - self.taille < communaute_x:
                    self.x = communaute_x + self.taille
                    self.vitesse_x = -self.vitesse_x
                elif self.x + self.taille > communaute_x + TAILLE_COMMUNAUTE:
                    self.x = communaute_x + TAILLE_COMMUNAUTE - self.taille
                    self.vitesse_x = -self.vitesse_x

                if self.y - self.taille < communaute_y:
                    self.y = communaute_y + self.taille
                    self.vitesse_y = -self.vitesse_y
                elif self.y + self.taille > communaute_y + TAILLE_COMMUNAUTE:
                    self.y = communaute_y + TAILLE_COMMUNAUTE - self.taille
                    self.vitesse_y = -self.vitesse_y
