"""
Solution of Assignment 3:
We create an AVL TREE i.e. a Balanced Binary Search Tree of points sorted by x coordinates(thus x coordinate is assigned to that node 
and the coord stores its coordinate) then with each node we attach  another AVL tree(sectree) with points which are the children of 
that node sorted according to the y coordinate( thus y coordinate  is assigned to it ). 
Then we search through the tree(x) and find the least common ancestor with the x value in range of the querypoint(x)+/-d then we go 
to the right(left) of this lca and search in the sectree those points in a similar way  whose ycoordinate also lie in the range of 
querypoint(y)+/-d .Then we store all these points and return them .


"""

class PointDatabase: # PointDatabase class to store the data points
    class point:# node in the AVL tree
        def __init__(self, coord): #initiator 
            self.coord = coord      #assigns coordinate
            self.value=coord[0]     #assigns value according to which tree the node belongs
            self.left = None        #left child
            self.right = None       #right child
            self.sectree = None     #Attaching the second AVL tree
            self.leaf = 0           #0==not a leaf; 1==is a leaf
   
    def Maketree(self,list,switch=1):#Constructing the tree , switch parameter tells us whether the tree of y coordinates is to be 
        #constructed or xcoordinates one
        l=len(list)
        if l==0:
            return None
        if l== 1:
            pointer = self.point(list[0])
            if switch==0:#assigning value according to which tree the node belongs (0 for ycoordinate tree)
                pointer.value=pointer.coord[1]
            pointer.leaf = 1
        else:
            median = l//2
            pointer = self.point(list[median]) 
            if switch==0:#assigning value according to which tree the node belongs (0 for ycoordinate tree)
                pointer.value=pointer.coord[1]
            pointer.left = self.Maketree(list[:median], switch)
            pointer.right = self.Maketree(list[median+1:], switch)
        if switch==1:
            pointer.sectree = self.Maketree( sorted(list, key=lambda coordinatey: coordinatey[1]), switch=0)
            #setting switch to 0 for making it a tree of ycoordinates 
        return pointer
    def liesin(self,point,interval,cond):
        # Function to check whether the point's coordinates lie in the given range . It can check in two ways-1)only y 2)both X,Y
        if cond == 1:#condition 1 when only y coordinates have to be checked
            ycoord = point
            if (ycoord >= interval[0][0]  and ycoord <= interval[0][1] ) :
                return 1
            else:
                return 0
        elif cond == 2:#condition 2 when both coordinates have to be checked
            xcoord = point[0]
            ycoord = point[1]

            if (xcoord >= interval[0][0]   and  xcoord <= interval[0][1]  and ycoord >= interval[1][0]  and  ycoord <= interval[1][1] ) :
                return 1
            else:
                return 0
    def leastcomanc(self,root,low,high):#Function to find the least common ancestor of the points which lies in the given range
        lca = root
        while lca != None:
            node = lca.value
            if high < node:
                lca = lca.left
            elif low > node:
                lca = lca.right
            elif low <= node <= high :
                break
        return lca
    def findy (self,tree, high, low):
        #Function to search for eligible points in the second tree whose y coordinates as well satisfy the criteria
        foundx = []
        lca = self.leastcomanc(tree , high, low)
        if lca == None:
            return foundx
        elif self.liesin( lca.coord[1] , [(high, low)], 1) :
            foundx.append(lca.coord)
        foundx += self.findy(lca.left, high, low)
        foundx += self.findy(lca.right, high, low)
        return foundx
    def findx(self,bbst,xlow,xhigh,ylow,yhigh):#To search those points whose x points lie in range
        foundx = []
        lca = self.leastcomanc(bbst,xlow,xhigh)
        if (lca == None):
            return foundx
        elif self.liesin(lca.coord, [( xlow,xhigh), (ylow,yhigh)], 2) :
            foundx.append(lca.coord)
        lcal = lca.left 
        while ( lcal != None ):
            if self.liesin(lcal.coord, [( xlow,xhigh), (ylow,yhigh)], 2):
                foundx.append(lcal.coord)
            if (xlow <= lcal.coord[0]):
                if lcal.right != None:
                    foundx += self.findy(lcal.right.sectree,ylow,yhigh)
                lcal = lcal.left
            else:
                lcal = lcal.right
        lcar = lca.right
        while ( lcar != None ):
            if self.liesin(lcar.coord, [(xlow, xhigh), (ylow,yhigh)], 2):
                    foundx.append(lcar.coord)
            if ( xhigh >= lcar.coord[0] ):
                if lcar.left != None:
                    foundx += self.findy(lcar.left.sectree, ylow,yhigh)
                lcar = lcar.right
            else:
                    lcar = lcar.left
        return foundx
    def __init__ (self, pointlist):
        #A constructor which creates an object of PointDatabase from a given pointlist of pairs of numbers
        value=sorted(pointlist)
        self.bbst = self.Maketree(value)
    def searchNearby(self, q, d):
        #An accessor method which, given a point q and distance d, returns the list of all points, in the set that self represents, #
        #that are at ℓ∞-distance at most d from q (arranged in an arbitrary order)
        search=self.findx( self.bbst, q[0]-d,q[0]+d,q[1]-d,q[1]+d)
        return search
p=PointDatabase([(4, 20), (5, 47), (8, 35), (9, 8), (13, 38), (17, 45), (21, 24), (22, 50), (27, 25), (31, 22), (35, 23), (38, 2), (40, 28), (43, 26), (46, 5)])
#p=PointDatabase([(10, 59), (22, 30), (26, 56), (29, 50), (32, 72), (34, 26), (39, 70), (43, 55), (52, 94), (56, 93), (60, 47), (68, 52), (70, 80), (71, 85), (75, 98), (82, 65), (86, 7), (88, 78), (96, 49), (99, 96)])
#p=PointDatabase([(21, 24), (9, 8), (13, 38), (17, 45), (35, 23), (5, 47), (46, 5), (38, 2), (4, 20), (22, 50), (40, 28), (43, 26), (31, 22), (8, 35), (27, 25)])
print(sorted(p.searchNearby((23,19),32.4)))
print('search',sorted(p.searchNearby((18,69),69.5)))


#p=PointDatabase([(38, 26), (43, 24), (5, 25), (30, 2), (29, 7), (37, 16), (51, 15), (40, 23), (23, 20), (8, 49), (34, 45), (42, 12), (32, 39), (17, 19), (12, 4)] )
#print(p.searchNearby((75,10),5.2))
"""pointDbObject = PointDatabase([(1,6), (2,4), (3,7), (4,9), (5,1), (6,3), (7,8), (8,10),(9,2), (10,5)])
print(pointDbObject.searchNearby((5,5), 1),
pointDbObject.searchNearby((4,8), 2),
pointDbObject.searchNearby((10,2), 1.5))"""
