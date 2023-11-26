# Classes

# Importation des modules nécessaires
import pygame  # Bibliothèque pour la création de jeux-vidéos
import random  # Module pour la génération de nombres aléatoires
import sys  # Module fournissant un accès à certaines variables utilisées ou maintenues par l'interprétateur python
import math # Calculs du cercle à partir du rayon par exemple

from constantes import * # On importe les variables de constantes.py

# Initialisation des modules Pygame manuellement
pygame.display.init()
pygame.font.init()

# Création de la fenêtre
ecran = pygame.display.set_mode((LARGEUR_ECRAN, HAUTEUR_ECRAN))
pygame.display.set_caption("Epydemie")

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
        self.est_en_quarantaine = False

        self.asymptomatique = False
        # Utiliser random.random() pour générer un nombre entre 0 et 1
        if random.random() < TAUX_ASYMPTOMATIQUES:
            self.asymptomatique = True

        self.dissident = False
        # Utiliser random.random() pour générer un nombre entre 0 et 1
        if random.random() < TAUX_DISSIDENTS:
            self.dissident = True

        self.vie = True

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
        # Utilise la méthode adaptée à la quarantaine si l'individu est en quarantaine
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
        self.couleur = (255, 0, 0) # Couleur d'un individu qui est infecté (en rouge)
        self.gueri = False

    def appliquer_distanciation(self, individus):
        # Si on est pas dissident soi-même
        if not self.dissident:

            # Pour chaque individu différent de nous-mêmes
            autres_individus = list(individus)
            autres_individus.remove(self)
            for autre in autres_individus:

                # Si l'autre n'est pas dissident non plus
                if not autre.dissident:
                    
                    # Calculer la distance entre deux individus
                    distance = ((self.x - autre.x) ** 2 + (self.y - autre.y) ** 2) ** 0.5
                    # Si la distance est en-dessous de 10 on fait des changements de direction
                    # Difficile de mettre une valeur autre que 10
                    if distance < 10:
                        angle = random.uniform(0, 2 * math.pi)
                        deplacement_x = 10 * math.cos(angle)
                        deplacement_y = 10 * math.sin(angle)
                        self.x += deplacement_x
                        self.y += deplacement_y


# Les méthodes statiques peuvent être appelées sans un objet de leur classe.

class Guerison:
    @staticmethod
    def progresser_guerison_mort(individu):
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
    def gestion_quarantaine(individu):
        if individu.est_en_quarantaine:
            if individu.gueri:
                individu.est_en_quarantaine = False
                # Réapparition aléatoire après guérison dans le grand carré noir
                individu.x = random.uniform(
                    EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU,
                    EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU,
                )
                individu.y = random.uniform(
                    EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU,
                    EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU,
                )


class Stats:
    def __init__(self):
        # Initialisation des listes pour les statistiques
        # On met la ligne des bleus de base à 160 pour que ça fasse pas vide au début
        self.historique_bleus = [160 for _ in range(LARGEUR_ECRAN)]
        self.historique_rouges = [0 for _ in range(LARGEUR_ECRAN)]
        self.historique_verts = [0 for _ in range(LARGEUR_ECRAN)]
        self.historique_morts = [0 for _ in range(LARGEUR_ECRAN)]
        # Police pour écrire
        self.font = pygame.font.Font(None, 36)

    def afficher_statistiques(self, nb_bleus, nb_rouges, nb_verts, nb_morts):
        # Afficher les statistiques en temps réel
        texte_bleus = self.font.render(f"Non exposés : {nb_bleus}", True, (0, 0, 255))
        texte_rouges = self.font.render(f"Infectés : {nb_rouges}", True, (255, 0, 0))
        texte_verts = self.font.render(f"Guéris : {nb_verts}", True, (0, 255, 0))
        texte_morts = self.font.render(f"Morts : {nb_morts}", True, (169, 169, 169))
        ecran.blit(texte_bleus, (10, 10))
        ecran.blit(texte_rouges, (10, 50))
        ecran.blit(texte_verts, (10, 90))
        ecran.blit(texte_morts, (10, 130))

    def actualiser_courbes(self, nb_bleus, nb_rouges, nb_verts, nb_morts):
        # Ajouter les valeurs actuelles à l'historique
        self.historique_bleus.append(nb_bleus)
        self.historique_rouges.append(nb_rouges)
        self.historique_verts.append(nb_verts)
        self.historique_morts.append(nb_morts)

        # Coefficienter avec 160 pour garder un affichage stable peu importe NB_INDIVIDUS
        self.historique_bleus[-1] *= (160 / NB_INDIVIDUS)
        self.historique_rouges[-1] *= (160 / NB_INDIVIDUS)
        self.historique_verts[-1] *= (160 / NB_INDIVIDUS)
        self.historique_morts[-1] *= (160 / NB_INDIVIDUS)

        # Ne garder que les données qui apparaissent sur l'écran pour éviter de surcharger
        self.historique_bleus = self.historique_bleus[-LARGEUR_ECRAN:]
        self.historique_rouges = self.historique_rouges[-LARGEUR_ECRAN:]
        self.historique_verts = self.historique_verts[-LARGEUR_ECRAN:]
        self.historique_morts = self.historique_morts[-LARGEUR_ECRAN:]

    def afficher_courbes(self):
        # Dessiner les courbes statistiques en temps réel avec des points
        for i in range(len(self.historique_bleus)):
            x = i

            y_bleus = (HAUTEUR_ECRAN - self.historique_bleus[i] - 50)
            y_rouges = (HAUTEUR_ECRAN - self.historique_rouges[i] - 50)
            y_verts = (HAUTEUR_ECRAN - self.historique_verts[i] - 50)
            y_morts = (HAUTEUR_ECRAN - self.historique_morts[i] - 50)

            pygame.draw.circle(ecran, (0, 0, 255), (x, y_bleus), 2) # Point bleu
            pygame.draw.circle(ecran, (255, 0, 0), (x, y_rouges), 2) # Point rouge
            pygame.draw.circle(ecran, (0, 255, 0), (x, y_verts), 2) # Point vert
            pygame.draw.circle(ecran, (169, 169, 169), (x, y_morts), 2) # Point gris

        # Indications pour les valeurs des courbes
        text_100p = self.font.render("100%", True, (0, 0, 0))
        text_0p = self.font.render("0%", True, (0, 0, 0))
        # On les place proportionnellement à l'écran
        ecran.blit(text_100p, (10, HAUTEUR_ECRAN - 250))
        ecran.blit(text_0p, (10, HAUTEUR_ECRAN - 35))


