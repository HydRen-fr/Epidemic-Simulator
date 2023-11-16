# V4 - Sans quarantaine

import pygame
import random
import sys

# Constantes
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
COULEUR_MUR = (0, 0, 0)  # Noir
COULEUR_FOND = (255, 255, 255)  # Blanc
TAILLE_CARRE = 350
TAILLE_INDIVIDU = 4
NB_INDIVIDUS = 100
VITESSE_MAX = 0.1
TAUX_INFECTIOSITE = 0.1

# Initialisation des modules Pygame manuellement
pygame.display.init()
pygame.font.init()

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Simulation d'épidémie")

class Individu:
    def __init__(self, x, y, taille, couleur):
        self.x = x
        self.y = y
        self.taille = taille
        self.couleur = couleur
        # NB_INDIVIDUS AUGMENTE = NB OPÉS AUGMENTE = VITESSE PLUS LENTE = GUERISON PLUS LONGUE mais ça reste correct juste c'est pas beau
        # Vitesse + rapide pour un grand nombre
        self.vitesse_x = (random.uniform(-VITESSE_MAX, VITESSE_MAX) * NB_INDIVIDUS) / 10
        self.vitesse_y = (random.uniform(-VITESSE_MAX, VITESSE_MAX) * NB_INDIVIDUS) / 10
        self.temps_infecte = 0
        # Guérison + courte pour un grand nombre
        self.temps_guerison = random.randint(200000, 600000) * (1/NB_INDIVIDUS)


    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir_sur_murs(self):
        if self.x - self.taille < (LARGEUR_ECRAN - TAILLE_CARRE) // 2 or self.x + self.taille > (LARGEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 or self.y + self.taille > (HAUTEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_y = -self.vitesse_y

    def detecter_collision(self, autre_individu):
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

    def infecter(self):
        self.couleur = (255, 0, 0)  # Rouge (infecté)

    def progresser_guerison(self):
        if self.couleur == (255, 0, 0):  # Si infecté
            self.temps_infecte += 1
            if self.temps_infecte >= self.temps_guerison:
                self.couleur = (0, 255, 0)  # Vert (guéri)
                self.temps_infecte = 0


# Création d'une liste d'Individus avec un individu initial infecté
individus = [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (255, 0, 0)  # Rouge (infecté)
)] + [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (0, 0, 255)  # Bleu (non infecté)
) for _ in range(NB_INDIVIDUS - 1)]



# Liste des couples d'individus en collision
collisions_en_cours = []

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner le fond blanc
    ecran.fill(COULEUR_FOND)

    # Dessiner le carré noir
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN - TAILLE_CARRE) // 2, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Déplacer et faire rebondir les Individus
    for individu in individus:
        individu.bouger()
        individu.rebondir_sur_murs()
        individu.progresser_guerison()
        individu.dessiner()

    # Vérifier les collisions en cours
    collisions_en_cours = [(i, j) for (i, j) in collisions_en_cours if i.detecter_collision(j)]

    # Tester les collisions et mettre à jour les couleurs
    for i in range(len(individus)):
        for j in range(i + 1, len(individus)):
            if (individus[i], individus[j]) not in collisions_en_cours and individus[i].detecter_collision(individus[j]):
                collisions_en_cours.append((individus[i], individus[j]))
                # L'un des deux est rouge
                if individus[i].couleur == (255, 0, 0) or individus[j].couleur == (255, 0, 0):
                    # Utiliser random.random() pour générer un nombre entre 0 et 1
                    if random.random() < TAUX_INFECTIOSITE:
                        individus[i].couleur, individus[j].couleur = (255, 0, 0), (255, 0, 0)  # Rouges tous les deux

    # Mettre à jour l'affichage
    pygame.display.flip()
