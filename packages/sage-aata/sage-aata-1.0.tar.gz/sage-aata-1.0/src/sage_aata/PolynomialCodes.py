# Here we create a method that generates an encoding message based on an encoding polynomial.  This can then be used 
# to encode messages with out computing the polynomials, although the notions are equivalent.

# In[1]:


def create_matrix(p,n,k):
    matrix = []
    for i in range(0,k):
        row = p*(x**i)
        row = list(row)
        while len(row)<n:
            row.append(0)
        matrix.append(list(row))
    return matrix

