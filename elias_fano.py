import sys, math, hashlib

#------------------------------BitArray Class-------------------------------
#To crete a BitArray object give as argument the number of bits you want to
#store. Note that the size of the BitArray object is the total count of bits
#of the bytes needed to store the number of bits given as argument on create

class BitArray:

    #Constructor
    #Sets all initial values of bits to "0"
    def __init__(self, size):
        self.size = int(math.ceil(size/8)*8)
        self.bytearray = bytearray((size+7)>>3)
        for i in range(len(self.bytearray)):
            self.bytearray[i] = 0

    #Function that returns the bytearray object
    def ByteArray(self):
        return self.bytearray

    #Function that returns the value of an individual bit
    def get_bit(self, bit_ix):

        if not isinstance(bit_ix, int):
            raise IndexError("bit array index not an int")

        if bit_ix < 0 or bit_ix >= self.size:
            raise IndexError("bit array index out of range")

        byte_ix = bit_ix >> 3
        bit_ix = bit_ix & 7
        return (self.bytearray[byte_ix] >> bit_ix) & 1

    #Function that sets the value of an individual bit
    def set_bit(self, bit_ix, val):
        if not isinstance(bit_ix, int):
            raise IndexError("bit array index not an int")

        if bit_ix < 0 or bit_ix >= self.size:
            raise IndexError("bit array index out of range")

        if not isinstance(val, int):
            raise ValueError("bit array value not an int")

        if val not in (0, 1):
            raise ValueError("bit array value must be 0 or 1")

        byte_ix = bit_ix >> 3
        bit_ix = bit_ix & 7
        bit_val = 1 << bit_ix

        if val:
            self.bytearray[byte_ix] |= bit_val
        else:
            self.bytearray[byte_ix] &= ~bit_val

    #Functions that use index notation for accessing individual bits
    def __getitem__(self, key):
        return self.get_bit(key)

    def __setitem__(self, key, value):
        self.set_bit(key, value)

    #Function that prints the whole bytearray in the desired format
    def print(self):
            for i in range(len(self.bytearray)):
                for j in range(8):
                    __builtins__.print(self[8*i+j], end="")
                __builtins__.print()
#---------------------------------------------------------------------------


#--------------Functions--------------

#Masks the l least significant bits
def lmask(l):
    temp = 1
    for i in range(l-1):
        temp = temp << 1
        temp = temp + 1
    return temp

#Masks the u most significant bits
def umask(u,l):
    temp = 1
    for i in range(u-1):
        temp = temp << 1
        temp = temp + 1
    return temp << l
#-------------------------------------


#-------------------------INPUT-------------------------
filename = sys.argv[1]
with open(filename,"r") as f:
    numberList = f.read().splitlines()

numberList = [int(i) for i in numberList]

n = len(numberList)
mx = numberList[n-1]

l = int(math.modf(math.log(mx/n,2))[1])
u = int(math.ceil(math.log(mx,2))) - l

numberOfLBits = n * l
numberOfUBits = n + int(math.floor(mx/math.pow(2,l)))
#-------------------------------------------------------


#-----------------------L Array-----------------------
Larray = BitArray(numberOfLBits)
#BitArray.initializeZero(Larray)

for i in range(n):
    lower = numberList[i] & lmask(l)
    temp = lower
    for j in range(l):
        bitToSet = temp & 1
        Larray[(i*l)+l-j-1] = bitToSet
        temp = temp >> 1
#-----------------------------------------------------


#-----------------------U Array-----------------------
Uarray = BitArray(numberOfUBits)
#BitArray.initializeZero(Uarray)

counter = -1
for i in range(n):
    upper = numberList[i] & umask(u,l)
    upper = upper >> l
    if i==0:
        prev = 0
    else:
        prev = numberList[i-1] & umask(u,l)
        prev = prev >> l
    upper = upper - prev
    counter = counter + upper + 1
    Uarray[counter] = 1
#-----------------------------------------------------


#----------OUTPUT-------------
print("l",l)
print("L")
BitArray.print(Larray)
print("U")
BitArray.print(Uarray)
#------------------------------


#----------SHA-256-------------
L = BitArray.ByteArray(Larray)
U = BitArray.ByteArray(Uarray)

m = hashlib.sha256()
m.update(L)
m.update(U)
digest = m.hexdigest()
print(digest)
#------------------------------