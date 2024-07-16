from torch import FloatTensor,matmul,randn
input = FloatTensor([0,5,2,7,4,2,1,6,7,3])
temp = randn(10,4)
print(temp)
print(matmul(input,temp))
print(temp)
print(temp[2][3])

from genomedefineradv import *
temp = cell("asd","asd","asd")
print(temp.inputointe)
