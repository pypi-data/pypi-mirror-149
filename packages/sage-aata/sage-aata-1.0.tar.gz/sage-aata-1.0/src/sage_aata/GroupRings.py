
def star(a, groupRing):
    element = list(a)
    newElement = groupRing(0)
    for group,ring in element:
        newElement = newElement + ring*groupRing(group.inverse())
    return newElement

def hat(C, groupRing):
    elements = list(C)
    element = groupRing(elements[0])
    for i in range(1,len(elements)):
        element = element + groupRing(elements[i])
    return element





