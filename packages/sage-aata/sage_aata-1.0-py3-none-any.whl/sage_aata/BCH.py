
def create_matrix(p,n,A):
    matrix = []
    for i in range(0,n-p.degree()):
        row = p*(x^i)
        row = list(row)
        while len(row)!=n:
            row.append(0)
        matrix.append(row)
    matrix1 = []
    h = (x^n+1)/p
    h = A(h)
    for i in range(0,n-h.degree()):
        h = A(h)
        row = h*(x^i)
        row = A(row)
        row = list(row)
        row.reverse()
        while len(row)<n:
            row.insert(0,0)
        matrix1.append(row)
    return matrix, matrix1

import random

class Bernoulli:
    # define the constructor, that requires a parameter p, which should
    # be between zero and one.
    def __init__(self, p):
        self.p = p
    
    # define the method that will display information about the 
    # object when in a print statement
    def __repr__(self):
        return f"Bernoulli distribution with parameter {self.p}"
    
    # define the method that performs a random trial from the 
    # Bernoulli distribution based on the parameter p
    def randomTrial(self):
        value = random.random()
        if value < self.p:
            return 1
        else:
            return 0
        
class BurstChannel:
    def __init__(self, b, p):
        self.B = Bernoulli(b)
        self.burst = Bernoulli(p)
    def __repr__(self):
        return f"Burst Channel based on {self.B}"
    
    
    def transmit(self,message):
        previous_flip = False
        flip = False
        for i in range(0,len(message)):
            if not previous_flip:
                previous_flip = self.B.randomTrial()
                if previous_flip:
                    message[i] = (message[i]+1) % 2
            else:
                previous_flip = self.burst.randomTrial()
                if previous_flip:
                    message[i] = (message[i]+1) % 2
        return message
            



def encode(message,G):
    message = Matrix(message).transpose()
    encoded = G*message
    encoded = list(encoded.transpose())
    return list(encoded[0])

def decode(message,H):
    message = Matrix(message).transpose()
    decoded = H*message
    decoded = list(decoded.transpose())
    return list(decoded[0])





