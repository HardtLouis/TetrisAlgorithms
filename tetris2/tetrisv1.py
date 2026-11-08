from tkinter import *
import random

perdu = False
score = 0
actuel = None
tickCounter = 0
nBlocs = 0
anim = 0
ltr = []

def genererGrille(largeur, hauteur):
    l = []
    for i in range(largeur):
        a = []
        for j in range(hauteur):
            a.append(0)
        l.append(a)
    return l

grille = genererGrille(10,20)


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

class tetro():
    def __init__(self, l, px, py, cId, peutTourner):
        self.groupe = l.copy()
        self.x = px
        self.y = py
        self.couleur = cId
        self.tourne = peutTourner

    def miseAJour(self, grilleJeu):
        pos = False
        for i in self.groupe:
            if i[1] + self.y == 0:
                pos = True
            if i[1] + self.y - 1 >= 0 and i[1] + self.y - 1 < len(grilleJeu[0]) and grilleJeu[i[0] + self.x][i[1] + self.y - 1] != 0:
                pos = True
        if pos:
            for i in self.groupe:
                if i[1] + self.y < len(grilleJeu[0]) and i[0] + self.x < len(grilleJeu):
                    grilleJeu[i[0] + self.x][i[1] + self.y] = self.couleur
                else:
                    return 2
            return 1
        
        self.y -= 1
        return 0

    def mouvement(self, delta, grille):
        m = True
        for i in self.groupe:
            
            if self.x + i[0] + delta < 0 or self.x + i[0] + delta >= len(grille) or self.y + i[1] < len(grille[0]) and grille[self.x + i[0] + delta][ self.y + i[1]] != 0:
                m = False
        if m:
            self.x += delta

    def rotation(self, rotationHoraire, grille):
        if rotationHoraire != 0:
            groupeC = []
            for i in self.groupe:
                if rotationHoraire == 90:
                    groupeC.append((i[1],-i[0]))
                if rotationHoraire == 270:
                    groupeC.append((-i[1],i[0]))
                if rotationHoraire == 180:
                    groupeC.append((-i[0],-i[1]))
                    
            
            peutTourner = True
            for i in groupeC:
                if self.x + i[0] < 0 or self.x + i[0] >= len(grille):
                    peutTourner = False
                elif self.y + i[1] < 0:
                    peutTourner = False
                elif self.y + i[1] < len(grille[0]) and self.x + i[0] > 0 and self.x + i[0] < len(grille) and grille[self.x + i[0]][self.y + i[1]] != 0:
                    peutTourner = False
                    
            if peutTourner:
                for i in range(len(self.groupe)):
                    if i < len(groupeC):
                        self.groupe[i] = groupeC[i]
        

leL = [(0,0), (0, -1), (-1, -1), (0, 1)]
antiL = [(0,0), (0, -1), (1, -1), (0, 1)]
leT = [(0,0), (0, 1), (1, 1), (-1, 1)]
leI = [(0, -1), (0,0), (0,1),(0, 2)]
LeZ = [(-1,0), (0,0), (0, 1), (1, 1)]
LeS = [(1,0), (0,0), (0, 1), (-1, 1)]
leBloc = [(-1,0), (0,0), (-1, 1), (0, 1)]

structuresPossibles = [leL, leT, leI, LeZ, leBloc, LeS, antiL]
Couleurs = ["red", "blue", "green", "yellow", "purple"]
prochain = None


tk = Tk()

dessin = Canvas(tk, height = 600, width = 600, bg = 'gray')
dessin.pack()

dessin.create_rectangle(0, 0, 600, 200, fill="black")
dessin.create_rectangle(0, 0, 200, 600, fill="black")
dessin.create_rectangle(400,0,600,600, fill="black")


def entrees(event):
    global actuel, grille, tickCounter
    
    if actuel != None:
        if event.keysym == "Right":
            actuel.mouvement(1, grille)
            
        if event.keysym == "Left":
            actuel.mouvement(-1, grille)
            
        if event.keysym == "Up":
            actuel.rotation(90, grille)

        if event.keysym == "Down":
            if actuel != None:
                while actuel.miseAJour(grille) == 0:
                    pass
                tickCounter = 0
            
        
