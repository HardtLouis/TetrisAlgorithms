from tkinter import *
from objet.tetro import *
from objet.algorithmes import *

import random
import time


perdu = False
score = 0
##Variable servant aux animations
tickCounter = 0
##Nombre de tetrominaux tombés
nBlocs = 0
##lorsque non nulle affiche une bande blanche selon ltr[]
anim = 0
##liste de lignes à afficher en blanc si ltr non nulle
ltr = []

temps = time.time()

##Génere une grille vide de dimensions données
def genererGrille(largeur, hauteur):
    l = []
    for i in range(largeur):
        a = []
        for j in range(hauteur):
            a.append(0)
        l.append(a)
    return l


grille = genererGrille(10,20)


##Supprime les lignes pleines d'une grille de tetris et descend les blocs au dessus des lignes supprimées
def supprimerLigne(grille):
    l = []
    for j in range(len(grille[0])):
        s = 0
        for i in range(len(grille)):
            if grille[i][j] != 0:
                s += 1
        if s == len(grille):
            l.append(j)
            for z in range(j, len(grille[0])):
                for i in range(len(grille)):
                    if z < len(grille[0]) - 1:
                        grille[i][z] = grille[i][z+1]
                    else:
                        grille[i][z] = 0
    return l

##Structures de base du tetris
leL = [(0,0), (0, -1), (-1, -1), (0, 1)]
antiL = [(0,0), (0, -1), (1, -1), (0, 1)]
leT = [(0,0), (0, 1), (1, 0), (-1, 0)]
leI = [(0, -1), (0,0), (0,1),(0, 2)]
LeZ = [(-1,0), (0,0), (0, 1), (1, 1)]
LeS = [(1,0), (0,0), (0, 1), (-1, 1)]
leBloc = [(-1,0), (0,0), (-1, 1), (0, 1)]

##Structure non présente utilisées pour des tests
leGrosBloc = [(-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1), (1, -1), (0, -1), (-1, -1)]

##Liste des structures (utilisé par des algorithmes et le jeu
structuresPossibles = [leL, leT, leI, LeZ, leBloc, LeS, antiL]
##couleurs possibles des blocs
Couleurs = ["red", "blue", "green", "yellow", "purple", "white", "pink", "brown", "orange"]
##Bloc en train de tomber
actuel = None
##Prochain bloc qui sera placé
prochain = None

##Algorithme utilisé (à changer selon l'algorithme qui nous intéresse)
algo = Algoback(structuresPossibles)

tk = Tk()

dessin = Canvas(tk, height = 600, width = 600, bg = 'gray')
dessin.pack()

dessin.create_rectangle(0, 0, 600, 200, fill="black")
dessin.create_rectangle(0, 0, 200, 600, fill="black")
dessin.create_rectangle(400,0,600,600, fill="black")

##Controles si l'on veut jouer nous même
def entrees(event):
    global actuel, grille, tickCounter, perdu
    
    if actuel != None:
        if event.keysym == "Right":
            actuel.mouvement(1, grille)
            
        if event.keysym == "Left":
            actuel.mouvement(-1, grille)
            
        if event.keysym == "Up":
            actuel.rotation(90, grille)

        if event.keysym == "Down":
            actuel.rotation(270, grille)
            
        if event.keysym == "Return":
            a = 0
            while a == 0:
                a = actuel.miseAJour(grille)
            if a == 2:
                perdu = True
            actuel = None
            
##Associe à l'interface la fonction des contrôles        
tk.bind('<Key>',entrees)

##Affiche la grille
def dessinGrille():
    global grille
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] != 0:
                col = Couleurs[grille[i][j] - 1]
                dessin.create_rectangle(200 + i * 20, 580 - j * 20, 220 + i * 20, 600 - j * 20, fill = col, tags = "grille")
                
dessinGrille()

def maxRecup(l):
    m = l[0]
    for i in range(1, len(l)):
        if m[0] < l[i][0]:
            m = l[i]
    return m

##SimulationVisuelle sert à lancer une simulation où l'interface reste, la chute des tetrominaux est instantannée