class Cosmos:
    def __init__(self):
        self.individus = self.initialiser_individus()

        # Liste des couples d'individus en collision
        self.collisions_en_cours = []
        # Compteur des individus morts
        self.nb_morts = 0

        self.stats = Stats()

    def initialiser_individus(self):
        # Création d'une liste d'individus pour la simulation
        individus = [
            Individu(
                random.randint(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU),
                random.randint(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU),
                TAILLE_INDIVIDU,
                (255, 0, 0),  # Couleur pour le premier individu (en rouge)
            )
        ] + [
            Individu(
                random.randint(EMPLACEMENT_CARRE_X + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_X_CONJ - TAILLE_INDIVIDU),
                random.randint(EMPLACEMENT_CARRE_Y + TAILLE_INDIVIDU, EMPLACEMENT_CARRE_Y_CONJ - TAILLE_INDIVIDU),
                TAILLE_INDIVIDU,
                (0, 0, 255),  # Couleur pour les autres individus (en bleu)
            ) for _ in range(NB_INDIVIDUS - 1)
        ]
        return individus

    def simulation(self):
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
        self.individus = [ind for ind in self.individus if ind.vie]
        # Actualiser le nombre de morts
        self.nb_morts = NB_INDIVIDUS - len(self.individus)

        # Appliquer la distanciation sociale si c'est demandé
        if RAYON_DISTANCIATION:
            for individu in self.individus:
                if not individu.est_en_quarantaine:
                    individu.appliquer_distanciation(self.individus)

        # Gérer le statut de chaque individu + déplacer et faire rebondir les individus dans le cadre
        for individu in self.individus:
            Guerison.progresser_guerison_mort(individu)
            Quarantaine.placer_en_quarantaine(individu)
            Quarantaine.gestion_quarantaine(individu)
            individu.bouger()
            individu.rebondir_sur_murs()
            individu.dessiner()


        # Vérifier les collisions en cours
        self.collisions_en_cours = [(i, j) for (i, j) in self.collisions_en_cours if i.detecter_collision(j)]

        # Tester les collisions et mettre à jour les couleurs
        ind_no_quarantaine = [ind for ind in self.individus if not ind.est_en_quarantaine]
        for i in range(len(ind_no_quarantaine)):
            for j in range(i + 1, len(ind_no_quarantaine)):
                if (
                    (ind_no_quarantaine[i], ind_no_quarantaine[j]) not in self.collisions_en_cours
                    and ind_no_quarantaine[i].detecter_collision(ind_no_quarantaine[j])
                ):
                    self.collisions_en_cours.append((ind_no_quarantaine[i], ind_no_quarantaine[j]))
                    # L'un des deux est rouge
                    if ind_no_quarantaine[i].couleur == (255, 0, 0) or ind_no_quarantaine[j].couleur == (255, 0, 0):
                        # Utiliser random.random() pour générer un nombre entre 0 et 1
                        if random.random() < TAUX_INFECTIOSITE:
                            # Si ça passe en-dessous du taux d'infectiosité on infecte
                            ind_no_quarantaine[i].infecter(), ind_no_quarantaine[j].infecter()



        # Compteurs pour les statistiques
        nb_bleus = sum(1 for ind in self.individus if ind.couleur == (0, 0, 255))
        nb_rouges = sum(1 for ind in self.individus if ind.couleur == (255, 0, 0))
        nb_verts = sum(1 for ind in self.individus if ind.couleur == (0, 255, 0))
        # nb_morts initialisé plus tôt et en attribut de la classe comme c'est linéaire

        self.stats.afficher_statistiques(nb_bleus, nb_rouges, nb_verts, self.nb_morts)
        self.stats.actualiser_courbes(nb_bleus, nb_rouges, nb_verts, self.nb_morts)
        self.stats.afficher_courbes()

        # Mettre à jour l'affichage
        pygame.display.flip()
