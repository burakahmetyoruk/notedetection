


def getNote(line,dist) :

    if(line == 0) :
        if(dist <= 2):
            #Fa
            return 'F'
        else:
            #Sol
            return 'G'
    elif(line == 1):
        if(dist <= 2):
            #Re
            return 'D'
        else:
            #Mi
            return 'E'
    elif(line == 2):
        if(dist <=  2) :
            #Si
            return 'B'
        else:
            #La
            return 'A'
    elif(line == 3):
        if(dist <= 2):
            #Sol
            return 'G'
        else:
            #Fa
            return 'F'
    elif(line == 4) :
        if(dist < 2):
            #Mi
            return 'E'
        elif(dist == 4):
            #Fa
            return 'F'
        elif((dist > 1) and (dist <= 6)):
            #Re
            return 'D'
        elif(dist >= 8):
            #Do
            return 'C'
    else:
        return ''

