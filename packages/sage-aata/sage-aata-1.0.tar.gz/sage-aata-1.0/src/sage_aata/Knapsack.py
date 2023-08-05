
import math


def gcd(a,b):

    # set the variable atemp to the maximum of the two numbers.
    # Note that we take the absolute value of each of the numbers,
    # as this does not change the gcd.
    atemp = max(abs(a),abs(b))

    # similar with btemp, but the minimum.
    btemp = min(abs(a),abs(b))

    # let a be the maximum of the two, and b be the minimum of the two,
    # where both are now positive, if they were not before
    a = atemp
    b = btemp

    # while b is non zero...
    while b > 0:
        # obtain the quotient of a/b...
        quotient = math.floor(a/b)
        # as well as the remainder of a/b...
        remainder = a % b
        # then, for the next step in the Euclidean Algorithm, set
        # a to be the current value of b, and set b to be the remainder
        # obtained from the previous step, continue this process untill
        # the remainder is zero.
        a = b
        b = remainder

    # return the quotient, as this will be the greatest common divisor.
    return a

def gcd_full(a: int,b: int):
    # store the original values of a and b into the
    # variables aOrig and bOrig, to be used at the end
    aOrig = a
    bOrig = b

    # let atemp be the maximum of the absolute values of a and b
    # let btemp be the minimum
    atemp = max(abs(a),abs(b))
    btemp = min(abs(a),abs(b))

    # reassign the max value to be a and the minimum value to be b
    a = atemp
    b = btemp

    # create a list to hold all of the quotients, there is no need to
    # save all the remainders, as they are not used in the pseudocode
    # above
    quotients = []

    # same as before, go through and perform the steps of the Euclidean
    # algorithm, only this time, save all of the quotients into the list
    # that we just defined.
    while b > 0:
        quotient = math.floor(a/b)
        remainder = a % b
        a = b
        b = remainder
        quotients.append(quotient)

    # let d, be the value of the gcd
    d = a

    # throw the very last equation (the one with no remainder)
    # away, since we do not use it in the pseudocode above
    quotients.pop()

    # set x and y to their initial values
    x = 1
    y = -quotients.pop()

    # set the count equal to one, this will be used to alternate which one of x and y
    # we change in each step
    count = 0

    # follow the pseudocode above until there are no longer any quotients left
    while len(quotients)!=0:
        if count % 2 == 0:
            x = x-quotients.pop()*y
        if count % 2 == 1:
            y = y-quotients.pop()*x

        count = count + 1

    # this part is a little messy (sorry about that), but test to see which linear
    # combination of the original values of a and b give us the gcd, then
    # return those values
    if x*aOrig+y*bOrig==d:
        return [d,x,y]
    elif (-x)*aOrig+y*bOrig==d:
        return [d,-x,y]
    elif x*aOrig+(-y)*bOrig==d:
        return [d,x,-y]
    elif (-x)*aOrig+(-y)*bOrig==d:
        return [d,-x,-y]
    elif y*aOrig+x*bOrig==d:
        return [d,y,x]
    elif (-y)*aOrig+x*bOrig==d:
        return [d,-y,x]
    elif y*aOrig+(-x)*bOrig==d:
        return [d,y,-x]
    elif (-y)*aOrig+(-x)*bOrig==d:
        return [d,-y,-x]








def inverse_mod(a, b):
    nums = gcd_full(a,b)
    if (a*nums[1])%b == 1:
        return nums[1]%b
    else:
        return nums[2]%b


# In[ ]:


# import the random module, so we can generate random sequences
import random

# define the create_sequence() function, it will take in a positive integer
# that will be used as the size of the sequence.
def create_sequence(n: int):
    # create a list to hold the sequence.
    sequence = []
    # select a starting point randomly between 1 and 100000
    random_num = random.randint(1,100000)
    # add that number to the sequence
    sequence.append(random_num)
    # add numbers until we reach a length of i+1
    for i in range(0,n):
        # set the total equal to zero
        total = 0
        # calculate the sum of all the previous terms in the sequence
        for j in range(0,i+1):
            total = total + sequence[j]
        # select a random number that is bigger than that sum
        random_num = random.randint(total,total+10000)
        # and add it to the list
        sequence.append(random_num)
    # since we have one extra number in the list, take the last one and remove
    # it from the list, and multiply it by two, this will be our
    # modulus
    modulus = 2*sequence.pop()
    # return the sequence as a tuple, as well as the modulus
    return tuple(sequence), modulus



