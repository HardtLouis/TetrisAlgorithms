from objet.algorithme_base import *
from objet.tetro import *

# programme 1 (ne fonctionne que lorsque les blocs "anti-L" et "S" sont absents)
class algogol(algorithme):
    
    def miseAJour(self, grille, actuel, prochain):
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

# Programme 2 (le plus rapide marchant avec les notations)
class essaiePos(algorithme):
    def miseAJour(self, grille, actuel, prochain):
        if actuel != None and actuel.y == 28:
        
            meilleur = None
            prValides = []
            for i in range(len(grille)):
                for j in range(self.nRot(actuel)):
                    
                    copy1 = tetro(actuel.groupe, 5, 29, 1)
                    copy1.rotation(90 * j, grille.copy())
                    copy1.x = i
                    
                    b = True
                    for gr in copy1.groupe:
                        if i + gr[0] < 0 or i + gr[0] >= len(grille):
                            b = False
                    if b:
                        prValides.append((i, j))
            
            for p in prValides:
                grilleC = self.copieGrille(grille)
                
                copy1 = tetro(actuel.groupe, p[0], 29, 1)
                copy1.rotation(90 * p[1], grilleC)

                a = 0
                while a == 0:
                    a = copy1.miseAJour(grilleC)
                
                score = self.grilleHScoreTrous(grilleC)
                if a == 2:
                    score += 1000000
                    
                if meilleur == None or meilleur[0] > score:
                    meilleur = (score, p[0], p[1], grilleC)

            
            
            actuel.rotation(meilleur[2] * 90, grille)
            actuel.x = meilleur[1]
            return (meilleur[0], grilleC)

class essaiePosProch(algorithme):
    def miseAJour(self, grille, actuel, prochain):
        if actuel != None and prochain != None and actuel.y == 28:
            
            meilleur = None
            prValidesP = []
            prValidesS = []

            rot1 = self.nRot(actuel)
            rot2 = self.nRot(prochain)
            
            for p in range(len(grille)):
                for kk in range(len(grille)):
                    q = len(grille) - 1 - kk
                    for i in range(rot1):
                        for j in range(rot2):
                            grilleC = self.copieGrille(grille)
                            
                            copy1 = tetro(actuel.groupe, 5, 29, 1)
                            copy1.rotation(90 * i, grilleC)
                            copy1.mouvement(q-copy1.x, grilleC)

                            copy2 = tetro(prochain.groupe, 5, 29, 1)
                            copy2.rotation(90 * j, grilleC)
                            copy2.mouvement(p-copy2.x, grilleC)
                            
                            a = 0
                            while a == 0:
                                a = copy1.miseAJour(grilleC)
                            
                            b = 0
                                
                            while b == 0:
                                b = copy2.miseAJour(grilleC)
                            
                            score = self.grilleHScore(grilleC)
                            
                            if a == 2 or b == 2:
                                score += 1000000000
                                
                            if meilleur == None or meilleur[0] > score:
                                meilleur = (score, copy1.x, i)
                                    

            
            
            actuel.rotation(meilleur[2] * 90, grille)
            actuel.x = meilleur[1]
            print(meilleur)
            
            return meilleur[0]

