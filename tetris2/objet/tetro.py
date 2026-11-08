class tetro():
    def __init__(self, l, px, py, cId):
        self.groupe = l.copy()
        self.x = px
        self.y = py
        self.couleur = cId
        self.rot = 0

    def miseAJour(self, grilleJeu):
        pos = False
        for i in self.groupe:
            if i[1] + self.y == 0:
                pos = True
            try:
                if i[1] + self.y - 1 >= 0 and i[1] + self.y - 1 < len(grilleJeu[0]) and grilleJeu[i[0] + self.x][i[1] + self.y - 1] != 0:
                    pos = True
            except:
                pos = False
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

    def posXValide(self, grille):
        for i in self.groupe:
            px = self.x + i[0]
            if px < 0 or px >= len(grille):
                return False
        return True

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
                self.rot = (self.rot + rotationHoraire) % 360
                for i in range(len(self.groupe)):
                    if i < len(groupeC):
                        self.groupe[i] = groupeC[i]
                return True
        return False
        
