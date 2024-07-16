import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from genomedefineradv import *
import pickle
#Basic one cell movement plotted outputs
size    = 128
time_steps = 192
spawnboundaries = [103,0,size-1,size-1]#topleft,then btm right [103,0,size-1,size-1]
savename = "curvebarrier/curvenewver0high185"
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
#for i in gelist:
    #print(i.source,i.target,i.weight)
idcounter = 0
celllist = []
collision = []
wallx = []
wally = []
def adder(x,y):
    global wallx
    global wally
    wallx.append(x)
    wally.append(y)
mapp = open("curve2.map")
for mappcounter in range(128):#represents line counter
    mappreadline = mapp.readline()[:-1]
    mappreadline = [int(i) for i in mappreadline]
    collision.append(copy.copy(mappreadline))
    for x in range(len(mappreadline)):
        if mappreadline[x] == 1:
            adder(x,mappcounter)
#HERE LOADS GENERATION#8000 works
with open(savename, "rb") as f:
    celllist = pickle.load(f)
    for i in celllist:
        possiblex = random.randint(spawnboundaries[0],spawnboundaries[2])
        possibley = random.randint(spawnboundaries[1],spawnboundaries[3])
        while not collision[possibley][possiblex] == 0:
            possiblex = random.randint(spawnboundaries[0],spawnboundaries[2])
            possibley = random.randint(spawnboundaries[1],spawnboundaries[3])
        collision[possibley][possiblex] = i[2]
        i[0] = possiblex
        i[1] = possibley
if False: 
    neurons = []
    for i in range(numgenomes+1):
        neurons.append(0)
    neurons[0] = 1
    for i in newcell.genomes:
        neurons[i.target] = neurons[i.source]*i.weight
    print(neurons)
xlist = []
ylist = []
clist = []
xlist,ylist,clist = listtocoord(celllist)
#STARTING PLOTTING PART

fig, ax = plt.subplots()
marker_size = 3 #up this to make points more visible
tigger = 1
print(len(collision))
hasprinted = True  
def animate(i):
    global collision
    global tigger
    """ Perform animation step. """
    #important - the figure is cleared and new axes are added
    fig.clear()
    ax = fig.add_subplot(111, aspect='equal', autoscale_on=False, xlim=(-1,size), ylim=(-1,size))
    #the new axes must be re-formatted
    
    # and the elements for this frame are added
    ax.text(0.02, 0.95, 'Time step = %d' % i, transform=ax.transAxes)
    xlist,ylist,clist = listtocoord(celllist)
    for i in range(len(celllist)):#handles cell movement including collision
        changex,changey = cellmove(celllist[i][0],celllist[i][1],celllist[i][2],tigger)
        initialx, initialy = celllist[i][0],celllist[i][1]
        finalx, finaly = celllist[i][0],celllist[i][1]

        if initialx + changex>size-1:
            changex = size-1-initialx
        if initialx + changex<0:
            changex = 0-initialx
        if initialy + changey>size-1:
            changey = size-1-initialy
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
        #celllist[i][0] += changex
        #celllist[i][1] += changey
    tigger += 1
    xlist,ylist,clist = listtocoord(celllist)
    s = ax.scatter(xlist,ylist, c = clist, marker = "s", edgecolor = None,s=marker_size)#HERES THE ERROR
    s2 = ax.scatter(wallx,wally, c = "#000000", marker = "s", edgecolor = None,s=marker_size)
    fig.colorbar(s)
    
   
    
print(xlist,ylist,clist)


plt.grid()
ani = animation.FuncAnimation(fig, animate, interval=100, frames=range(time_steps))
ani.save('onecell4.gif', writer='pillow')
