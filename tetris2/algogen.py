from objet.tetro import *
from objet.algorithmes import *

import random
import multiprocessing
import concurrent.futures
import time

leL = [(0,0), (0, -1), (-1, -1), (0, 1)]
antiL = [(0,0), (0, -1), (1, -1), (0, 1)]
leT = [(0,0), (0, 1), (1, 0), (-1, 0)]
leI = [(0, -1), (0,0), (0,1),(0, 2)]
LeZ = [(-1,0), (0,0), (0, 1), (1, 1)]
LeS = [(1,0), (0,0), (0, 1), (-1, 1)]
leBloc = [(-1,0), (0,0), (-1, 1), (0, 1)]

leGrosBloc = [(-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1), (1, -1), (0, -1), (-1, -1)]

structuresPossibles = [leL, leT, leI, LeZ, leBloc, LeS, antiL]

def genererGrille(largeur, hauteur):
    l = []
    for i in range(largeur):
        a = []
        for j in range(hauteur):
            a.append(0)
        l.append(a)
    return l

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


def mutation(qplet):
    i = random.randint(0, 4)
    qplet2 = (0,0,0,0)
    if i == 0:
        qplet2 = (max(0, min(40, qplet[0] + random.randint(-5, 5))), qplet[1], qplet[2], qplet[3])
    elif i == 1:
        qplet2 = (qplet[0], max(1, min(11, qplet[1] + random.randint(-3, 3))), qplet[2], qplet[3])
    elif i == 2:
        qplet2 = (qplet[0], qplet[1], max(0, min(40, qplet[2] + random.randint(-5, 5))), qplet[3])
    else:
        qplet2 = (qplet[0], qplet[1], qplet[2], max(0, min(60, qplet[3] + random.randint(-5, 5))))
    return qplet2

def scoreqplet(qplet):
    global structuresPossibles
        
    a = None
    p = None
    alg = algobasegen(structuresPossibles, qplet[0], qplet[1], qplet[2], qplet[3])
    sco = 0
    nombreTotal = 0
    TTot = 0
    gr = genererGrille(10, 20)
    perdu = False
    
    while sco < 200000:
        temp = time.time()
        if a == None:
            
            if p == None:
                struct = random.choice(structuresPossibles)
                a = tetro(struct, 5, 29, 1)

                struct2 = random.choice(structuresPossibles)
                p = tetro(struct2, 5, 29, 1)
            else:
                a = p
                struct = random.choice(structuresPossibles)

                while a.groupe == struct:
                    struct = random.choice(structuresPossibles)
                        
                p = tetro(struct, 5, 29, 1)

        if a != None:
            i = a.miseAJour(gr)
            alg.miseAJour(gr, a, p)
            
            if i == 2 or perdu:
                break;
            elif i == 1:
                a = p
                struct = random.choice(structuresPossibles)

                while a.groupe == struct:
                    struct = random.choice(structuresPossibles)
                        
                p = tetro(struct, 5, 29, 1)
                
        nombreTotal += 1
        TTot += time.time() - temp
        l = supprimerLigne(gr)
        sco += len(l) * 10
    print(str(sco) + " / " + str(TTot / nombreTotal))
    return (sco - (TTot / nombreTotal))

def associe(lt, qplet):

    n = scoreqplet(qplet)
    
    lt.append((n, qplet))

def classement(l):
    lt = []
    lp = []

    for i in l:
        lt.append((scoreqplet(i), i))
    
    d = lambda x : x[0] * -1
    print(d(lt[0]))
    lt.sort(key = lambda x : x[0] * -1)
    qpll = [i[1] for i in lt]

    return qpll

def enfants(qplet1, qplet2):
    enfant1 = (qplet1[0], qplet2[1], qplet1[2], qplet2[3])
    enfant2 = (qplet2[0], qplet1[1], qplet2[2], qplet1[3])
    enfant3 = (qplet2[0], qplet1[1], qplet1[2], qplet2[3])
    enfant4 = (qplet1[0], qplet2[1], qplet2[2], qplet1[3])
    return (enfant1, enfant2, enfant3, enfant4)

def nouvgen(gen):
    l = []
    l.append(gen[0])
    for i in range(4):
        qenf = enfants(gen[0], gen[i+1])
        l.append(mutation(qenf[0]))
        l.append(mutation(qenf[1]))
        l.append(mutation(qenf[2]))
        l.append(mutation(qenf[3]))

    while len(l) < 20:
        l.append((random.randint(0, 40), random.randint(1, 11), random.randint(0, 40), random.randint(0, 61)))

    return l
    
def jplvjvm():
    
    gen = [(random.randint(0, 40), random.randint(1, 11), random.randint(0, 40), random.randint(0, 61)) for _ in range(20)]
    gen = classement(gen)
    meilleur = gen[0]
    lim = 0
    
    while lim < 3:
        meilleur = gen[0]
        print(meilleur)
        gen = nouvgen(gen)
        with open("sauvgen.txt", "w") as f:
            for i in gen:
                f.write(str(i) + "\n")
                
        gen = classement(gen)
        if meilleur == gen[0]:
            lim += 1
        else:
            lim = 0
            
    return meilleur

def algogensauv():

    fichier = open("sauvgen.txt", "r")
    
    gen = []
    for l in fichier.readlines():
        recup = l[1:len(l)-2]
        quatstr = recup.split(", ")
        gen.append((int(quatstr[0]), int(quatstr[1]), int(quatstr[2]), int(quatstr[3])))

    print(gen)
    gen = classement(gen)
    meilleur = gen[0]
    lim = 0
    
    while lim < 100:
        meilleur = gen[0]
        print(meilleur)
        gen = nouvgen(gen)
        with open("sauvgen.txt", "w") as f:
            for i in gen:
                f.write(str(i) + "\n")
        gen = classement(gen)
        if meilleur == gen[0]:
            lim += 1
        else:
            lim = 0
            
    return meilleur
            

algogensauv()
