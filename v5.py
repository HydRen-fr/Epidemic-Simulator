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
        self.gueri = False

        self.reperage_quarantaine = random.randint(80000, 200000) * (1/NB_INDIVIDUS)
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
        self.gueri = False

    def progresser_guerison(self):
        # Vérifier quand l'individu infecté pourra être guéri.
        if self.couleur == (255, 0, 0):  # Si l'individu est infecté.
            self.temps_infecte += 1
            if self.temps_infecte >= self.temps_guerison:
                self.couleur = (0, 255, 0)  # Couleur de l'individu guéri (en vert).
                self.temps_infecte = 0
                self.gueri = True


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
