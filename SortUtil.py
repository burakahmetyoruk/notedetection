
def  sortblobsbyx(b1, b2) :

        return b1[0] < b2[0]


def sortblobsbyy(b1, b2) :
    return b1[0] > b2[0] & b1[1] < b1[1]


def sortblobs(blobs, index, centerpointylist) :

    sortedList = list()

    blobSize = len(blobs)

    # If image has a one staff dont have to sort by y axis
    if(len(centerpointylist) == 0):
        return blobs
    for i in range(0,blobSize) :
            if(index == 0) :
                if(blobs[i][1] < centerpointylist[index]):
                    sortedList.append(blobs[i])

            elif(index >= 1  and index <= 5) :
                if(index < len(centerpointylist)) :
                    if((blobs[i][1] > centerpointylist[index - 1]) and (blobs[i][1] < centerpointylist[index])) :
                        sortedList.append(blobs[i])
                elif(blobs[i][1] > centerpointylist[index - 1]):
                    sortedList.append(blobs[i])
    return sortedList

def compare_slopes(a,b):
    return a[0] < b[0]

