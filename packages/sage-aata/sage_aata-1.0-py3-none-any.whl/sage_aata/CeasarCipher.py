import math

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





def digitize(string):
    cipher_text = []
    for i in string:
        if i == 'A' or i == 'a': cipher_text.append(0)
        if i == 'B' or i == 'b': cipher_text.append(1)
        if i == 'C' or i == 'c': cipher_text.append(2)
        if i == 'D' or i == 'd': cipher_text.append(3)
        if i == 'E' or i == 'e': cipher_text.append(4)
        if i == 'F' or i == 'f': cipher_text.append(5)
        if i == 'G' or i == 'g': cipher_text.append(6)
        if i == 'H' or i == 'h': cipher_text.append(7)
        if i == 'I' or i == 'i': cipher_text.append(8)
        if i == 'J' or i == 'j': cipher_text.append(9)
        if i == 'K' or i == 'k': cipher_text.append(10)
        if i == 'L' or i == 'l': cipher_text.append(11)
        if i == 'M' or i == 'm': cipher_text.append(12)
        if i == 'N' or i == 'n': cipher_text.append(13)
        if i == 'O' or i == 'o': cipher_text.append(14)
        if i == 'P' or i == 'p': cipher_text.append(15)
        if i == 'Q' or i == 'q': cipher_text.append(16)
        if i == 'R' or i == 'r': cipher_text.append(17)
        if i == 'S' or i == 's': cipher_text.append(18)
        if i == 'T' or i == 't': cipher_text.append(19)
        if i == 'U' or i == 'u': cipher_text.append(20)
        if i == 'V' or i == 'v': cipher_text.append(21)
        if i == 'W' or i == 'w': cipher_text.append(22)
        if i == 'X' or i == 'x': cipher_text.append(23)
        if i == 'Y' or i == 'y': cipher_text.append(24)
        if i == 'Z' or i == 'z': cipher_text.append(25)
    return cipher_text



def alphabetize(digits):
    plain_text = ""
    for i in digits:
        if i == 0: plain_text = plain_text + "A"
        if i == 1: plain_text = plain_text + "B"
        if i == 2: plain_text = plain_text + "C"
        if i == 3: plain_text = plain_text + "D"
        if i == 4: plain_text = plain_text + "E"
        if i == 5: plain_text = plain_text + "F"
        if i == 6: plain_text = plain_text + "G"
        if i == 7: plain_text = plain_text + "H"
        if i == 8: plain_text = plain_text + "I"
        if i == 9: plain_text = plain_text + "J"
        if i == 10: plain_text = plain_text + "K"
        if i == 11: plain_text = plain_text + "L"
        if i == 12: plain_text = plain_text + "M"
        if i == 13: plain_text = plain_text + "N"
        if i == 14: plain_text = plain_text + "O"
        if i == 15: plain_text = plain_text + "P"
        if i == 16: plain_text = plain_text + "Q"
        if i == 17: plain_text = plain_text + "R"
        if i == 18: plain_text = plain_text + "S"
        if i == 19: plain_text = plain_text + "T"
        if i == 20: plain_text = plain_text + "U"
        if i == 21: plain_text = plain_text + "V"
        if i == 22: plain_text = plain_text + "W"
        if i == 23: plain_text = plain_text + "X"
        if i == 24: plain_text = plain_text + "Y"
        if i == 25: plain_text = plain_text + "Z"
    return plain_text




def CeasarEncrypt(plain_text, a, b):
    message = digitize(plain_text)
    for i in range(0,len(message)):
        message[i] = (a*message[i]+b) % 26
    return alphabetize(message)


def CeasarDecrypt(cipher_text, a, b):
    cipher_text = digitize(cipher_text)
    inverse = inverse_mod(a, 26)
    for i in range(0,len(cipher_text)):
        cipher_text[i] = (inverse*cipher_text[i]-inverse*b) % 26
    return alphabetize(cipher_text)
