

class algorithme:

    def __init__(self, structPoss):
        self.structuresPossibles = structPoss
    
    def miseAJour(self, grille, actuel, prochain):
        pass

    ##Fonctionnement des simulations
    def copieGrille(self, grille):
        grilleC = []
        for i in grille:
            grilleC.append(i.copy())
        return grilleC


    ##Recuperation d'informations non essentielles
    def nRot(self, tetro):
        if tetro.groupe in self.structuresPossibles:
            ind = self.structuresPossibles.index(tetro.groupe)
            if ind == 2 or ind == 3 or ind == 5:
                return 2
            elif ind == 4:
                return 1
        return 4

    ##Fonctions necessaires aux notations
    def hauteur(self, grille, n):
        i = len(grille[0])-1
        while i >= 0:
            if grille[n][i] != 0:
                break;
            i -= 1
        return i+1

    def detecteTrous(self, grilleC):
        trouColonnes = 0
        l = []
        for i in range(len(grilleC)):
            trouTemp = 0
            for j in range(len(grilleC[0])):
                if grilleC[i][j] == 0:
                    trouTemp += 1
                else:
                    trouColonnes += trouTemp
        return trouColonnes

    def detecteLigneAvecTrous(self, grilleC):
        vides = []
        for i in range(len(grilleC)):
            for j in range(self.hauteur(grilleC, i)):
                if grilleC[i][j] == 0 and not j in vides:
                    vides.append(j)
        return vides
    

    def supprimerLigne(self, grille):
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


    ##Fonction de notation
    def grilleHScore(self, grilleC):
        
        score = 0
        self.supprimerLigne(grilleC)
        hMin = 20
        hMax = 0
        vides = []
        for i in range(len(grilleC)):
            haut = self.hauteur(grilleC, i)
            if hMax < haut:
                hMax = haut
            if hMin > haut:
                hMin = haut
            for j in range(haut):
                if grilleC[i][j] != 0:
                    score += j+1
                if grilleC[i][j] == 0 and not j in vides:
                    vides.append(j)
        score += len(vides) * 3
        score += max(0, ((hMax - hMin) - 6) * 4)
        return score

    def grilleHScoreTrous(self, grilleC):
        
        score = 0
        self.supprimerLigne(grilleC)
        hMin = 20
        hMax = 0
        vides = []
        for i in range(len(grilleC)):
            haut = self.hauteur(grilleC, i)
            if hMax < haut:
                hMax = haut
            if hMin > haut:
                hMin = haut
            for j in range(haut):
                if grilleC[i][j] != 0:
                    score += j+1
                if grilleC[i][j] == 0 and not j in vides:
                    vides.append(j)
        score += hMax * 10
        score += len(vides) * 3
        score += max(0, ((hMax - hMin) - 6) * 4)
        return score
        
    def grilleDScore(self, grilleC):
        score = 0
        self.supprimerLigne(grilleC)
        hMin = 20
        hMax = 0
        maxDelta = 0
        vides = []
        for i in range(len(grilleC)):
            haut = self.hauteur(grilleC, i)
            if i < len(grilleC) - 1:
                maxDelta = max(maxDelta, abs(haut - self.hauteur(grilleC, i+1)))
            if hMax < haut:
                hMax = haut
            if hMin > haut:
                hMin = haut
            for j in range(haut):
                if grilleC[i][j] != 0:
                    score += j+1
                if grilleC[i][j] == 0 and not j in vides:
                    o = 0
                    while j + 1 + o < haut and grilleC[i][j+1+o] != 0:
                        o+=1
                    vides.append((i,j, o))
        for j in vides:
            score += j[1] * 7 + j[2] * 5
        score += max(0, (maxDelta-2) * 3)
        return score

    def grilleHScoreGen(self, grilleC, scoretrou, hdelta, scoredelta):
        
        score = 0
        self.supprimerLigne(grilleC)
        hMin = 20
        hMax = 0
        vides = []
        for i in range(len(grilleC)):
            haut = self.hauteur(grilleC, i)
            if hMax < haut:
                hMax = haut
            if hMin > haut:
                hMin = haut
            for j in range(haut):
                if grilleC[i][j] != 0:
                    score += j+1
                if grilleC[i][j] == 0 and not j in vides:
                    vides.append(j)
        score += len(vides) * scoretrou
        score += max(0, ((hMax - hMin) - hdelta) * scoredelta)
        return score
