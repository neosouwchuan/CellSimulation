import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pickle
from genomedefineradv import *
import copy
filesavename = "curvebarrier/curvenewver0"#the map file must have at least one extra empty line
barriername = "curvebarrier.map"
version = 0
loadfromfile = False
time_steps = 192
size = 128
numberCells = 300
survivedQueue = 100
chanceFresh = .1
spawnboundaries = [103,0,size-1,size-1]#topleft,then btm right [103,0,size-1,size-1]
def printoutcollision(collision):
    for i in collision:
        for j in i:
            if j == 0 or j == 1:
                print(j,end=" ")
            else:
                print("s",end=" ")
        print("")
#Basic one cell movement plotted outputs
def survivalCondition(celllist,collision):
    survived = []
    for i in range(len(celllist)):  
        collision[celllist[i][1]][celllist[i][0]] = 0
        if(celllist[i][0]<25):# and (celllist[i][1]<64):
            survived.append(celllist[i][2])
    return survived

def cellmove(x,y,uniquecell,timestep):#CELLMOVE CANNOT BE MOVED TO GENOME BECAUSE COLLISION NOT DEFINED THERE
    
    changex = 0
    changey = 0
    neuronss = [0 for i in range(cell.inputs)]

    #Prep sensor neurons
    neuronss[0] = 1
    neuronss[5] = timestep/time_steps#gives the proportional age for seasonal movement changes
    #nsew 2345
    #neurons[4] = 1 if x==0 else (1 if collision[x-1][y] != 0)
    #neurons[5] = 1 if x==127 else 1 if collision[x+1][y] != 0
    #neurons[2] = 1 if y==127 else 1 if collision[x][y+1] != 0
    #neurons[3] = 1 if y==0 else 1 if collision[x][y-1] != 0
    #returns the nsew blocked or not
    if x==0:
        neuronss[4] =1
    elif collision[y][x-1] != 0:
        neuronss[9] = 1
    if x==size - 1  :
        neuronss[3] = 1
    elif collision[y][x+1] != 0:
        neuronss[8] = 1 
    if y==size - 1:
        neuronss[1] = 1
    elif collision[y+1][x] != 0:
        neuronss[6] = 1
    if y==0:
        neuronss[2] = 1
    elif collision[y-1][x] != 0:
        neuronss[7] = 1
    if x<127 and x>0 and y<127 and y>0:#OKOK YES I KNOW THAT THE NEURON inputs are wrong
        #BUT IT DOESNT MATTER CAUSE ONLY MIXED UP THATS NN for u
        if collision[y+1][x-1] == 1:
            neuronss[10] = 1
        if collision[y+1][x+1] == 1:
            neuronss[11] = 1
        if collision[y-1][x+1] == 1:
            neuronss[12] = 1
        if collision[y-1][x-1] == 1:
            neuronss[13] = 1
    #print(neurons)
    #NEURONS PROCESSED THEN MOVEMENT TIME
    neuronst = uniquecell.movement(neuronss)
    if neuronst[4]>1:#activate random movement
        changex += random.randint(-1,1)
        changey += random.randint(-1,1)
    if neuronst[0]>1:
        changey +=1
    if neuronst[1]>1:
        changey -=1
    if neuronst[2]>1:
        changex +=1
    if neuronst[3]>1:
        changex -=1

    return changex, changey
idcounter = 0
celllist = []
global collision
collision = []
#THIS PART MAKES THE WALLS
mapp = open(barriername)
for mappcounter in range(128):
    mappreadline = mapp.readline()[:-1]
    mappreadline = [int(i) for i in mappreadline]
    collision.append(copy.copy(mappreadline))
mapp.close()
#THIS PART ENDS MAKING

if loadfromfile:#LOAD INSTEAD OF GENERATE
    with open(filesavename + str(version), "rb") as f:
        celllist = pickle.load(f)
else:
    cellist = []
    for i in range(numberCells):#generate cells
        color = "%06x" % random.randint(0, 0xFFFFFF)
        newcell = cell(idcounter,"#"+color)
        cellist.append(newcell)
        idcounter +=1
for i in range(len(celllist)):#generate cells
    possiblex = random.randint(spawnboundaries[0],spawnboundaries[2])
    possibley = random.randint(spawnboundaries[1],spawnboundaries[3])
    while not collision[possibley][possiblex] == 0:
        possiblex = random.randint(spawnboundaries[0],spawnboundaries[2])
        possibley = random.randint(spawnboundaries[1],spawnboundaries[3])
    #possiblex = int(possiblex)
    #possibley = int(possibley)
    #print(newcell.colour)
    celllist.append([possiblex,possibley,newcell])#IMPORTANT LIST
    collision[possibley][possiblex] = newcell
