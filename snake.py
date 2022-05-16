from upemtk import *
from time import sleep
from random import randint

# dimensions du jeu
taille_case = 15
largeur_plateau = 40  # en nombre de cases
hauteur_plateau = 30  # en nombre de cases

def deplacement(pos_serp,direction):
    """ 
    fonction recevant les coordonnées de chaque partie du corps du 
    serpent, ainsi que la direction qu'aura saisi le joueur a l'aide 
    des touches et renvoyant les nouvelles coordonnées des parties du 
    corps du serpent
    """
    x,y=pos_serp[0]
    u,v=change_direction(direction,touche)
    pos_serp = (x + u, y + v)
    return pos_serp
    
def case_vers_pixel(case):
    """
	Fonction recevant les coordonnées d'une case du plateau sous la 
	forme d'un couple d'entiers (ligne, colonne) et renvoyant les 
	coordonnées du pixel se trouvant au centre de cette case. Ce calcul 
	prend en compte la taille de chaque case, donnée par la variable 
	globale taille_case.
    """
    i, j = case
    return (i + .5) * taille_case, (j + .5) * taille_case


def affiche_pommes(pomme):
    """
    fonction recevant les coordonnées de la future position
    de la pomme et renvoyant un dessin de celle-ci à la position 
    établie 
    """
    
    x, y = case_vers_pixel(pos_pomme)  # conversion des coordonées en pixel

    cercle(x, y, taille_case/2,
           couleur='darkred', remplissage='red')
    rectangle(x-2, y-taille_case*.4, x+2, y-taille_case*.7,
              couleur='darkgreen', remplissage='darkgreen')


def affiche_serpent(pos_serp):
    i=0
    
    while i<len(pos_serp):
        x, y = case_vers_pixel(pos_serp[i])  # conversion des coordonées en pixel
        
        cercle(x, y, taille_case/2 + 1,
           couleur='darkgreen', remplissage='green')
           
        i+=1
    
def change_direction(direction, touche):
    if touche == 'Up':
        # flèche haut pressée
        return (0,-1)
    elif touche == 'Down':
        return (0,1)
    elif touche == 'Right':
        return (1,0)
    elif touche == 'Left':
        return (-1,0)
    else:
        # pas de changement !
        return direction

def ready():
    texte(t/2,t/2,"Tapez sur une touche !",c0,"center")
    attend_ev()
    efface_tout()

# programme principal
if __name__ == "__main__":

    # initialisation du jeu
    framerate = 10    # taux de rafraîchissement du jeu en images/s
    direction = (0, 0)# direction initiale du serpent
    pos_serp=[(20,15)]
    pos_pomme=(-1,-1)
    colision_pomme_serpent=True
    cree_fenetre(taille_case * largeur_plateau,
                 taille_case * hauteur_plateau)
    texte(largeur_plateau/2,hauteur_plateau/2,"Bonne chance!",couleur="Black")

    # boucle principale
    while True:
        # affichage des objets
        efface_tout()
            
        if pos_pomme==pos_serp[0]:
            colision_pomme_serpent=True
            pos_serp.insert(1,pos_pomme)
            
        if colision_pomme_serpent==True:
            x=randint(0,largeur_plateau-1)
            y=randint(0,hauteur_plateau-1)
            pos_pomme=(x,y)
            colision_pomme_serpent=False
            
        affiche_pommes(pos_pomme)
        
        pos_serp.insert(0,deplacement(pos_serp,direction))
        pos_serp.pop()
        
        x,y=pos_serp[0]
        colision=pos_serp.count(pos_serp[0])
        if x==-1 or x==largeur_plateau or y==-1 or y==hauteur_plateau or colision!=1 :
            score=len(pos_serp)-1
            print(score,"pommes mangées")
            break
            
        affiche_serpent(pos_serp)# affiche toutes les positions de chaque partie du corps du serpent !
        
        mise_a_jour()

        # gestion des événements
        ev = donne_ev()
        ty = type_ev(ev)
        if ty == 'Quitte':
            break
        elif ty == 'Touche':
            direction = change_direction(direction, touche(ev))

        # attente avant rafraîchissement
        sleep(1/framerate)

    # fermeture et sortie
    ferme_fenetre()