# In[ ]:


# this function takes in a positive integer m, and returns
# a number between m/2 and m that is relatively prime to m,
# as well as its inverse.
def get_multiplier(mod: int):
    # get some random number in the correct range.
    mult = random.randint(mod/2,mod)
    # if it is not relatively prime to mod, then try again
    # until we get a good number
    while gcd(mult,mod)!=1:
        mult = random.randint(mod/2,mod)
    # return the number, as well as its multiplicative
    # inverse
    return mult, inverse_mod(mult,mod)


# In[ ]:


# define the method that will create the public sequence,
# this function takes in the private sequence, the multiplier,
# as well as the modulus.
def create_public_sequence(seq: list, a: int, m: int):
    # create a list to hold the public sequence
    public_sequence = []
    # for each number in the private sequence, calculate
    # the new number for the public sequence, and add it to the list
    for i in range(0,len(seq)):
        public_sequence.append( (a*seq[i]) % m)
    # return the new sequence as a tuple.
    return tuple(public_sequence)


# Here we define the `pad_message()` and `depad_message()` functions.  These are not meant to be used by the user,
# but are called by the encrypt and decrypt functions, respectively.  Like I mentioned earlier, to encode each
# letter in the plaintext message, we use 8 bits of binary.  Do not change these functions.
# (Also disregard the fact that the letter *H* was missed when I typed this up the first time, and in laziness,
# it was just assigned the next number 188)

# In[ ]:


