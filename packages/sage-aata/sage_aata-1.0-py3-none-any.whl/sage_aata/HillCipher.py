
# coding: utf-8

# # Hill Cipher

# Below is the code to implement the Hill Cipher, which is an example of a **polyalphabetic cryptosystem**, that is, it does
# not assign a single ciphertext letter to a single plaintext letter, but rather a ciphertext letter may represent more than
# one plaintext letter.  This example is from Judson's [Abstract Algebra](http://abstract.ups.edu/sage-aata.html) textbook,
# example 7.4.  The encryption is based on the matrix
# \begin{equation*}
# A=\left(\begin{array}{cc}
# 3 & 5 \\
# 1 & 2
# \end{array}\right)
# \end{equation*}
# and encryptes pairs of letters at a time, rather than one letter at a time.
#
# The digitize and alphabetize functions are rather similar to the ones found in the CeasarCipher document, the bigest change
# being that these pair the numbers up so as to form matrices for encryption and decryption.

# In[ ]:


def digitize(string):
    cipher_text = []
    holder = []
    for i in string:
        if i == 'A' or i == 'a': holder.append([0])
        if i == 'B' or i == 'b': holder.append([1])
        if i == 'C' or i == 'c': holder.append([2])
        if i == 'D' or i == 'd': holder.append([3])
        if i == 'E' or i == 'e': holder.append([4])
        if i == 'F' or i == 'f': holder.append([5])
        if i == 'G' or i == 'g': holder.append([6])
        if i == 'H' or i == 'h': holder.append([7])
        if i == 'I' or i == 'i': holder.append([8])
        if i == 'J' or i == 'j': holder.append([9])
        if i == 'K' or i == 'k': holder.append([10])
        if i == 'L' or i == 'l': holder.append([11])
        if i == 'M' or i == 'm': holder.append([12])
        if i == 'N' or i == 'n': holder.append([13])
        if i == 'O' or i == 'o': holder.append([14])
        if i == 'P' or i == 'p': holder.append([15])
        if i == 'Q' or i == 'q': holder.append([16])
        if i == 'R' or i == 'r': holder.append([17])
        if i == 'S' or i == 's': holder.append([18])
        if i == 'T' or i == 't': holder.append([19])
        if i == 'U' or i == 'u': holder.append([20])
        if i == 'V' or i == 'v': holder.append([21])
        if i == 'W' or i == 'w': holder.append([22])
        if i == 'X' or i == 'x': holder.append([23])
        if i == 'Y' or i == 'y': holder.append([24])
        if i == 'Z' or i == 'z': holder.append([25])
        if len(holder)==2:
            cipher_text.append(holder)
            holder = []
    if len(holder)==1:
        holder.append(23)
        cipher_text.append(holder)
    return cipher_text








def alphabetize(digits):
    plain_text = ""
    for number in digits:
        for i in number:
            if i[0] == 0: plain_text = plain_text + "A"
            if i[0] == 1: plain_text = plain_text + "B"
            if i[0] == 2: plain_text = plain_text + "C"
            if i[0] == 3: plain_text = plain_text + "D"
            if i[0] == 4: plain_text = plain_text + "E"
            if i[0] == 5: plain_text = plain_text + "F"
            if i[0] == 6: plain_text = plain_text + "G"
            if i[0] == 7: plain_text = plain_text + "H"
            if i[0] == 8: plain_text = plain_text + "I"
            if i[0] == 9: plain_text = plain_text + "J"
            if i[0] == 10: plain_text = plain_text + "K"
            if i[0] == 11: plain_text = plain_text + "L"
            if i[0] == 12: plain_text = plain_text + "M"
            if i[0] == 13: plain_text = plain_text + "N"
            if i[0] == 14: plain_text = plain_text + "O"
            if i[0] == 15: plain_text = plain_text + "P"
            if i[0] == 16: plain_text = plain_text + "Q"
            if i[0] == 17: plain_text = plain_text + "R"
            if i[0] == 18: plain_text = plain_text + "S"
            if i[0] == 19: plain_text = plain_text + "T"
            if i[0] == 20: plain_text = plain_text + "U"
            if i[0] == 21: plain_text = plain_text + "V"
            if i[0] == 22: plain_text = plain_text + "W"
            if i[0] == 23: plain_text = plain_text + "X"
            if i[0] == 24: plain_text = plain_text + "Y"
            if i[0] == 25: plain_text = plain_text + "Z"
    return plain_text


# Here we define the HillEncrypt and HillDecrypt functions, which take in strings, and encrypt or decrypt them according
# to the matrices passed into them as parameters.

# In[ ]:


def HillEncrypt(message, A, b):
    encoded = digitize(message)
    cipher_text = []
    for item in encoded:
        cipher_text.append(matrixAdd(matrixMultiply(A,item),b))
    return alphabetize(cipher_text)

def HillDecrypt(message, A, b):
    A = A.inverse()
    encoded = digitize(message)
    plain_text = []
    for item in encoded:
        plain_text.append(matrixSubtract(matrixMultiply(A,item),matrixMultiply(A,b)))
    return alphabetize(plain_text)

def matrixMultiply(m1,m2):
    A = [[m1[0][0],m1[0][1]],[m1[1][0],m1[1][1]]]
    B = [[m2[0][0]],[m2[1][0]]]
    result = [[(A[0][0]*B[0][0]+A[0][1]*B[1][0]) % 26],[(A[1][0]*B[0][0]+A[1][1]*B[1][0]) % 26]]
    return result

def matrixSubtract(m1,m2):
    C = [[(m1[0][0]-m2[0][0]) % 26],[(m1[1][0]-m2[1][0]) % 26]]
    return C

def matrixAdd(m1,m2):
    C = [[(m1[0][0]+m2[0][0])%26],[(m1[1][0]+m2[1][0]) % 26]]
    return C
