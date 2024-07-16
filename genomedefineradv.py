import random
import copy
from torch import FloatTensor,matmul,randn,Tensor


#0 is time cycle thus always 
#NEW ONE  0 same
#age is 5
#1234 nsew if its border
#6789 nsew is if its a physical wall
#10 12 13 14 topleft topright btmright btmleft



#0123 are move nsew respectively or at least try to
#while  4 is random

class cell():
    inputs =14
    internal = 5
    outputs = 5
    def __init__(self, name, colour):
        self.inputointe = randn(cell.inputs,cell.internal)
        self.intetooutp = randn(cell.internal,cell.outputs)
        self.id = name
        self.colour = colour
    def mutation(self):
        for i in range(random.randint(1,4)):
            randx = random.randint(0,cell.inputs-1)
            randy = random.randint(0,cell.internal-1)
            self.inputointe[randx][randy] += random.uniform(-1,1)
        for i in range(random.randint(1,4)):
            randx = random.randint(0,cell.internal-1)
            randy = random.randint(0,cell.outputs-1)
            self.intetooutp[randx][randy] += random.uniform(-1,1)
        self.colour = self.colour[1:]
        r = self.colour[:2]
        r = min(int(r,16) + random.randint(-32,32),255)
        r = max(r,0)
        g = self.colour[2:4]
        g = min(int(g,16) + random.randint(-32,32),255)
        g = max(g,0)
        b = self.colour[4:6]
        b = min(int(b,16) + random.randint(-32,32),255)
        b = max(b,0)
        self.colour = "#" + hex(r)[2:].zfill(2) + hex(g)[2:].zfill(2) + hex(b)[2:].zfill(2)
        return self
    def movement(self,arr):#arr stands for the input sensors in normal array format
        arr = Tensor(arr)
        arr = matmul(arr,self.inputointe)
        arr = matmul(arr,self.intetooutp)
        return arr
def listtocoord(arr):
    xlist2 = []
    ylist2 = []
    clist2 = []
    for i in arr:
        xlist2.append(i[0])
        ylist2.append(i[1])
        clist2.append(i[2].colour)
    return xlist2,ylist2,clist2


#431007d
#60100ab
