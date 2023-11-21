# V7 - Mort des individus et statistiques en temps réel

# Importation des modules nécessaires
import pygame  # Bibliothèque pour la création de jeux-vidéos
import random  # Module pour la génération de nombres aléatoires
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interprétateur python
import math # Calculs du cercle à partir du rayon par exemple



# Constantes définissant les paramètres du programme

LARGEUR_ECRAN = 1600  # Largeur de la fenêtre de la simulation
HAUTEUR_ECRAN = 1000  # Hauteur de la fenêtre de la simulation
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




# Initialisation des modules Pygame manuellement
pygame.display.init()
pygame.font.init()


# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Epydemie")



# Définition de la classe représentant un individu dans la simulation
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

        self.asymptomatique = False
        # Utiliser random.random() pour générer un nombre entre 0 et 1
        if random.random() < TAUX_ASYMPTOMATIQUES:
            self.asymptomatique = True

        self.vie = True

    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

    def placer_en_quarantaine(self):
        if self.couleur == (255, 0, 0) and self.temps_infecte >= self.reperage_quarantaine \
            and self.est_en_quarantaine == False and self.asymptomatique == False:
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
                self.x = random.uniform(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU)
                self.y = random.uniform(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU)

    def bouger(self):
        self.x += self.vitesse_x
        self.y += self.vitesse_y

    def rebondir_sur_murs(self):
        # Vérifier si l'individu atteint les bords du cadre et les fait rebondir en conséquence
        if not self.est_en_quarantaine:
            if self.x - self.taille < EMPLACEMENT_CARRE_X:
                self.x = EMPLACEMENT_CARRE_X + self.taille
                self.vitesse_x = -self.vitesse_x
            elif self.x + self.taille > EMPLACEMENT_CARRE_X_CONJ:
                self.x = EMPLACEMENT_CARRE_X_CONJ - self.taille
                self.vitesse_x = -self.vitesse_x

            if self.y - self.taille < EMPLACEMENT_CARRE_Y:
                self.y = EMPLACEMENT_CARRE_Y + self.taille
                self.vitesse_y = -self.vitesse_y
            elif self.y + self.taille > EMPLACEMENT_CARRE_Y_CONJ:
                self.y = EMPLACEMENT_CARRE_Y_CONJ - self.taille
                self.vitesse_y = -self.vitesse_y
        else:
            self.rebondir_sur_murs_quarantaine()

    def rebondir_sur_murs_quarantaine(self):
        # Vérifier si l'individu atteint les bords du cadre de la quarantaine et les fait rebondir en conséquence
        if self.x - self.taille < EMPLACEMENT_QUARANTAINE_X or self.x + self.taille > EMPLACEMENT_QUARANTAINE_X + TAILLE_QUARANTAINE:
            self.vitesse_x = -self.vitesse_x
        if self.y - self.taille < EMPLACEMENT_QUARANTAINE_Y or self.y + self.taille > EMPLACEMENT_QUARANTAINE_Y + TAILLE_QUARANTAINE:
            self.vitesse_y = -self.vitesse_y

    def detecter_collision(self, autre_individu):
        # Calculer la distance entre deux individus et tester s'ils entrent en collision
        distance = ((self.x - autre_individu.x) ** 2 + (self.y - autre_individu.y) ** 2) ** 0.5
        return distance <= self.taille + autre_individu.taille

    def infecter(self):
        self.couleur = (255, 0, 0)  # Couleur d'un individu qui est infecté (en rouge)
        self.gueri = False

    def progresser_guerison(self):
        global nb_morts
        # Vérifier quand l'individu infecté pourra être guéri
        if self.couleur == (255, 0, 0):  # Si l'individu est infecté
            self.temps_infecte += 1
            if self.temps_infecte >= self.temps_guerison:
                # Utiliser random.random() pour générer un nombre entre 0 et 1
                if random.random() < LETALITE:
                    self.vie = False  # L'individu décède
                    nb_morts += 1
                else:
                    self.couleur = (0, 255, 0)  # Couleur de l'individu guéri (en vert)
                    self.temps_infecte = 0
                    self.gueri = True
    
    def appliquer_distanciation(self, autres_individus):
        for autre in autres_individus:
            if autre != self:
                distance = ((self.x - autre.x) ** 2 + (self.y - autre.y) ** 2) ** 0.5
                if distance < 10:
                    angle = random.uniform(0, 2 * math.pi)
                    deplacement_x = 10 * math.cos(angle)
                    deplacement_y = 10 * math.sin(angle)
                    self.x += deplacement_x
                    self.y += deplacement_y




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




