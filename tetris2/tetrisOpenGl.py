import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import numpy

from objet.tetro import *
from objet.algorithmes import * 
import random
import time

perdu = False
score = 0
actuel = None
prochain = None
tickCounter = 0
nBlocs = 0
anim = 0
ltr = []

temps = time.time()

##initialisation de OpenGL

tailleX = 10 * 20 + 120 * 2
tailleY = 20 * 20 + 120 * 2

if not glfw.init():
    raise Exception("initialisation ratée")

window = glfw.create_window(tailleX, tailleY, "TetVer PyOpenGl 1.0", None, None)

glfw.make_context_current(window)


glClearColor(0.1,0.1,0.1,1)

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

leL = [(0,0), (0, -1), (-1, -1), (0, 1)]
antiL = [(0,0), (0, -1), (1, -1), (0, 1)]
leT = [(0,0), (0, 1), (1, 1), (-1, 1)]
leI = [(0, -1), (0,0), (0,1),(0, 2)]
LeZ = [(-1,0), (0,0), (0, 1), (1, 1)]
LeS = [(1,0), (0,0), (0, 1), (-1, 1)]
leBloc = [(-1,0), (0,0), (-1, 1), (0, 1)]

leGrosBloc = [(-1,0), (0,0), (1,0), (-1,1), (0,1), (1,1), (1, -1), (0, -1), (-1, -1)]

structuresPossibles = [leL, leT, leI, LeZ, leBloc, LeS, antiL]
Couleurs = [(255,0,0), (0,0,255), (0,255,0), (255,255,0), (255,0,255), (255,255,255), (150,255,255), (255,100,0), (69,100,255)]
prochain = None

algo = AlgoTest(structuresPossibles)

def dessinGrille():
    global grille
    for i in range(len(grille)):
        for j in range(len(grille[0])):
            if grille[i][j] != 0:
                col = Couleurs[grille[i][j] - 1]
                glColor3f(float(col[0]/255),float(col[1]/255),float(col[2]/255));
                glVertex2i(6 + i, 26-j);

    """if actuel != None:
        col = Couleurs[actuel.couleur - 1]
        glColor3f(float(col[0]/255),float(col[1]/255),float(col[2]/255));
        for c in actuel.groupe:
            glVertex2i(6 + actuel.x + c[0], 26-actuel.y + c[1]);

    if prochain != None:
        col = Couleurs[prochain.couleur - 1]
        glColor3f(float(col[0]/255),float(col[1]/255),float(col[2]/255));
        for c in prochain.groupe:
            glVertex2i(2 + c[0], 18 + c[1]);"""

def maxRecup(l):
    m = l[0]
    for i in range(1, len(l)):
        if m[0] < l[i][0]:
            m = l[i]
    return m

while not glfw.window_should_close(window):

    glfw.poll_events()
    
    glClear(GL_COLOR_BUFFER_BIT);
    glMatrixMode( GL_PROJECTION );
    glLoadIdentity();
    gluOrtho2D( 0.0, float(tailleX), float(tailleY),0.0 );
    glScale(20,20,1)
    glPointSize(18)
            
    ##TBT = round(max(2, 20 - nBlocs / 5))
            
        
        
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

    if actuel != None:
        i = actuel.miseAJour(grille)
        while i == 0:
            i = algo.miseAJour(grille, actuel, prochain)
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
    glBegin(GL_POINTS);

    dessinGrille()

    glEnd();
    
    glfw.swap_buffers(window)

glfw.terminate()