def pad_message(plaintext: str):
    ciphertext = ""
    for i in plaintext:
        if i == "a": ciphertext = ciphertext +"0"+ bin(97)[2:]
        if i == "b": ciphertext = ciphertext +"0"+ bin(98)[2:]
        if i == "c": ciphertext = ciphertext +"0"+ bin(99)[2:]
        if i == "d": ciphertext = ciphertext +"0"+ bin(100)[2:]
        if i == "e": ciphertext = ciphertext +"0"+ bin(101)[2:]
        if i == "f": ciphertext = ciphertext +"0"+ bin(102)[2:]
        if i == "g": ciphertext = ciphertext +"0"+ bin(103)[2:]
        if i == "h": ciphertext = ciphertext +"0"+ bin(104)[2:]
        if i == "i": ciphertext = ciphertext +"0"+ bin(105)[2:]
        if i == "j": ciphertext = ciphertext +"0"+ bin(106)[2:]
        if i == "k": ciphertext = ciphertext +"0"+ bin(107)[2:]
        if i == "l": ciphertext = ciphertext +"0"+ bin(108)[2:]
        if i == "m": ciphertext = ciphertext +"0"+ bin(109)[2:]
        if i == "n": ciphertext = ciphertext +"0"+ bin(110)[2:]
        if i == "o": ciphertext = ciphertext +"0"+ bin(111)[2:]
        if i == "p": ciphertext = ciphertext +"0"+ bin(112)[2:]
        if i == "q": ciphertext = ciphertext +"0"+ bin(113)[2:]
        if i == "r": ciphertext = ciphertext +"0"+ bin(114)[2:]
        if i == "s": ciphertext = ciphertext +"0"+ bin(115)[2:]
        if i == "t": ciphertext = ciphertext +"0"+ bin(116)[2:]
        if i == "u": ciphertext = ciphertext +"0"+ bin(117)[2:]
        if i == "v": ciphertext = ciphertext +"0"+ bin(118)[2:]
        if i == "w": ciphertext = ciphertext +"0"+ bin(119)[2:]
        if i == "x": ciphertext = ciphertext +"0"+ bin(120)[2:]
        if i == "y": ciphertext = ciphertext +"0"+ bin(121)[2:]
        if i == "z": ciphertext = ciphertext +"0"+ bin(122)[2:]
        if i == "A": ciphertext = ciphertext +"0"+ bin(123)[2:]
        if i == "B": ciphertext = ciphertext +"0"+ bin(124)[2:]
        if i == "C": ciphertext = ciphertext +"0"+ bin(125)[2:]
        if i == "D": ciphertext = ciphertext +"0"+ bin(126)[2:]
        if i == "E": ciphertext = ciphertext +"0"+ bin(127)[2:]
        if i == "F": ciphertext = ciphertext + bin(128)[2:]
        if i == "G": ciphertext = ciphertext + bin(129)[2:]
        if i == "H": ciphertext = ciphertext + bin(188)[2:]
        if i == "I": ciphertext = ciphertext + bin(130)[2:]
        if i == "J": ciphertext = ciphertext + bin(131)[2:]
        if i == "K": ciphertext = ciphertext + bin(132)[2:]
        if i == "L": ciphertext = ciphertext + bin(133)[2:]
        if i == "M": ciphertext = ciphertext + bin(134)[2:]
        if i == "N": ciphertext = ciphertext + bin(135)[2:]
        if i == "O": ciphertext = ciphertext + bin(136)[2:]
        if i == "P": ciphertext = ciphertext + bin(137)[2:]
        if i == "Q": ciphertext = ciphertext + bin(138)[2:]
        if i == "R": ciphertext = ciphertext + bin(139)[2:]
        if i == "S": ciphertext = ciphertext + bin(140)[2:]
        if i == "T": ciphertext = ciphertext + bin(141)[2:]
        if i == "U": ciphertext = ciphertext + bin(142)[2:]
        if i == "V": ciphertext = ciphertext + bin(143)[2:]
        if i == "W": ciphertext = ciphertext + bin(144)[2:]
        if i == "X": ciphertext = ciphertext + bin(145)[2:]
        if i == "Y": ciphertext = ciphertext + bin(146)[2:]
        if i == "Z": ciphertext = ciphertext + bin(147)[2:]
        if i == "1": ciphertext = ciphertext + bin(148)[2:]
        if i == "2": ciphertext = ciphertext + bin(149)[2:]
        if i == "3": ciphertext = ciphertext + bin(150)[2:]
        if i == "4": ciphertext = ciphertext + bin(151)[2:]
        if i == "5": ciphertext = ciphertext + bin(152)[2:]
        if i == "6": ciphertext = ciphertext + bin(153)[2:]
        if i == "7": ciphertext = ciphertext + bin(154)[2:]
        if i == "8": ciphertext = ciphertext + bin(155)[2:]
        if i == "9": ciphertext = ciphertext + bin(156)[2:]
        if i == "0": ciphertext = ciphertext + bin(157)[2:]
        if i == " ": ciphertext = ciphertext + bin(158)[2:]
        if i == '"': ciphertext = ciphertext + bin(159)[2:]
        if i == "'": ciphertext = ciphertext + bin(160)[2:]
        if i == "+": ciphertext = ciphertext + bin(161)[2:]
        if i == "-": ciphertext = ciphertext + bin(162)[2:]
        if i == "(": ciphertext = ciphertext + bin(163)[2:]
        if i == ")": ciphertext = ciphertext + bin(164)[2:]
        if i == "*": ciphertext = ciphertext + bin(165)[2:]
        if i == "&": ciphertext = ciphertext + bin(166)[2:]
        if i == "^": ciphertext = ciphertext + bin(167)[2:]
        if i == "%": ciphertext = ciphertext + bin(168)[2:]
        if i == "$": ciphertext = ciphertext + bin(169)[2:]
        if i == "#": ciphertext = ciphertext + bin(170)[2:]
        if i == "@": ciphertext = ciphertext + bin(171)[2:]
        if i == "!": ciphertext = ciphertext + bin(172)[2:]
        if i == "?": ciphertext = ciphertext + bin(173)[2:]
        if i == "/": ciphertext = ciphertext + bin(174)[2:]
        if i == "\\": ciphertext = ciphertext + bin(175)[2:]
        if i == ">": ciphertext = ciphertext + bin(176)[2:]
        if i == "<": ciphertext = ciphertext + bin(177)[2:]
        if i == ".": ciphertext = ciphertext + bin(178)[2:]
        if i == ",": ciphertext = ciphertext + bin(179)[2:]
        if i == "_": ciphertext = ciphertext + bin(180)[2:]
        if i == "=": ciphertext = ciphertext + bin(181)[2:]
        if i == "[": ciphertext = ciphertext + bin(182)[2:]
        if i == "]": ciphertext = ciphertext + bin(183)[2:]
        if i == "{": ciphertext = ciphertext + bin(184)[2:]
        if i == "}": ciphertext = ciphertext + bin(185)[2:]
        if i == "|": ciphertext = ciphertext + bin(186)[2:]
        if i == "~": ciphertext = ciphertext + bin(187)[2:]
    return ciphertext


