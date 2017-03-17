
import cv2 as cv
import numpy as np
import SortUtil as sort
from Util import dist
from NoteFinder import getNote
from ContourDetection import findContours
from Transform import four_point_transform
def main() :

    src = cv.imread('images/photo1.jpg',1)
    ret, thresh = cv.threshold(src, 120, 255, cv.THRESH_BINARY_INV)
    #Convert to Gray
    gray = cv.cvtColor(thresh, cv.COLOR_RGB2GRAY)
    #Find Edges
    edges = cv.Canny(thresh, 100, 200, apertureSize=3)
    #Find Contours
    screenCnt = findContours(edges)
    #If Image has a contour
    if screenCnt is not None:
        pts = np.array(screenCnt, dtype="float32")
        #cv.drawContours(src, [screenCnt], -1, (0, 255, 0), 3)
        #cv.imshow("Contours", src)
        warped = four_point_transform(src, pts)

        cv.imshow("warped",warped)
        cv.waitKey(0)
    else:
        #If image do not have any contour use original image
        warped = src

    #Re-Calculate After Transformation
    ret, thresh = cv.threshold(warped, 120, 255, cv.THRESH_BINARY_INV)
    # Convert to Gray
    gray = cv.cvtColor(thresh, cv.COLOR_RGB2GRAY)
    # Find Edges
    edges = cv.Canny(gray, 100, 200, apertureSize=3)




    #Line Detection
    pt1list = list()
    pt2list = list()
    linelist = list()
    lines = cv.HoughLines(edges, 1, np.pi / 180, 200)
    for x in range(0, len(lines)):
        for rho, theta in lines[x]:
            costheta = np.cos(theta)
            sintheta = np.sin(theta)
            x0 = costheta * rho
            y0 = sintheta * rho
            x1 = int(x0 + 1000 * -sintheta)
            y1 = int(y0 + 1000 * costheta)
            x2 = int(x0 - 1000 * -sintheta)
            y2 = int(y0 - 1000 * costheta)
            pt1list.append((x1, y1))
            pt2list.append((x2, y2))
            #Prevent divide by zero
            if(sintheta == 0):
                sintheta = 1
            linelist.append((rho / sintheta))
            cv.line(src, (x1, y1), (x2, y2), (0, 0, 255), 1)
    #End Line Detection

    kernel = np.ones((5, 5), np.uint8)
    erosion = cv.erode(thresh, kernel, iterations=1)
    dilate = cv.dilate(erosion, kernel, iterations=1)
    ret,thresh = cv.threshold(dilate,128,255,cv.THRESH_BINARY_INV)

    # Setup SimpleBlobDetector parameters.
    params = cv.SimpleBlobDetector_Params()
    # Filter by Area.
    params.filterByArea = True
    params.minArea = 30
    # Filter by Convexity
    params.filterByConvexity = True
    # Set up the detector with default parameters.
    detector = cv.SimpleBlobDetector_create(params)
    # Detect blobs.
    keypoints = detector.detect(thresh)

    blobs = list()
    for keypoint in keypoints:
            x = keypoint.pt[0]
            y = keypoint.pt[1]
            cv.circle(warped,(int(x), int(y)), 3, (0, 0, 255), 1)
            blobs.append((int(x),int(y)))
    # Show keypoints
    cv.imshow("After Blob Detection", warped)
    cv.waitKey(0)


    #Find staff count (each staff has a 5 line)
    count = int(len(lines) / 5)

    #Find point between staff
    centerpointylist = list()
    if count > 1 :
        index = 5
        for i in range(0,count -1 ):
            centerpointylist.append((linelist[index] + linelist[index - 1]) / 2)
            index += 5



    #Sort Blobs by x and y axis
    sortedblobs = list()
    distlist = list()
    notelist = list()
    lineindex = 0
    for i in range (0,count):
        sortedblobs = sort.sortblobs(blobs,i,centerpointylist)
        sortedblobs.sort(key=lambda tup: tup[0])
        for j in range(0,len(sortedblobs)):
                for z in range(lineindex,lineindex + 5):
                    distance = dist(sortedblobs[j][0],sortedblobs[j][1],pt1list[z][0],pt1list[z][1],pt2list[z][0],pt2list[z][1])
                    distlist.append(distance)
                mindistance = min(distlist)
                indexofmin = distlist.index(mindistance)
                #Find appropriate music note
                note = getNote(indexofmin,mindistance)
                notelist.append(note)
                distlist = list()
        lineindex+=5

    print notelist

if __name__ == '__main__':
    main()

