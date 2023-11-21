from constantes import *

class Cosmos:
    def __init__(self):
        # Liste des couples d'individus en collision
        self.collisions_en_cours = []
        
    def dessiner(self):
        pygame.draw.circle(ecran, self.couleur, (int(self.x), int(self.y)), self.taille)

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
    
    
class Virus:
    def infecter(self):
        self.couleur = (255, 0, 0)  # Couleur d'un individu qui est infecté (en rouge)
        self.gueri = False
    
    
# MESURES PREVENTIVES
class Guerison:
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
    
class Quarantaine:
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

class Distanciation:
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



class Stats:
    # Compteur des individus morts
    nb_morts = 0
    
    # Initialisation des listes pour les statistiques
    # On met la ligne des bleus de base à 160 pour que ça fasse pas vide au début
    historique_bleus = [160 for i in range(LARGEUR_ECRAN)]
    historique_rouges = [0 for i in range(LARGEUR_ECRAN)]
    historique_verts = [0 for i in range(LARGEUR_ECRAN)]
    historique_morts = [0 for i in range(LARGEUR_ECRAN)]
    
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
    
    

    
    