# In[ ]:


def depad_message(ciphertext: str):
    plaintext = ""
    for i in range(0,len(ciphertext),8):
        if ciphertext[i:i+8] == "0"+bin(97)[2:]: plaintext = plaintext + "a"
        if ciphertext[i:i+8] == "0"+bin(98)[2:]: plaintext = plaintext + "b"
        if ciphertext[i:i+8] == "0"+bin(99)[2:]: plaintext = plaintext + "c"
        if ciphertext[i:i+8] == "0"+bin(100)[2:]: plaintext = plaintext + "d"
        if ciphertext[i:i+8] == "0"+bin(101)[2:]: plaintext = plaintext + "e"
        if ciphertext[i:i+8] == "0"+bin(102)[2:]: plaintext = plaintext + "f"
        if ciphertext[i:i+8] == "0"+bin(103)[2:]: plaintext = plaintext + "g"
        if ciphertext[i:i+8] == "0"+bin(104)[2:]: plaintext = plaintext + "h"
        if ciphertext[i:i+8] == "0"+bin(105)[2:]: plaintext = plaintext + "i"
        if ciphertext[i:i+8] == "0"+bin(106)[2:]: plaintext = plaintext + "j"
        if ciphertext[i:i+8] == "0"+bin(107)[2:]: plaintext = plaintext + "k"
        if ciphertext[i:i+8] == "0"+bin(108)[2:]: plaintext = plaintext + "l"
        if ciphertext[i:i+8] == "0"+bin(109)[2:]: plaintext = plaintext + "m"
        if ciphertext[i:i+8] == "0"+bin(110)[2:]: plaintext = plaintext + "n"
        if ciphertext[i:i+8] == "0"+bin(111)[2:]: plaintext = plaintext + "o"
        if ciphertext[i:i+8] == "0"+bin(112)[2:]: plaintext = plaintext + "p"
        if ciphertext[i:i+8] == "0"+bin(113)[2:]: plaintext = plaintext + "q"
        if ciphertext[i:i+8] == "0"+bin(114)[2:]: plaintext = plaintext + "r"
        if ciphertext[i:i+8] == "0"+bin(115)[2:]: plaintext = plaintext + "s"
        if ciphertext[i:i+8] == "0"+bin(116)[2:]: plaintext = plaintext + "t"
        if ciphertext[i:i+8] == "0"+bin(117)[2:]: plaintext = plaintext + "u"
        if ciphertext[i:i+8] == "0"+bin(118)[2:]: plaintext = plaintext + "v"
        if ciphertext[i:i+8] == "0"+bin(119)[2:]: plaintext = plaintext + "w"
        if ciphertext[i:i+8] == "0"+bin(120)[2:]: plaintext = plaintext + "x"
        if ciphertext[i:i+8] == "0"+bin(121)[2:]: plaintext = plaintext + "y"
        if ciphertext[i:i+8] == "0"+bin(122)[2:]: plaintext = plaintext + "z"
        if ciphertext[i:i+8] == "0"+bin(123)[2:]: plaintext = plaintext + "A"
        if ciphertext[i:i+8] == "0"+bin(124)[2:]: plaintext = plaintext + "B"
        if ciphertext[i:i+8] == "0"+bin(125)[2:]: plaintext = plaintext + "C"
        if ciphertext[i:i+8] == "0"+bin(126)[2:]: plaintext = plaintext + "D"
        if ciphertext[i:i+8] == "0"+bin(127)[2:]: plaintext = plaintext + "E"
        if ciphertext[i:i+8] == bin(128)[2:]: plaintext = plaintext + "F"
        if ciphertext[i:i+8] == bin(129)[2:]: plaintext = plaintext + "G"
        if ciphertext[i:i+8] == bin(130)[2:]: plaintext = plaintext + "I"
        if ciphertext[i:i+8] == bin(131)[2:]: plaintext = plaintext + "J"
        if ciphertext[i:i+8] == bin(132)[2:]: plaintext = plaintext + "K"
        if ciphertext[i:i+8] == bin(133)[2:]: plaintext = plaintext + "L"
        if ciphertext[i:i+8] == bin(134)[2:]: plaintext = plaintext + "M"
        if ciphertext[i:i+8] == bin(135)[2:]: plaintext = plaintext + "N"
        if ciphertext[i:i+8] == bin(136)[2:]: plaintext = plaintext + "O"
        if ciphertext[i:i+8] == bin(137)[2:]: plaintext = plaintext + "P"
        if ciphertext[i:i+8] == bin(138)[2:]: plaintext = plaintext + "Q"
        if ciphertext[i:i+8] == bin(139)[2:]: plaintext = plaintext + "R"
        if ciphertext[i:i+8] == bin(140)[2:]: plaintext = plaintext + "S"
        if ciphertext[i:i+8] == bin(141)[2:]: plaintext = plaintext + "T"
        if ciphertext[i:i+8] == bin(142)[2:]: plaintext = plaintext + "U"
        if ciphertext[i:i+8] == bin(143)[2:]: plaintext = plaintext + "V"
        if ciphertext[i:i+8] == bin(144)[2:]: plaintext = plaintext + "W"
        if ciphertext[i:i+8] == bin(145)[2:]: plaintext = plaintext + "X"
        if ciphertext[i:i+8] == bin(146)[2:]: plaintext = plaintext + "Y"
        if ciphertext[i:i+8] == bin(147)[2:]: plaintext = plaintext + "Z"
        if ciphertext[i:i+8] == bin(148)[2:]: plaintext = plaintext + "1"
        if ciphertext[i:i+8] == bin(149)[2:]: plaintext = plaintext + "2"
        if ciphertext[i:i+8] == bin(150)[2:]: plaintext = plaintext + "3"
        if ciphertext[i:i+8] == bin(151)[2:]: plaintext = plaintext + "4"
        if ciphertext[i:i+8] == bin(152)[2:]: plaintext = plaintext + "5"
        if ciphertext[i:i+8] == bin(153)[2:]: plaintext = plaintext + "6"
        if ciphertext[i:i+8] == bin(154)[2:]: plaintext = plaintext + "7"
        if ciphertext[i:i+8] == bin(155)[2:]: plaintext = plaintext + "8"
        if ciphertext[i:i+8] == bin(156)[2:]: plaintext = plaintext + "9"
        if ciphertext[i:i+8] == bin(157)[2:]: plaintext = plaintext + "0"
        if ciphertext[i:i+8] == bin(158)[2:]: plaintext = plaintext + " "
        if ciphertext[i:i+8] == bin(159)[2:]: plaintext = plaintext + '"'
        if ciphertext[i:i+8] == bin(160)[2:]: plaintext = plaintext + "'"
        if ciphertext[i:i+8] == bin(161)[2:]: plaintext = plaintext + "+"
        if ciphertext[i:i+8] == bin(162)[2:]: plaintext = plaintext + "-"
        if ciphertext[i:i+8] == bin(163)[2:]: plaintext = plaintext + "("
        if ciphertext[i:i+8] == bin(164)[2:]: plaintext = plaintext + ")"
        if ciphertext[i:i+8] == bin(165)[2:]: plaintext = plaintext + "*"
        if ciphertext[i:i+8] == bin(166)[2:]: plaintext = plaintext + "&"
        if ciphertext[i:i+8] == bin(167)[2:]: plaintext = plaintext + "^"
        if ciphertext[i:i+8] == bin(168)[2:]: plaintext = plaintext + "%"
        if ciphertext[i:i+8] == bin(169)[2:]: plaintext = plaintext + "$"
        if ciphertext[i:i+8] == bin(170)[2:]: plaintext = plaintext + "#"
        if ciphertext[i:i+8] == bin(171)[2:]: plaintext = plaintext + "@"
        if ciphertext[i:i+8] == bin(172)[2:]: plaintext = plaintext + "!"
        if ciphertext[i:i+8] == bin(173)[2:]: plaintext = plaintext + "?"
        if ciphertext[i:i+8] == bin(174)[2:]: plaintext = plaintext + "/"
        if ciphertext[i:i+8] == bin(175)[2:]: plaintext = plaintext + "\\"
        if ciphertext[i:i+8] == bin(176)[2:]: plaintext = plaintext + ">"
        if ciphertext[i:i+8] == bin(177)[2:]: plaintext = plaintext + "<"
        if ciphertext[i:i+8] == bin(178)[2:]: plaintext = plaintext + "."
        if ciphertext[i:i+8] == bin(179)[2:]: plaintext = plaintext + ","
        if ciphertext[i:i+8] == bin(180)[2:]: plaintext = plaintext + "_"
        if ciphertext[i:i+8] == bin(181)[2:]: plaintext = plaintext + "="
        if ciphertext[i:i+8] == bin(182)[2:]: plaintext = plaintext + "["
        if ciphertext[i:i+8] == bin(183)[2:]: plaintext = plaintext + "]"
        if ciphertext[i:i+8] == bin(184)[2:]: plaintext = plaintext + "{"
        if ciphertext[i:i+8] == bin(185)[2:]: plaintext = plaintext + "}"
        if ciphertext[i:i+8] == bin(186)[2:]: plaintext = plaintext + "|"
        if ciphertext[i:i+8] == bin(187)[2:]: plaintext = plaintext + "~"
        if ciphertext[i:i+8] == bin(188)[2:]: plaintext = plaintext + "H"
    return plaintext


