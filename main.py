'''
# DOCUMENTATION DE LA V3
# Importation des modules nécessaires.
import pygame  # Bibliothèque pour la création de jeux vidéo.
import random  # Module pour la génération de nombres aléatoires.
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interpréteur Python.

# Constantes définissant les paramètres du programme.
LARGEUR_ECRAN = 800  # Largeur de la fenêtre de la simulation.
HAUTEUR_ECRAN = 600  # Hauteur de la fenêtre de la simulation.
COULEUR_MUR = (0, 0, 0)  # Couleur des murs (en noir).
COULEUR_FOND = (255, 255, 255)  # Couleur du fond de la fenêtre (en blanc).
TAILLE_CARRE = 450  # Taille du cadre où les individus évoluent.
TAILLE_INDIVIDU = 4  # Taille des individus représentés par des points.
NB_INDIVIDUS = 70  # Nombre total d'individus dans la simulation.
VITESSE_MAX = 0.4  # Vitesse maximale des individus.

# Initialisation des modules Pygame manuellement.
pygame.display.init()
pygame.font.init()

# Création de la fenêtre de simulation.
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Simulation d'épidémie")

# Définition de la classe représentant un individu dans la simulation.
class Individu:
    def __init__(self, x, y, taille, couleur):
        self.x = x
        self.y = y
        self.taille = taille
        self.couleur = couleur
        self.vitesse_x = random.uniform(-VITESSE_MAX, VITESSE_MAX)
        self.vitesse_y = random.uniform(-VITESSE_MAX, VITESSE_MAX)

    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir_sur_murs(self):
        # Vérifier si l'individu atteint les bords du cadre et les fait rebondir en conséquence.
        if self.x - self.taille < (LARGEUR_ECRAN - TAILLE_CARRE) // 2 or self.x + self.taille > (LARGEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 or self.y + self.taille > (HAUTEUR_ECRAN + TAILLE_CARRE) // 2:
            self.vitesse_y = -self.vitesse_y

    def detecter_collision(self, autre_individu):
        # Calculer la distance entre deux individus et tester s'ils entrent en collision.
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

# Création d'une liste d'individus pour la simulation.
individus = [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (255, 0, 0)  # Couleur rouge pour le premier individu.
) for _ in range(1)] + [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (0, 0, 255)  # Couleur bleu pour les autres individus.
) for _ in range(NB_INDIVIDUS - 1)]

# Boucle principale de la simulation.
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner le fond blanc.
    ecran.fill(COULEUR_FOND)

    # Dessiner le cadre noir.
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN - TAILLE_CARRE) // 2, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Déplacer et faire rebondir les individus dans le cadre.
    for individu in individus:
        individu.bouger()
        individu.rebondir_sur_murs()
        individu.dessiner()

    # Tester les collisions entre les individus et mettre à jour les couleurs en cas de collision.
    for i in range(len(individus)):
        for j in range(len(individus)):
            if i != j and individus[i].detecter_collision(individus[j]):
                individus[i].couleur, individus[j].couleur = (255, 0, 0), (255, 0, 0)  # Les individus en collision deviennent rouges.

    # Mettre à jour l'affichage de la simulation.
    pygame.display.flip()



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
'''

# V5 - Quarantaine

# Importation des modules nécessaires.
import pygame  # Bibliothèque pour la création de jeux-vidéos.
import random  # Module pour la génération de nombres aléatoires.
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interprétateur python.

# Constantes définissant les paramètres du programme.
LARGEUR_ECRAN = 800  # Largeur de la fenêtre de la simulation.
HAUTEUR_ECRAN = 600  # Hauteur de la fenêtre de la simulation.
COULEUR_MUR = (0, 0, 0)  # Couleur des bords de la fenêtre de la simulation (en noir).
COULEUR_FOND = (255, 255, 255)  # Couleur du fond de la fenêtre de la simulation (en blanc).
TAILLE_CARRE = 300  # Taille du cadre où les individus évoluent.
TAILLE_INDIVIDU = 4  # Taille des individus représentés par des points.
NB_INDIVIDUS = 20  # Nombre total d'individus dans la simulation.
VITESSE_MAX = 0.1  # Vitesse maximale des individus.
TAUX_INFECTIOSITE = 0.4  # La probabilité d'être infecté.

