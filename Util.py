
from Line import Line
import numpy as np

def dist(pct1X,pct1Y,pct2X,pct2Y,pct3X,pct3Y) :
    line = getline(pct2X, pct2Y, pct3X, pct3Y)
    return abs(line.getA() * pct1X + line.getB() * pct1Y + line.getC()) / np.sqrt(line.getA() * line.getA() + line.getB() * line.getB())


def getline(x1,y1,x2,y2) :

    line = Line(y2 - y1, x2 - x1, x1 * y2 - x2 * y1)
    return line