class essaiePosProchOpti(algorithme):
    def miseAJour(self, grille, actuel, prochain):
        if actuel != None and prochain != None and actuel.y == 25:
        
            meilleur = None
            prValidesP = []
            prValidesS = []
            rot1 = self.nRot(actuel)
            rot2 = self.nRot(prochain)
            configF = []

            hMax = 0
            for i in range(len(grille)):
                hauteurLocale = self.hauteur(grille, i)
                if hauteurLocale > hMax:
                    hMax = hauteurLocale
            
            for p in range(len(grille)):
                for i in range(rot1):
                    
                    grilleC = self.copieGrille(grille)
                            
                    copy1 = tetro(actuel.groupe, 5, hMax + 2, 1)
                    copy1.rotation(90 * i, grilleC)
                    copy1.mouvement(p-copy1.x, grilleC)

                    
                    a = 0
                    while a == 0:
                        a = copy1.miseAJour(grilleC)

                        
                    for q in range(len(grille)):
                        
                        for j in range(rot2):

                            grilleCC = self.copieGrille(grilleC)
                            
                            copy2 = tetro(prochain.groupe, 5, hMax + 6, 1)
                            copy2.rotation(90 * j, grilleCC)
                            copy2.mouvement(q-copy2.x, grilleCC)
                            
                            if not (copy1.x, copy1.rot, copy2.x, copy2.rot) in configF:
                                configF.append((copy1.x, copy1.rot, copy2.x, copy2.rot))
                                
                                b = 0
                                    
                                while b == 0:
                                    b = copy2.miseAJour(grilleCC)
                                
                                score = self.grilleHScore(grilleCC)
                                
                                if a == 2 or b == 2:
                                    score += 1000000000
                                    
                                if meilleur == None or meilleur[0] > score:
                                    meilleur = (score, copy1.x, i)
                                    

            
            
            actuel.rotation(meilleur[2] * 90, grille)
            actuel.x = meilleur[1]
            
            return meilleur[0]


class essaiePosProchTrous(algorithme):

    def __init__(self, structPoss):
        self.structuresPossibles = structPoss
        self.ordresASuivre = None
        

    def trousDict(self, grilleC):
        d = {}
        trouColonnes = 0
        l = []
        for j in range(len(grilleC[0])):
            l = []
            for i in range(len(grilleC)):
                if grilleC[i][j] == 0 and self.hauteur(grilleC, i) > j:
                    l.append(i)
            d[j] = l
        return d

    
    def miseAJour(self, grille, actuel, prochain):
        if actuel != None and prochain != None and actuel.y == 28:
        
            meilleur = None
            prValidesP = []
            prValidesS = []
            rot1 = self.nRot(actuel)
            rot2 = self.nRot(prochain)
            configF = []

            d = self.trousDict(grille)

            hMax = 0
            for i in range(len(grille)):
                hauteurLocale = self.hauteur(grille, i)
                if hauteurLocale > hMax:
                    hMax = hauteurLocale

            ##print(d)
            
            for p in range(len(grille)):
                for i in range(rot1):
                    
                    grilleC = self.copieGrille(grille)
                            
                    copy1 = tetro(actuel.groupe, 5, hMax + 2, 1)
                    copy1.rotation(90 * i, grilleC)
                    copy1.mouvement(p-copy1.x, grilleC)

                    grilleCopies = []
                    instrucListe = []
                    
                    a = 0
                    while a == 0:
                        a = copy1.miseAJour(grilleC)
                        if copy1.y in d.keys():
                            for trouX in d[copy1.y]:
                                copy1Temp = tetro(actuel.groupe, copy1.x, copy1.y, 1)
                                encoreCopie = self.copieGrille(grilleC)
                                
                                for _ in range(abs(copy1Temp.x-trouX)):
                                    if copy1Temp.x > trouX:
                                        copy1Temp.mouvement(-1, encoreCopie)
                                    if copy1Temp.x < trouX:
                                        copy1Temp.mouvement(1, encoreCopie)
                                        
                                poulopop = 0
                                while poulopop == 0:
                                    poulopop = copy1Temp.miseAJour(encoreCopie)
                                    
                                grilleCopies.append(encoreCopie)
                                instrucListe.append({ 22 : copy1.x , copy1.y : trouX })
                                
                    grilleCopies.append(grilleC)
                    instrucListe.append({ 22 : copy1.x })
                    d2 = self.trousDict(grille)
                                    
                    for grilleCopieInd in range(len(grilleCopies)):
                        grilleCopie = grilleCopies[grilleCopieInd]
                        
                        for q in range(len(grille)):
                            
                            for j in range(rot2):

                                grilleCC = self.copieGrille(grilleCopie)
                                
                                copy2 = tetro(prochain.groupe, 5, hMax + 6, 1)
                                copy2.rotation(90 * j, grilleCC)
                                copy2.mouvement(q-copy2.x, grilleCC)
                                

                                grilleCopies2 = []
                                
                                
                                    
                                b = 0
                                        
                                while b == 0:
                                    b = copy2.miseAJour(grilleCC)
                                    if copy2.y in d2.keys():
                                        for trouX in d2[copy2.y]:
                                            copy2Temp = tetro(actuel.groupe, copy2.x, copy2.y, 1)
                                            encoreCopie = self.copieGrille(grilleCC)
                                            
                                            for _ in range(abs(copy2Temp.x-trouX)):
                                                if copy2Temp.x > trouX:
                                                    copy2Temp.mouvement(-1, encoreCopie)
                                                if copy2Temp.x < trouX:
                                                    copy2Temp.mouvement(1, encoreCopie)
                                                    
                                            poulopop = 0
                                            while poulopop == 0:
                                                poulopop = copy2Temp.miseAJour(encoreCopie)
                                                
                                            grilleCopies2.append(encoreCopie)

                                grilleCopies2.append(grilleCC)


                                for grilleCopie2 in grilleCopies2:
                                    
                                    
                                    score = self.grilleHScore(grilleCopie2)
                                        
                                    if a == 2 or b == 2:
                                        score += 1000000000
                                            
                                    if meilleur == None or meilleur[0] > score:
                                        meilleur = (score, instrucListe[grilleCopieInd], i)
                                    

            
            
            actuel.rotation(meilleur[2] * 90, grille)
            self.ordresASuivre = meilleur[1]
            return meilleur[0]

    
        elif actuel != None and self.ordresASuivre != None:
            if actuel.y in self.ordresASuivre.keys():
                dX = self.ordresASuivre[actuel.y]
                for _ in range(abs(dX - actuel.x)):
                    if dX > actuel.x:
                        actuel.mouvement(1, grille)
                    if dX < actuel.x:
                        actuel.mouvement(-1, grille)
                
            