if False:
    neurons = []
    for i in range(numgenomes+1):
        neurons.append(0)
    neurons[0] = 1
    for i in newcell.genomes:
        neurons[i.target] = neurons[i.source]*i.weight
    print(neurons)
#STARTING GENERATION PART
def onegeneration(celllist): #wdyt
    global collision
    for timestep in range(time_steps):# run for n number generations
    #firstly populate with celllist
    #done nothing lol
    #then move
        for i in range(len(celllist)):#handles cell movement including collision
            changex,changey = cellmove(celllist[i][0],celllist[i][1],celllist[i][2],timestep)
            initialx, initialy = celllist[i][0],celllist[i][1]
            finalx, finaly = celllist[i][0],celllist[i][1]
            if initialx + changex>size - 1:
                changex = size - 1 -initialx
            if initialx + changex<0:
                changex = 0-initialx
            if initialy + changey>size - 1:
                changey = size - 1-initialy
            if initialy + changey<0:
                changey = 0-initialy
            if changex>0:
                forstep = 1
            elif changex < 0:
                forstep = -1
                
            if changex!= 0:
                for j in range(forstep,(changex)+forstep,forstep):

                    if collision[initialy][initialx + j] != 0:
                        break
                    finalx = initialx + j
            if changey>0:
                forstep = 1
            else:
                forstep = -1
            for j in range(forstep,changey+forstep,forstep):
                if collision[initialy+j][finalx] != 0:
                    break
                else:
                    finaly = initialy+j
            collision[initialy][initialx] = 0
            collision[finaly][finalx] = celllist[2]
            celllist[i][0] = finalx
            celllist[i][1] = finaly
    #then check who survived
    #afterwards return celllist again to be populated and mutated
    #DEFINE SURVIVAL CONDITION HERE REMEMBER THAT COORD DOESNT MATTER AFTERWARDS041791
    # if the xposition is lesser than 15 survive and continue
    #reset collision here while celllist is definite along with aboth
    survived = survivalCondition(celllist,collision)
    return survived
highscore = 0
fit = []
for i in range(100):#generate cells
    color = "%06x" % random.randint(0, 0xFFFFFF)
    newcell = cell(idcounter,"#"+color)
    fit.append(newcell)
for i in range(version,version + 15000):#Number of generations duh

    if i%1 == 0:
        print("generation",i)
    # Presumably some sanity check
    # dicc = {}
    # for j in collision:
    #     for k in j:
    #         temp = type(k)
    #         if temp not in dicc.keys():
    #             dicc[temp] = 1
    #         else:
    #             dicc[temp] += 1
    # print(dicc)
    savefile = copy.copy(celllist)
    survived = onegeneration(celllist)
    highscore = max(highscore,len(survived))
    for j in survived:
        fit.append(j)
    fit = fit[len(fit)-100:]
    if highscore == len(survived) :
        print("lensurvived",len(savefile),"highest",highscore)
        with open(filesavename+"high"+str(i), 'wb') as f:
            pickle.dump(savefile, f)
    celllist = []
    collision = []
    #REMAKE the walls
    mapp = open(barriername)
    for mappcounter in range(128):
        mappreadline = mapp.readline()[:-1]
        mappreadline = [int(i) for i in mappreadline]
        collision.append(copy.copy(mappreadline))
    mapp.close()
    id = 0
    for j in range(numberCells):#size of subsequent generations
        if random.random()<chanceFresh:
            color = "%06x" % random.randint(0, 0xFFFFFF)
            newcell = cell(idcounter,"#"+color)
            idcounter +=1
        else:
            newcell = copy.copy(random.choice(fit))
        if random.randint(0,100)<30:
            newcell = newcell.mutation()
        if True:
            possiblex = random.randint(spawnboundaries[0],spawnboundaries[2])
            possibley = random.randint(spawnboundaries[1],spawnboundaries[3])
            while not collision[possibley][possiblex] == 0:
                possiblex = random.randint(spawnboundaries[0],spawnboundaries[2])
                possibley = random.randint(spawnboundaries[1],spawnboundaries[3])
        celllist.append([possiblex,possibley,newcell])#IMPORTANT LIST
        collision[possibley][possiblex] = newcell
    
    idcounter +=1
    

with open(filesavename, 'wb') as f:
    pickle.dump(celllist, f)