def simulationVisuelle():
    global grille, dessin, structuresPossibles, perdu, score, prochain, actuel, tickCounter, nBlocs, ltr, anim, temps
    
    dessin.delete("grille")
        
        
    if prochain == None:
        struct = random.choice(structuresPossibles)
        actuel = tetro(struct, 5, 29, 1 + random.randint(0, 8))

        struct2 = random.choice(structuresPossibles)
        prochain = tetro(struct2, 5, 29, 1 + random.randint(0, 8))
    else:
        actuel = prochain
        struct = random.choice(structuresPossibles)

        while actuel.groupe == struct:
            struct = random.choice(structuresPossibles)
                
        prochain = tetro(struct, 5, 29, 1 + random.randint(0, 8))
                    
                
    nBlocs += 1

    if actuel != None:
        
        
        i = 0
        while i == 0:
            i = actuel.miseAJour(grille)
            algo.miseAJour(grille, actuel, prochain)
            
        if i == 2 or perdu:
            print(score)
            grille = genererGrille(10,20)
            actuel = None
            prochain = None
            perdu = False
            score = 0
            nBlocs = 0
            print(round(time.time() - temps))
            print("PERDU")
                
        elif i == 1:
            actuel = None
    
    
    l = supprimerLigne(grille)
    score += len(l) * 10
                
    dessinGrille()
    dessin.create_text(300, 20, text="score:" + str(score), fill = "white", tags = "grille", font="Times 30 bold")
            
    dessin.after(1, simulationVisuelle)

##Utilisé pour faire fonctionner le jeu
def miseAJour():
    global grille, dessin, structuresPossibles, perdu, score, prochain, actuel, tickCounter, nBlocs, ltr, anim, temps


    
    dessin.delete("grille")
    TBT = round(max(0, 10 - nBlocs / 15))
            
    if tickCounter == 0:
        
        
        if actuel == None:
            if prochain == None:
                struct = random.choice(structuresPossibles)
                prochain = tetro(struct, 5, 29, 1 + random.randint(0, 8))

                struct2 = random.choice(structuresPossibles)
                prochain = tetro(struct2, 5, 29, 1 + random.randint(0, 8))
            else:
                actuel = prochain
                struct = random.choice(structuresPossibles)

                while actuel.groupe == struct:
                    struct = random.choice(structuresPossibles)
                
                prochain = tetro(struct, 5, 29, 1 + random.randint(0, 8))
                    
                
            nBlocs += 1

        algo.miseAJour(grille, actuel, prochain)

        if actuel != None:
            i = actuel.miseAJour(grille)
            if i == 2 or perdu:
                print(score)
                grille = genererGrille(10,20)
                actuel = None
                prochain = None
                perdu = False
                score = 0
                nBlocs = 0
                print(round(time.time() - temps))
                print("PERDU")
                
            elif i == 1:
                actuel = None

        tickCounter = TBT
    else:
        tickCounter -= 1
    
    
    f = 0
    if TBT != 0:
        f = (1-tickCounter) / TBT
    
    if actuel != None:
        for i in actuel.groupe:
            col = Couleurs[actuel.couleur - 1]
            dessin.create_rectangle(200 + (i[0] + actuel.x) * 20, 580 - (i[1] + actuel.y - f) * 20, 220 + (i[0] + actuel.x) * 20, 600 - (i[1] + actuel.y - f) * 20, fill = col, tags = "grille")
                
    if prochain != None:
        for i in prochain.groupe:
            col = Couleurs[prochain.couleur - 1]
            dessin.create_rectangle(30 + (i[0]) * 20, 280 - (i[1]) * 20, 50 + (i[0]) * 20, 300 - (i[1]) * 20, fill = col, tags = "grille")
    dessinGrille()
    dessin.create_text(300, 20, text="score:" + str(score), fill = "white", tags = "grille", font="Times 30 bold")
    
    
    l = supprimerLigne(grille)

    if len(l) != 0:
        ltr += l
        anim = 5
        score += len(l) * 10
    
    if anim != 0:
        anim -= 1
        for i in ltr:
            dessin.create_rectangle(200, 580-i*20, 400, 600-i*20, fill = "white", tags = "grille")
        if anim == 0:
            ltr.clear()

            
    dessin.after(1, miseAJour)    


dessin.after(1, miseAJour)
        

tk.mainloop()