class Algoback(algorithme):

    def __init__(self, structPoss):
        self.structuresPossibles = structPoss
        self.ordresASuivre = None
        self.coteDernier = True
        self.corr = False

    def positionValide(self, bloc, grille):
        for e in bloc.groupe:
            if bloc.x + e[0] < 0 or bloc.x + e[0] >= len(grille) or (bloc.y + e[1] < len(grille[0]) and grille[bloc.x + e[0]][bloc.y + e[1]] != 0):
                return False
        return True
    
    def trousListe(self, grilleC, hMax, coteDebut):
        l = []
        forVal = range(len(grilleC))
        if not coteDebut:
            forVal = range(len(grilleC)-1, -1, -1)
        for i in forVal:
            for j in range(min(len(grilleC[0]), hMax + 5)):
                if grilleC[i][j] == 0:
                    l.append((i, j))
        return l
            

    def positionFinie(self, bloc, grille):
            for gr in bloc.groupe:
                if bloc.y + gr[1] >= len(grille[0]) or gr[0] + bloc.x < 0 or gr[0] + bloc.x >= len(grille):
                    return False      
                if bloc.y + gr[1] == 0:
                    return True
                elif bloc.y + gr[1] > 0 and grille[gr[0] + bloc.x][bloc.y + gr[1]-1] == 0:
                    return True
            return False

    def LPP(self, bloc, grille, hMax):
        l = []
        li = self.trousListe(grille, hMax)
        for i in li:
            for k in range(self.nRot(bloc)):
                copie = tetro(bloc.groupe, 5, 27, 1)
                copie.rotation(90 * k, grille)
                copie.x = i[0]
                copie.y = i[1]
                if self.positionValide(copie, grille):
                    if self.positionFinie(copie, grille) and not (i[0],i[1],k) in l:
                         l.append((i[0], i[1], k))
        return l

    def peut_placer(self, bloc, grille):
        for e in bloc.groupe:
            if bloc.x + e[0] >= 0 and bloc.x + e[0] < len(grille) and bloc.y + e[1] >= 0 and bloc.y + e[1] < len(grille[0]):
                if grille[bloc.x + e[0]][bloc.y + e[1]] != 0:
                    return False
            else:
                return False
        return True

    def place(self, bloc, grille):
        if self.peut_placer(bloc, grille):
            for e in bloc.groupe:
                grille[bloc.x + e[0]][bloc.y + e[1]] = 1
            return True
        else:
            return False
        
            
    def trouveChemin(self, actuel, meilleur, grille):
        d = {meilleur[1] : ["x=" + str(meilleur[0])]}
        copie = tetro(actuel.groupe, 5, 28, 1)
        copie.rotation(meilleur[2] * 90, grille)
        copie.x = meilleur[0]
        copie.y = meilleur[1]

        def appendLO(d, copie, ordre):
            if copie.y in d.keys():
                if not ordre in d[copie.y]:
                    d[copie.y].append(ordre)
            else:
                d[copie.y] = [ordre]

        def creerCheminQuiMarche(copie, d, grille, g, at):
            if copie.y >= 25:
                copie.x = 5
                
                for i in range(1, 4):
                    copie.rotation(90, grille)
                    if copie.groupe in self.structuresPossibles:
                        d[25] = ["r=" + str(i)]
                        
                        return 1
                return 1
            else:
                tetrY = tetro(copie.groupe, copie.x, copie.y+1, 1)
                h = self.positionValide(tetrY, grille)
                
                tetrXG = tetro(copie.groupe, copie.x, copie.y, 1)
                dg = tetrXG.mouvement(-1, grille)
                tetrXD = tetro(copie.groupe, copie.x+1, copie.y, 1)
                dd = tetrXG.mouvement(1, grille)
                
                ccopie = tetro(copie.groupe, copie.x, copie.y, 1)
                if not h:
                    if not dd or g:
                        if not dg:
                            if not at:
                                s = 0
                                for i in range(1, 4):
                                    if ccopie.rotation(90, grille) and creerCheminQuiMarche(ccopie, d, grille, g, True) == 1:
                                        appendLO(d, copie, "r=" + str(i))
                                        return 1
                                    else:
                                        s += 1
                                if s == 3:
                                    return 0
                            else:
                                return 0
                            return 0
                        elif creerCheminQuiMarche(tetrXG, d, grille, True, False) == 1:
                            appendLO(d, copie, "x=" + str(copie.x))
                            return 1
                        else:
                            return 0
                    elif creerCheminQuiMarche(tetrXD, d, grille, False, False) == 1:
                        appendLO(d, copie, "x=" + str(copie.x))
                        return 1
                    else:
                        return 0
                elif creerCheminQuiMarche(tetrY, d, grille, False, False) == 1:
                    appendLO(d, copie, "x=" + str(copie.x))
                    return 1

        if creerCheminQuiMarche(copie, d, grille, False, False) == 0:
            return None
        elif self.positionFinie(copie, grille):
            return d

    def miseAJour(self, grille, actuel, prochain):
        if actuel != None and prochain != None and (actuel.y == 27 or self.corr):

            self.corr = False
            hMax = 0
            hMin = 0
            for i in range(len(grille)):
                temp = self.hauteur(grille, i)
                if temp > hMax:
                    hMax = temp
                if temp < hMin:
                    hMin = temp
                    
            grillescore = self.grilleHScore(grille)
                    
            record = None

            casse = False
                
            for (i, j) in self.trousListe(grille, hMax, self.coteDernier):
                for k in range(self.nRot(actuel)):
                    grilleC = self.copieGrille(grille)
                    copie = tetro(actuel.groupe, 5, 27, 1)
                    copie.rotation(k * 90, grilleC)
                    copie.x = i
                    copie.y = j
                    
                    if self.place(copie, grilleC):
                        trip1 = (i,j,k)

                        mj2 = 100

                        for (i2, j2) in self.trousListe(grilleC, hMax + 4, (not self.coteDernier)):

                            if (record != None and record[2][1] < j and j2 < hMax) or mj2 < hMax - 3:
                                break
                            else:
                                for k2 in range(self.nRot(prochain)):
                                    grilleCC = self.copieGrille(grilleC)
                                        
                                    copie2 = tetro(prochain.groupe, 5, 27, 1)
                                    copie2.rotation(k2*90, grilleCC)
                                    copie2.x = i2
                                    copie2.y = j2
                                    if self.place(copie2, grilleCC):

                                        trip2 = (i2,j2,k2)

                                        score = self.grilleHScore(grilleCC)
                                        if j2 < mj2:
                                            mj2 = j2

                                        if record == None or score < record[0]:
                                            o1 = self.trouveChemin(actuel, trip1, grille)
                                            if o1 != None and self.trouveChemin(prochain, trip2, grilleC) != None:
                                                record = (score, o1, (i, j))
                                                self.ordresASuivre = o1
                                                self.coteDernier = (i < 5)
                                    
            
        elif actuel != None and self.ordresASuivre != None:
            if actuel.y in self.ordresASuivre.keys():
                ordreliste = self.ordresASuivre[actuel.y]
                lon = len(ordreliste)
                for i in range(lon):
                    ordre = ordreliste[lon - 1 - i]
                    if ordre.startswith("r="):
                        actuel.rotation(360-int(ordre[2:]) * 90, grille)
                    else:
                        actuel.x = int(ordre[2:])
            elif len(self.ordresASuivre) <= 1:
                self.ordresASuivre = None
                self.corr = True