# Pour le carré de quarantaine
TAILLE_QUARANTAINE = 100  # Taille du cadre de la quarantaine.
# Placement des individus dans la quarantaine.
EMPLACEMENT_QUARANTAINE_X = ((LARGEUR_ECRAN - TAILLE_CARRE) // 2) + 380
EMPLACEMENT_QUARANTAINE_Y = ((HAUTEUR_ECRAN - TAILLE_CARRE) // 2)

# Initialisation des modules Pygame manuellement
pygame.display.init()
pygame.font.init()

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Simulation d'épidémie")

# Définition de la classe représentant un individu dans la simulation.
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

        self.reperage_quarantaine = random.randint(80000, 200000) * (1/NB_INDIVIDUS)
        self.temps_en_quarantaine = 0
        self.est_en_quarantaine = False


    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    def placer_en_quarantaine(self):
        if self.couleur == (255, 0, 0) and self.temps_infecte >= self.reperage_quarantaine:
            self.x = EMPLACEMENT_QUARANTAINE_X + TAILLE_QUARANTAINE / 2
            self.y = EMPLACEMENT_QUARANTAINE_Y + TAILLE_QUARANTAINE / 2
            self.est_en_quarantaine = True

    def gestion_quarantaine(self):
        if self.est_en_quarantaine:
            self.temps_en_quarantaine += 1
            if self.temps_infecte >= self.temps_guerison:
                self.est_en_quarantaine = False
                self.temps_en_quarantaine = 0
                # Réapparition aléatoire après guérison dans le grand carré noir
                self.x = random.uniform((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU)
                self.y = random.uniform((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU)

    def rebondir_sur_murs_quarantaine(self):
        # Vérifier si l'individu atteint les bords du cadre de la quarantaine et les fait rebondir en conséquence.
        if self.x - self.taille < EMPLACEMENT_QUARANTAINE_X or self.x + self.taille > EMPLACEMENT_QUARANTAINE_X + TAILLE_QUARANTAINE:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < EMPLACEMENT_QUARANTAINE_Y or self.y + self.taille > EMPLACEMENT_QUARANTAINE_Y + TAILLE_QUARANTAINE:
            self.vitesse_y = -self.vitesse_y

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir_sur_murs(self):
        # Vérifier si l'individu atteint les bords du cadre et les fait rebondir en conséquence.
        if not self.est_en_quarantaine:
            if self.x - self.taille < (LARGEUR_ECRAN - TAILLE_CARRE) // 2 or self.x + self.taille > (LARGEUR_ECRAN + TAILLE_CARRE) // 2:
                self.vitesse_x = -self.vitesse_x
            if self.y - self.taille < (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 or self.y + self.taille > (HAUTEUR_ECRAN + TAILLE_CARRE) // 2:
                self.vitesse_y = -self.vitesse_y
        else:
            self.rebondir_sur_murs_quarantaine()

    def detecter_collision(self, autre_individu):
        # Calculer la distance entre deux individus et tester s'ils entrent en collision.
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

    def infecter(self):
        self.couleur = (255, 0, 0)  # Couleur d'un individu qui est infecté (en rouge).

    def progresser_guerison(self):
        # Vérifier quand l'individu infecté pourra être guéri.
        if self.couleur == (255, 0, 0):  # Si l'individu est infecté.
            self.temps_infecte += 1
            if self.temps_infecte >= self.temps_guerison:
                self.couleur = (0, 255, 0)  # Couleur de l'individu guéri (en vert).
                self.temps_infecte = 0


# # Création d'une liste d'individus pour la simulation.
individus = [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (255, 0, 0)  # # Couleur pour le premier individu (en rouge).
)] + [Individu(
    random.randint((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    random.randint((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU),
    TAILLE_INDIVIDU,
    (0, 0, 255)  # Couleur pour les autres individus (en bleu).
) for _ in range(NB_INDIVIDUS - 1)]



# Liste des couples d'individus en collision
collisions_en_cours = []

# Boucle principale de la simulation.
while True:
    # Quitter sans problèmes en fermant la fenêtre.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner le fond blanc.
    ecran.fill(COULEUR_FOND)

    # Dessiner le cadre noir.
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN - TAILLE_CARRE) // 2, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Dessiner le cadre de la quarantaine.
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(EMPLACEMENT_QUARANTAINE_X, EMPLACEMENT_QUARANTAINE_Y, TAILLE_QUARANTAINE, TAILLE_QUARANTAINE), 2)

    # Déplacer et faire rebondir les individus dans le cadre.
    for individu in individus:
        individu.progresser_guerison()
        individu.placer_en_quarantaine()
        individu.gestion_quarantaine()
        individu.bouger()
        individu.rebondir_sur_murs()
        individu.dessiner()

    # Vérifier les collisions en cours
    collisions_en_cours = [(i, j) for (i, j) in collisions_en_cours if i.detecter_collision(j)]

    # Tester les collisions entre les individus et mettre à jour les couleurs en cas de collision.
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


# V5.5

import pygame
import random
import sys

# Constantes
LARGEUR_ECRAN = 800
HAUTEUR_ECRAN = 600
COULEUR_MUR = (0, 0, 0)  # Noir
COULEUR_FOND = (255, 255, 255)  # Blanc
TAILLE_CARRE = 290
TAILLE_INDIVIDU = 4
NB_INDIVIDUS = 25
VITESSE_MAX = 0.2
TAUX_INFECTIOSITE = 0.3

# Pour le carré de quarantaine
TAILLE_QUARANTAINE = 100
EMPLACEMENT_QUARANTAINE_X = ((LARGEUR_ECRAN - TAILLE_CARRE) // 2) + 380
EMPLACEMENT_QUARANTAINE_Y = ((HAUTEUR_ECRAN - TAILLE_CARRE) // 2)

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
        self.vitesse_x = (random.uniform(-VITESSE_MAX, VITESSE_MAX))
        self.vitesse_y = (random.uniform(-VITESSE_MAX, VITESSE_MAX))
        self.temps_infecte = 0
        # Guérison + courte pour un grand nombre
        self.temps_guerison = random.randint(20000, 60000)
        self.gueri = False

        self.reperage_quarantaine = random.randint(8000, 20000)
        self.temps_en_quarantaine = 0
        self.est_en_quarantaine = False


    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    def placer_en_quarantaine(self):
        if self.couleur == (255, 0, 0) and self.temps_infecte >= self.reperage_quarantaine and self.est_en_quarantaine == False:
            self.x = EMPLACEMENT_QUARANTAINE_X + TAILLE_QUARANTAINE / 2
            self.y = EMPLACEMENT_QUARANTAINE_Y + TAILLE_QUARANTAINE / 2
            self.est_en_quarantaine = True

    def gestion_quarantaine(self):
        if self.est_en_quarantaine:
            self.temps_en_quarantaine += 1
            if self.gueri:
                self.est_en_quarantaine = False
                self.temps_en_quarantaine = 0
                # Réapparition aléatoire après guérison dans le grand carré noir
                self.x = random.uniform((LARGEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (LARGEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU)
                self.y = random.uniform((HAUTEUR_ECRAN - TAILLE_CARRE) // 2 + TAILLE_INDIVIDU, (HAUTEUR_ECRAN + TAILLE_CARRE) // 2 - TAILLE_INDIVIDU)

    def rebondir_sur_murs_quarantaine(self):
        if self.x - self.taille < EMPLACEMENT_QUARANTAINE_X or self.x + self.taille > EMPLACEMENT_QUARANTAINE_X:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < EMPLACEMENT_QUARANTAINE_Y or self.y + self.taille > EMPLACEMENT_QUARANTAINE_Y:
            self.vitesse_y = -self.vitesse_y

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir_sur_murs(self):
        if not self.est_en_quarantaine:
            if self.x - self.taille < (LARGEUR_ECRAN - TAILLE_CARRE) // 2 or self.x + self.taille > (LARGEUR_ECRAN + TAILLE_CARRE) // 2:
                self.vitesse_x = -self.vitesse_x
            if self.y - self.taille < (HAUTEUR_ECRAN - TAILLE_CARRE) // 2 or self.y + self.taille > (HAUTEUR_ECRAN + TAILLE_CARRE) // 2:
                self.vitesse_y = -self.vitesse_y
        else:
            self.rebondir_sur_murs_quarantaine()

    def detecter_collision(self, autre_individu):
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

    def infecter(self):
        self.couleur = (255, 0, 0)  # Rouge (infecté)
        self.gueri = False

    def progresser_guerison(self):
        if self.couleur == (255, 0, 0):  # Si infecté
            self.temps_infecte += 1
            if self.temps_infecte >= self.temps_guerison:
                self.couleur = (0, 255, 0)  # Vert (guéri)
                self.temps_infecte = 0
                self.gueri = True


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
    # Quitter sans problèmes en fermant la fenêtre
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Dessiner le fond blanc
    ecran.fill(COULEUR_FOND)

    # Dessiner le carré noir
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect((LARGEUR_ECRAN - TAILLE_CARRE) // 2, (HAUTEUR_ECRAN - TAILLE_CARRE) // 2, TAILLE_CARRE, TAILLE_CARRE), 2)

    # Dessiner le carré de quarantaine
    pygame.draw.rect(ecran, COULEUR_MUR, pygame.Rect(EMPLACEMENT_QUARANTAINE_X, EMPLACEMENT_QUARANTAINE_Y, TAILLE_QUARANTAINE, TAILLE_QUARANTAINE), 2)

    # Déplacer et faire rebondir les Individus
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