tk.bind('<Key>',entrees)


def dessinGrille():
    global grille
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] != 0:
                col = Couleurs[grille[i][j] - 1]
                dessin.create_rectangle(200 + i * 20, 580 - j * 20, 220 + i * 20, 600 - j * 20, fill = col, tags = "grille")
                
dessinGrille()


####################Programmes utilisés pour gagner########################
# programme 1 (ne fonctionne que lorsque les blocs "anti-L" et "S" sont absents)

def hauteur(grille, n):
    i = len(grille[0])-1
    while i >= 0:
        if grille[n][i] != 0:
            break;
        i -= 1
    return i

def algogol(grille, actuel, structures):
    global tickCounter;
    if actuel != None:
        if actuel.groupe == structures[2]:
            if hauteur(grille, 9) > hauteur(grille, 8):
                actuel.x = 8
            else:
                actuel.x = 9

        if actuel.groupe == structures[4]:
            actuel.x = 7

        if actuel.groupe == structures[3]:
            
            actuel.rotation(90, grille)
            actuel.x = 4
            
        if actuel.groupe == structures[1]:
            if hauteur(grille, 0) > hauteur(grille, 1):
                actuel.rotation(90, grille)
                actuel.x = 0
            else:
                actuel.rotation(-90, grille)
                actuel.x = 1

        if actuel.groupe == structures[0]:
            if hauteur(grille, 3) > hauteur(grille, 2):
                actuel.rotation(180, grille)
                actuel.x = 2
            else:
                actuel.x = 3
            
### algo 2

def detecteTrous(grilleC):
    trouColonnes = 0
    for i in range(len(grilleC)):
        trouTemp = 0
        for j in range(len(grilleC[0])):
            if grilleC[i][j] == 0:
                trouTemp += 1
            else:
                trouColonnes += trouTemp
    return trouColonnes

def grilleHScore(grilleC):
    score = 0
    supprimerLigne(grilleC)
    for i in range(len(grilleC)):
        for j in range(len(grilleC[0])):
            if grilleC[i][j] != 0:
                score += j * 1
    
    return score

def copieGrille(grille):
    grilleC = []
    for i in grille:
        grilleC.append(i.copy())
    return grilleC

def essaiePos(grille, actuel):
    if actuel != None:
        
        meilleur = None
        prValides = []
        for i in range(len(grille)):
            for j in range(4):
                
                copy1 = tetro(actuel.groupe, 5, 29, 1, True)
                copy1.rotation(90 * j, grille.copy())
                copy1.x = i
                
                b = True
                for gr in copy1.groupe:
                    if i + gr[0] < 0 or i + gr[0] >= len(grille):
                        b = False
                if b:
                    prValides.append((i, j))
        
        for p in prValides:
            grilleC = copieGrille(grille)
            
            copy1 = tetro(actuel.groupe, p[0], 29, 1, True)
            copy1.rotation(90 * p[1], grilleC)

            a = 0
            while a == 0:
                a = copy1.miseAJour(grilleC)
            
            score = grilleHScore(grilleC)
            if a == 2:
                score += 1000000
                
            if meilleur == None or meilleur[0] > score:
                meilleur = (score, p[0], p[1])

        
        
        actuel.rotation(meilleur[2] * 90, grille)
        actuel.x = meilleur[1]

##Algo3

def detecteTrous(grilleC):
    trouColonnes = 0
    for i in range(len(grilleC)):
        trouTemp = 0
        for j in range(len(grilleC[0])):
            if grilleC[i][j] == 0:
                trouTemp += 1
            else:
                trouColonnes += trouTemp
    return trouColonnes

def deltaSup2(grilleC):
    
    n = 0
    
    for i in range(len(grilleC) - 1):
        h1 = hauteur(grilleC, i)
        h2 = hauteur(grilleC, i + 1)
        if abs(h1-h2) >= 2:
            n += abs(h1-h2)
    return n