class algobasegen(algorithme):

    def __init__(self, structPoss, scoret, hdel, scoredel, lt):
        self.structuresPossibles = structPoss
        self.ordresASuivre = None
        self.scoretrou = scoret
        self.hdelta = hdel
        self.scoredelta = scoredel
        self.limiteTroncature = lt

    def positionValide(self, bloc, grille):
        for e in bloc.groupe:
            if bloc.x + e[0] < 0 or bloc.x + e[0] >= len(grille) or (bloc.y + e[1] < len(grille[0]) and grille[bloc.x + e[0]][bloc.y + e[1]] != 0):
                return False
        return True
    
    def trousListe(self, grilleC, hMax):
        l = []
        
        for i in range(len(grilleC)):
            for j in range(min(20, hMax + 3)):
                if j < len(grilleC[0]) and grilleC[i][j] == 0:
                    l.append((i, j))
        return l

    def positionFinie(self, bloc, grille):
            for gr in bloc.groupe:
                if bloc.y + gr[1] >= len(grille[0]) or gr[0] + bloc.x < 0 or gr[0] + bloc.x >= len(grille):
                    return False      
                if bloc.y + gr[1] == 0:
                    return True
                elif bloc.y + gr[1] > 0 and grille[gr[0] + bloc.x][bloc.y + gr[1]-1] == 0:
                    return True
            return False

    def LPP(self, bloc, grille, hMax):
        l = []
        li = self.trousListe(grille, hMax)
        for i in li:
            for k in range(self.nRot(bloc)):
                copie = tetro(bloc.groupe, 5, 27, 1)
                copie.rotation(90 * k, grille)
                copie.x = i[0]
                copie.y = i[1]
                if self.positionValide(copie, grille):
                    if self.positionFinie(copie, grille) and not (i[0],i[1],k) in l:
                         l.append((i[0], i[1], k))
        return l

    def peut_placer(self, bloc, grille):
        for e in bloc.groupe:
            if bloc.x + e[0] >= 0 and bloc.x + e[0] < len(grille) and bloc.y + e[1] >= 0 and bloc.y + e[1] < len(grille[0]):
                if grille[bloc.x + e[0]][bloc.y + e[1]] != 0:
                    return False
            else:
                return False
        return True

    def place(self, bloc, grille):
        if self.peut_placer(bloc, grille):
            for e in bloc.groupe:
                grille[bloc.x + e[0]][bloc.y + e[1]] = 1
            return True
        else:
            return False
        
            
    def trouveChemin(self, actuel, meilleur, grille):
        d = {meilleur[1] : ["x=" + str(meilleur[0])]}
        copie = tetro(actuel.groupe, 5, 28, 1)
        copie.rotation(meilleur[2] * 90, grille)
        copie.x = meilleur[0]
        copie.y = meilleur[1]

        def appendLO(d, copie, ordre):
            if copie.y in d.keys():
                d[copie.y].append(ordre)
            else:
                d[copie.y] = [ordre]

        def creerCheminQuiMarche(copie, d, grille, g, at):
            if copie.y >= 25:
                copie.x = 5
                
                for i in range(1, 4):
                    copie.rotation(90, grille)
                    if copie.groupe in self.structuresPossibles:
                        d[25] = ["r=" + str(i)]
                        
                        return 1
                return 1
            else:
                tetrY = tetro(copie.groupe, copie.x, copie.y+1, 1)
                h = self.positionValide(tetrY, grille)
                
                tetrXG = tetro(copie.groupe, copie.x, copie.y, 1)
                dg = tetrXG.mouvement(-1, grille)
                tetrXD = tetro(copie.groupe, copie.x+1, copie.y, 1)
                dd = tetrXG.mouvement(1, grille)
                
                ccopie = tetro(copie.groupe, copie.x, copie.y, 1)
                if not h:
                    if not dd or g:
                        if not dg:
                            if not at:
                                s = 0
                                for i in range(1, 4):
                                    if ccopie.rotation(90, grille) and creerCheminQuiMarche(ccopie, d, grille, g, True) == 1:
                                        appendLO(d, copie, "r=" + str(i))
                                        return 1
                                    else:
                                        s += 1
                                if s == 3:
                                    return 0
                            else:
                                return 0
                            return 0
                        elif creerCheminQuiMarche(tetrXG, d, grille, True, False) == 1:
                            appendLO(d, copie, "x=" + str(copie.x))
                            return 1
                        else:
                            return 0
                    elif creerCheminQuiMarche(tetrXD, d, grille, False, False) == 1:
                        appendLO(d, copie, "x=" + str(copie.x))
                        return 1
                    else:
                        return 0
                elif creerCheminQuiMarche(tetrY, d, grille, False, False) == 1:
                    appendLO(d, copie, "x=" + str(copie.x))
                    return 1

        if creerCheminQuiMarche(copie, d, grille, False, False) == 0:
            return None
        elif self.positionFinie(copie, grille):
            return d

    def miseAJour(self, grille, actuel, prochain):
        if actuel != None and prochain != None and actuel.y == 27:
            
            hMax = 0
            hMin = 0
            for i in range(len(grille)):
                temp = self.hauteur(grille, i)
                if temp > hMax:
                    hMax = temp
                if temp < hMin:
                    hMin = temp
                    
            grillescore = self.grilleHScore(grille)
                    
            record = None

            casse = False
                
            for (i, j) in self.trousListe(grille, hMax):
                for k in range(self.nRot(actuel)):
                    grilleC = self.copieGrille(grille)
                    copie = tetro(actuel.groupe, 5, 27, 1)
                    copie.rotation(k * 90, grilleC)
                    copie.x = i
                    copie.y = j
                    
                    if self.place(copie, grilleC):
                        trip1 = (i,j,k)

                        for (i2, j2) in self.trousListe(grilleC, hMax):
                            for k2 in range(self.nRot(prochain)):
                                grilleCC = self.copieGrille(grilleC)
                                    
                                copie2 = tetro(prochain.groupe, 5, 27, 1)
                                copie2.rotation(k2*90, grilleCC)
                                copie2.x = i2
                                copie2.y = j2
                                if self.place(copie2, grilleCC):

                                    trip2 = (i2,j2,k2)

                                    score = self.grilleHScoreGen(grilleCC, self.scoretrou, self.hdelta, self.scoredelta)

                                    if record == None or score < record[0]:
                                        o1 = self.trouveChemin(actuel, trip1, grille)
                                        if o1 != None and self.trouveChemin(prochain, trip2, grilleC) != None:
                                            record = (score, o1)
                                            self.ordresASuivre = o1
                                            if grillescore - score > self.limiteTroncature:
                                                break
                                                break
                                                break
                                                break
                                    
            
        elif actuel != None and self.ordresASuivre != None:
            if actuel.y in self.ordresASuivre.keys():
                ordreliste = self.ordresASuivre[actuel.y]
                lon = len(ordreliste)
                for i in range(lon):
                    ordre = ordreliste[lon - 1 - i]
                    if ordre.startswith("r="):
                        actuel.rotation(360-int(ordre[2:]) * 90, grille)
                    else:
                        actuel.x = int(ordre[2:])