# Liste des couples d'individus en collision
collisions_en_cours = []

# Compteur des individus morts
nb_morts = 0

# Initialisation des listes pour les statistiques
# On met la ligne des bleus de base à 160 pour que ça fasse pas vide au début
historique_bleus = [160 for i in range(LARGEUR_ECRAN)]
historique_rouges = [0 for i in range(LARGEUR_ECRAN)]
historique_verts = [0 for i in range(LARGEUR_ECRAN)]
historique_morts = [0 for i in range(LARGEUR_ECRAN)]


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





    # Compteurs pour les statistiques
    nb_bleus = sum(1 for ind in individus if ind.couleur == (0, 0, 255))
    nb_rouges = sum(1 for ind in individus if ind.couleur == (255, 0, 0))
    nb_verts = sum(1 for ind in individus if ind.couleur == (0, 255, 0))
    # nb_morts initialisé plus tôt comme c'est linéaire



    # Afficher les statistiques en temps réel
    font = pygame.font.Font(None, 36)
    text_bleus = font.render(f"Non exposés : {nb_bleus}", True, (0, 0, 255))
    text_rouges = font.render(f"Infectés : {nb_rouges}", True, (255, 0, 0))
    text_verts = font.render(f"Guéris : {nb_verts}", True, (0, 255, 0))
    text_morts = font.render(f"Morts : {nb_morts}", True, (169, 169, 169))
    ecran.blit(text_bleus, (10, 10))
    ecran.blit(text_rouges, (10, 50))
    ecran.blit(text_verts, (10, 90))
    ecran.blit(text_morts, (10, 130))



    # Ajouter les valeurs actuelles à l'historique
    historique_bleus.append(nb_bleus)
    historique_rouges.append(nb_rouges)
    historique_verts.append(nb_verts)
    historique_morts.append(nb_morts)

    # Coefficienter avec 160 pour garder un affichage stable peu importe NB_INDIVIDUS
    historique_bleus[-1] *= (160 / NB_INDIVIDUS)
    historique_rouges[-1] *= (160 / NB_INDIVIDUS)
    historique_verts[-1] *= (160 / NB_INDIVIDUS)
    historique_morts[-1] *= (160 / NB_INDIVIDUS)

    historique_bleus = historique_bleus[-LARGEUR_ECRAN:]
    historique_rouges = historique_rouges[-LARGEUR_ECRAN:]
    historique_verts = historique_verts[-LARGEUR_ECRAN:]
    historique_morts = historique_morts[-LARGEUR_ECRAN:]

    # Dessiner les courbes statistiques en temps réel avec des points
    for i in range(len(historique_bleus)):
        x = i

        y_bleus = (HAUTEUR_ECRAN - historique_bleus[i] - 50)
        y_rouges = (HAUTEUR_ECRAN - historique_rouges[i] - 50)
        y_verts = (HAUTEUR_ECRAN - historique_verts[i] - 50)
        y_morts = (HAUTEUR_ECRAN - historique_morts[i] - 50)

        pygame.draw.circle(ecran, (0, 0, 255), (x, y_bleus), 2)  # Point bleu
        pygame.draw.circle(ecran, (255, 0, 0), (x, y_rouges), 2)  # Point rouge
        pygame.draw.circle(ecran, (0, 255, 0), (x, y_verts), 2)   # Point vert
        pygame.draw.circle(ecran, (169, 169, 169), (x, y_morts), 2)  # Point gris

    # Indications pour les valeurs des courbes
    text_100p = font.render("100%", True, (0, 0, 0))
    text_0p = font.render("0%", True, (0, 0, 0))
    ecran.blit(text_100p, (10, HAUTEUR_ECRAN - 250))
    ecran.blit(text_0p, (10, HAUTEUR_ECRAN - 35))



    # Mettre à jour l'affichage
    pygame.display.flip()
