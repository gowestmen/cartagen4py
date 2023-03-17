# this file define the Segment class, which representation a mathematical segment

from shapely.geometry import Point
from util import angle_operations
import math
import numpy as np

# get the list of segments of a linestring or a polygon
def get_segment_list(geometry):
    coords = []
    if(geometry.geom_type == 'LineString'):
        coords = geometry.coords
    elif(geometry.geom_type == 'Polygon'):
        coords = geometry.exterior.coords
    segment_list = []
    for i in range(1,len(coords)):
        segment_list.append(Segment(coords[i-1],coords[i]))
    return segment_list

class Segment:
    point1 = []
    point2 = []
    __coefA = 0
    __coefB = 0
    __coefC = 0

    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2
        self.__coefA = point2[1] - point1[1]
        self.__coefB = point1[0] - point2[0]
        self.__coefC = point1[1] * (point2[0]-point1[0]) + point1[0] * (point1[1] - point2[1])
    
    def get_coefA(self):
        return self.__coefA
    
    def get_coefB(self):
        return self.__coefB
    
    def get_coefC(self):
        return self.__coefC

    def orientation(self):
        xAxisPt = Point(self.point1[0] + 10.0, self.point1[1])
        return angle_operations.angle_3_pts(xAxisPt,Point(self.point1),Point(self.point2))
    
    def length(self):
        return math.sqrt((self.point2[0]-self.point1[0])*(self.point2[0]-self.point1[0]) + (self.point2[1]-self.point1[1])*(self.point2[1]-self.point1[1]))

    # compute the intersection point of two segments extended as straight lines
    def straight_line_intersection(self, segment2):
        matrix = np.zeros((2,2))
        matrix.itemset((0,0),self.__coefA)
        matrix.itemset((1,0),segment2.__coefA)
        matrix.itemset((0,1),self.__coefB)
        matrix.itemset((1,1),segment2.__coefB)

        # check if straight lines are parallel, i.e. matrix determinant is zero
        det = np.linalg.det(matrix)
        if (det==0.0):
            return None

        # inverse the matrix
        inverse = np.linalg.inv(matrix)

        x_intersection = - inverse.item(0,0)*self.__coefC - inverse.item(0,1)*segment2.__coefC
        y_intersection = - inverse.item(1,0)*self.__coefC - inverse.item(1,1)*segment2.__coefC

        return Point(x_intersection, y_intersection)
    
if __name__ == '__main__':
    segment1 = Segment((0,0),(10,0))
    segment2 = Segment((5,-5),(5,5))
    segment3 = Segment((0,0),(6,6))

    print(segment1.length())
    print(segment1.orientation())
    print(segment2.length())
    print(segment2.orientation())
    print(segment3.length())
    print(segment3.orientation())
    print(segment1.straight_line_intersection(segment2))