# Here we define the `knapsack_solve()` function, which takes in a superincreasing sequence, as well as a
# number, and solves the knapsack problem.  Diclaimer: **This function does not check to make sure the
# sequence is superincreasing, nor does it check to ensure that the knapsack problem has a solution, it just
# goes through the algorithm as if these conditions are true.**

# In[ ]:


# takes in a sequence that is supposed to be superincreasing, as well
# as a number.
def knapsack_solve(seq: list, number: int):
    # define an empty string
    plaintext = ""
    # for each number in the sequence,
    for i in range(0,len(seq)):
        # if the number given is greater than the number in the sequence,
        if number >= seq[len(seq)-1-i]:
            # set the coefficient of that number to 1,
            plaintext = "1" + plaintext
            # and subtract that number from the number given.
            number = number - seq[len(seq)-1-i]
        # otherwise, set its coefficient to 0, and move on.
        else:
            plaintext = "0" + plaintext
    # return the solution to the knapsack problem.
    return plaintext


# In[ ]:


# function takes in a plaintext string, as well as the public sequence.
def knapsackEncrypt(plaintext: str, sequence: list):
    # encode the message
    plaintext = pad_message(plaintext)
    # define a new list for the ciphertext
    ciphertext = []
    # define a placeholder for each block of message.
    word = 0
    # for each number in the encoded message,
    for i in range(0,len(plaintext)):
        # if we have reached the end of the sequence, add the current value of
        # the word to the ciphertext list, and start over.
        # Note that on the first iteration of this for loop, while we will add a zero
        # to the ciphertext list, we will remove it later.
        if (i % len(sequence))== 0:
            ciphertext.append(word)
            word = 0
        # add the value of the plaintext times the sequence value to the word
        word = word + int(sequence[i % len(sequence)])*int(plaintext[i:i+1])
    # remove the first value of the ciphertext, since it is just zero.
    ciphertext.remove(0)
    # if there is anything left in word, add it to the list
    if word!=0:
        ciphertext.append(word)
    # return the ciphertext
    return ciphertext



# In[ ]:


# method takes in the ciphertext, the private sequence, the private multiplier
# as well as the private the modulus.
def knapsackDecrypt(ciphertext: list, seq: list, c: int, m: int):
    # define a new list for the plaintext
    plaintext = []
    # for each number in the ciphertext,
    for i in ciphertext:
        # multiply it by our private multiplier, and reduce mod m
        i = (c*i) % m
        # then, solve the knapsack problem with our private superincreasing
        # sequence.
        plaintext.append(knapsack_solve(seq,i))
    # define a new string
    plain = ""
    # add all of the solutions to the knapsack problem from the previous for loop
    # into one long string,
    for i in plaintext:
        plain = plain + str(i)
    # then, return the depaded message.
    return depad_message(plain)
    