def grilleHScoreAlgo3(grilleC):
    score = 0
    supprimerLigne(grilleC)
    score += detecteTrous(grilleC) * 1000
    score += deltaSup2(grilleC) * 10
    for i in range(len(grilleC)):
        for j in range(len(grilleC[0])):
            if grilleC[i][j] != 0:
                score += j * 1
    
    return score

def essaiePosProch(grille, actuel, prochain):
    if actuel != None and prochain != None and actuel.y == 28:
        
        meilleur = None
        prValidesP = []
        prValidesS = []
        for i in range(len(grille)):
            for j in range(4):
                copy1 = tetro(actuel.groupe, 5, 29, 1, True)
                copy1.rotation(90 * j, grille.copy())
                copy1.x = i
                
                b = True
                for gr in copy1.groupe:
                    if i + gr[0] < 0 or i + gr[0] >= len(grille):
                        b = False
                if b:
                    prValidesP.append((i, j))
                    
        for i in range(len(grille)):
            for j in range(4):
                copy2 = tetro(prochain.groupe, 5, 29, 1, True)
                copy2.rotation(90 * j, grille.copy())
                copy2.x = i
                
                b = True
                for gr in copy2.groupe:
                    if i + gr[0] < 0 or i + gr[0] >= len(grille):
                        b = False
                if b:
                    prValidesS.append((i, j))
        
        for p in prValidesP:
            for q in prValidesS:
                grilleC = copieGrille(grille)
                
                copy1 = tetro(actuel.groupe, p[0], 29, 1, True)
                copy1.rotation(90 * p[1], grilleC)

                copy2 = tetro(prochain.groupe, q[0], 29, 1, True)
                copy2.rotation(90 * q[1], grilleC)

                a = 0
                while a == 0:
                    a = copy1.miseAJour(grilleC)
                if a != 2:
                    a = 0
                    
                while a == 0:
                    a = copy2.miseAJour(grilleC)
                
                score = grilleHScoreAlgo3(grilleC)
                if a == 2:
                    score += 1000000
                    
                if meilleur == None or meilleur[0] > score:
                    meilleur = (score, p[0], p[1])

        
        
        actuel.rotation(meilleur[2] * 90, grille)
        actuel.x = meilleur[1]
                    
##########################################"
                    
                    
                

def miseAJour():
    global grille, dessin, structuresPossibles, perdu, score, prochain, actuel, tickCounter, nBlocs, ltr, anim
    
    dessin.delete("grille")
    l = supprimerLigne(grille)
    TBT = max(3, 50 - nBlocs * 3)
    if len(l) != 0:
        ltr += l
        anim = 5
        score += len(l) * 10
            
    if tickCounter == 0:
        
        
        if actuel == None:
            if prochain == None:
                struct = random.choice(structuresPossibles)
                prochain = tetro(struct, 5, 29, 1 + random.randint(0, 4), True)

                struct2 = random.choice(structuresPossibles)
                prochain = tetro(struct2, 5, 29, 1 + random.randint(0, 4), True)
            else:
                actuel = prochain
                struct = random.choice(structuresPossibles)

                while actuel.groupe == struct:
                    struct = random.choice(structuresPossibles)
                
                prochain = tetro(struct, 5, 29, 1 + random.randint(0, 4), True)
                    
                
            nBlocs += 1

        if actuel != None:
            i = actuel.miseAJour(grille)
            if i == 2:
                print(score)
                grille = genererGrille(10,20)
                actuel = None
                prochain = None
                perdu = False
                score = 0
                nBlocs = 0
                
            elif i == 1:
                actuel = None

        essaiePosProch(grille, actuel, prochain)
        tickCounter = TBT
    else:
        tickCounter -= 1
    
    
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
    

    if anim != 0:
        anim -= 1
        for i in ltr:
            dessin.create_rectangle(200, 580-i*20, 400, 600-i*20, fill = "white", tags = "grille")
        if anim == 0:
            ltr.clear()

            
    dessin.after(16, miseAJour)    


dessin.after(16, miseAJour)



tk.mainloop()
