'''
==================================================================
Truss-Analysis : Input Part
Req. python,numpy,pandas,matplotlib
2019.09

No Input Required
==================================================================
'''

'''
====================================================================
Import Part
====================================================================
'''

import numpy as np
import itertools

'''
Space Truss is subjected to axial force
1. Create Loads
2. Create Nodes
3. Set Loads for nodes
5. Create Element from node
6. Create Model
'''
class Load:
    def __init__(self):
        self.name = 1
        self.type = [0]
        #load type
            # 1 = perpendicular point load
            # 2 = perpendicular uniform distributed load
            # 3 = perpendicular triangular distributed load
            # 4 = perpendicular trapzodial distributed load
            # 5 = axial point load
            # 6 = axial uniform load
        self.size = [[0, 0,0], [0, 0,0],]  # size[0] =startloadsize(x,y,z coordinate) size[1] =endloadsize(x,y,z coordinate)

    def set_name(self, name):
        self.name = name
    def set_type(self,type):
        self.type[0] = type
    #Loads on [Element] must be set in Local coordinate
    def set_size(self, xstart, ystart,zstart, xend, yend,zend): #right&up  positive
        self.size[0][0] = xstart
        self.size[0][1] = ystart
        self.size[0][2] = zstart
        self.size[1][0] = xend
        self.size[1][1] = yend
        self.size[1][2] = zend

    def __repr__(self):
        return "{0}, {1},{2}".format(self.name, self.type, self.size)

#Not use here
class Moment:
    def __init__(self):
        self.name = 1
        self.size = [0]
        self.axis = [0]

    def set_name(self, name):
        self.name = name

    def set_size(self, size):
        self.size[0] = size
    # x-axis = 1
    # y-axis = 2
    # z-axis = 3
    def set_axis(self,axis):
        self.axis[0] = axis

    def __repr__(self):
        return "{0}, {1}".format(self.name, self.size)

class Node:
    def __init__(self):
        self.name = 1
        # coord[0]=xcoord,coord[1]=ycoord,coord[2]=zcoord
        self.coord = [0, 0, 0]
        # res[0]=x-restrain
        # res[1]=y-restrain
        # res[2]=z-restrain
        self.res = [0, 0, 0]
        self.loads = [] #[Load]s in this node
        self.moments = [] #[Moment]s in this node

    def set_name(self, name):
        self.name = name

    def set_coord(self, xval, yval, zval):
        self.coord[0] = xval
        self.coord[1] = yval
        self.coord[2] = zval

    def set_res(self, xres, yres, zres):
        self.res[0] = xres
        self.res[1] = yres
        self.res[2] = zres


    def set_load(self,load):
        self.loads.append([load])

    def set_moment(self,moment):
        self.moments.append([moment])

    def __repr__(self):
        return "{0}, {1},{2},{3},{4}".format(self.name, self.coord, self.res, self.loads, self.moments)

class Element(Node):
    def __init__(self):
        self.name = 1
        self.nodes = []  # nodes[0]=start node,nodes[1]=end node
        self.loads = []  # [load,distance_from_startnode,distance_from_endnode]self on member
        self.moments = []  # [moment,distance_from_startnode]s on member
        self.em = 0  # elastic modulus
        self.area = 0  # Sectional area
        self.i = 0 # moment of inertia

    def set_name(self, name):
        self.name = name
    def set_nodes(self, startnode, endnode):
        self.nodes.append(startnode)
        self.nodes.append(endnode)
    def set_em(self, emval):
        self.em = emval
    # Set sectional area
    def set_area(self, areaval):
        self.area = areaval
    # Set moment of inertia
    def set_i(self, ival):
        self.i = ival
    #Add loads
    #Loads must be set in Local coordinate
    def set_load(self,load,distance_from_startnode,distance_from_endnode):
        self.loads.append([load,distance_from_startnode,distance_from_endnode])
    #Add Moments
    def set_moment(self,moments,distance_from_startnode,distance_from_endnode):
        self.moments.append([moment,distance_from_startnode,distance_from_endnode])

    def __repr__(self):
        return "{0}, {1}, {2}, {3},{4},{5} ".format(self.name,self.nodes[0], self.nodes[1], self.em, self.area, self.i)

class Model():
    def __init__(self):
        self.nodes = []
        self.elements = []
        self.loads = []
        self.moments = []

        self.coord = []
        self.msup = []
        self.em = []
        #self.cp adjust from beam
        self.cp = []
        self.mprp = []
        self.jp = []
        #self.pj adjust from beam
        self.pj = []

        self.mp = []
        self.pm = []

        self.ndof = 0
        self.Qall = []
        self.nsc =[]
        self.tnsc=[]
        self.p_matrix=[]
        self.jlv=[]

        self.global_k=[]
        self.ssm =[]
        self.d =[]

        self.v =[]
        self.u =[]
        self.q =[]
        self.f =[]

    # add an load to model
    def add_load(self, load):
        self.loads.append(load)

    # add an moment to model
    def add_moment(self, moment):
        self.moments.append(moment)

    # add a node to model
    def add_node(self, node):
        self.nodes.append(node)

    # add an element to model
    def add_element(self, element):
        self.elements.append(element)

    # remove all node and element from model
    def reset(self):
        self.nodes = []
        self.elements = []

    # generate coord matrix-will be called my gen_all method
    # [node[x-coord,y-coord]]
    def gen_coord(self):
        for i in range(len(self.nodes)):
            self.coord.append(self.nodes[i].coord)

        return self.coord

    # generate msup matrix-will be called my gen_all method
    # msup contains Support Data Matrix [joint no., restrain in Y-axis, Rotation]
    def gen_msup(self):
        for i in range(len(self.nodes)):
            if (self.nodes[i].res[0] == 1) or (self.nodes[i].res[1] == 1) or (self.nodes[i].res[2] == 1):
                self.msup.append([self.nodes[i].name, self.nodes[i].res[0], self.nodes[i].res[1], self.nodes[i].res[2]])

        return self.msup

    # generate elastic modulus matrix-will be called my gen_all method
    def gen_em(self):
        x = []
        for i in range(len(self.elements)):
            x.append(self.elements[i].em)
        self.em = list(set(x))  # Remove duplicate elements a list by turn a list into a set and turn to a list again

        return self.em

    # generate cross sectional area matrix-will be called my gen_all method[Area, Moment of Inertia]
    def gen_cp(self):
        x=[]
        for i in range(len(self.elements)):
            x.append([self.elements[i].area,self.elements[i].i])
        x.sort()
        self.cp = list(x for x, _ in itertools.groupby(x))

        return self.cp

    # generate element matrix   -will be called my gen_all method
    def gen_mprp(self):
        for i in range(len(self.elements)):
            self.mprp.append([self.elements[i].nodes[0].name, self.elements[i].nodes[1].name])

        for i in range(len(self.elements)):
            for j in range(len(self.em)):
                if self.elements[i].em == self.em[j]:
                    self.mprp[i].append(j + 1)
        for i in range(len(self.elements)):
            for j in range(len(self.cp)):
                if (self.elements[i].area == self.cp[j][0]) and (self.elements[i].i == self.cp[j][1]):
                    self.mprp[i].append(j + 1)

        return self.mprp

    # generate support joint matrix-will be called my gen_all method
    def gen_jp(self):
        for i in range(len(self.nodes)):
            if len(self.nodes[i].loads) != 0:
                self.jp.append(self.nodes[i].name)
        for i in range(len(self.nodes)):
            if len(self.nodes[i].moments) != 0:
                self.jp.append(self.nodes[i].name)

        list(set(self.jp))

        return self.jp

    def gen_pj(self):
        for i in range(len(self.nodes)):
            if (len(self.nodes[i].loads) != 0) :

                sumX = 0
                sumY = 0
                sumZ = 0
                for j in range(len(self.nodes[i].loads)):
                    sumX += self.nodes[i].loads[j][0].size[0][0]
                    sumY += self.nodes[i].loads[j][0].size[0][1]
                    sumZ += self.nodes[i].loads[j][0].size[0][2]

                self.pj.append([sumX,sumY,sumZ])

        return self.pj

    def gen_mp(self):
        for i in range(len(self.elements)):
            if len(self.elements[i].loads) != 0:
                for j in range(len(self.elements[i].loads)):
                    self.mp.append([self.elements[i].name,self.elements[i].loads[j][0].type[0]])
            if len(self.elements[i].moments) != 0:
                for j in range(len(self.elements[i].moments)):
                    self.mp.append([self.elements[i].name,7])

        return self.mp

    #Check if input is ok
    def gen_pm(self):
        for i in range(len(self.elements)):
            if len(self.elements[i].loads) != 0:
                for j in range(len(self.elements[i].loads)):
                    #Load's Values
                    l1 = self.elements[i].loads[j][1]
                    l2 = self.elements[i].loads[j][2]
                     #load type
                    # 1 = perpendicular point load
                    # 2 = perpendicular uniform distributed load
                    # 3 = perpendicular triangular distributed load
                    # 4 = perpendicular trapzodial distributed load
                    # 5 = axial point load
                    # 6 = axial uniform load

                    #Case Load on X-Y [Local Coordinate] and Positive-Negative
                    ZeroX = ((self.elements[i].loads[j][0].size[0][0]==0) and (self.elements[i].loads[j][0].size[1][0]==0))
                    ZeroY = ((self.elements[i].loads[j][0].size[0][1]==0) and (self.elements[i].loads[j][0].size[1][1]==0))

                    YPos = ((ZeroX is True) and ((self.elements[i].loads[j][0].size[0][1]>0) or (self.elements[i].loads[j][0].size[1][1]>0)))
                    YNeg = ((ZeroX is True) and ((self.elements[i].loads[j][0].size[0][1]<0) or (self.elements[i].loads[j][0].size[1][1]<0)))
                    XPos = (((self.elements[i].loads[j][0].size[0][0]>0) or (self.elements[i].loads[j][0].size[1][0]>0)) and (ZeroY is True))
                    XNeg = (((self.elements[i].loads[j][0].size[0][0]<0) or (self.elements[i].loads[j][0].size[1][0]<0)) and (ZeroY is True))

                    #Case Point Load
                    if self.elements[i].loads[j][0].type[0] == 1:
                        #Case Load on Y and Negative
                        if (YPos is False) and (YNeg is True) and (XPos is False) and (XNeg is False):
                            w = self.elements[i].loads[j][0].size[0][1]
                            self.pm.append([-w, 0, l1,0])
                        #Case Load on Y and Positive
                        if (YPos is True) and (YNeg is False) and (XPos is False) and (XNeg is False):
                            w = self.elements[i].loads[j][0].size[0][1]
                            self.pm.append([w, 0, l1,0])
                        #No Case Load on X

                    #Case Uniform Distributed Load
                    if self.elements[i].loads[j][0].type[0] == 2:
                        #Case Load on Y and Negative
                        if (YPos is False) and (YNeg is True) and (XPos is False) and (XNeg is False):
                            w = self.elements[i].loads[j][0].size[0][1]
                            self.pm.append([-w, 0, l1,l2])
                        #Case Load on Y and Positive
                        if (YPos is True) and (YNeg is False) and (XPos is False) and (XNeg is False):
                            w = self.elements[i].loads[j][0].size[0][1]
                            self.pm.append([w, 0, l1,l2])
                        #No Case Load on X

                    #Case Triangular Load
                    if self.elements[i].loads[j][0].type[0] == 3:
                        #Case Load on Y and Negative
                        if (YPos is False) and (YNeg is True) and (XPos is False) and (XNeg is False):
                            w1 = self.elements[i].loads[j][0].size[0][1]
                            w2 = self.elements[i].loads[j][0].size[1][1]
                            self.pm.append([-w1, -w2, l1,l2])
                        #Case Load on Y and Positive
                        if (YPos is True) and (YNeg is False) and (XPos is False) and (XNeg is False):
                            w1 = self.elements[i].loads[j][0].size[0][1]
                            w2 = self.elements[i].loads[j][0].size[1][1]
                            self.pm.append([w1, w2, l1,l2])
                        #Case Load on X

                    #Case Trapzodial Load
                    if self.elements[i].loads[j][0].type[0] == 4:
                        #Case Load on Y and Negative
                        if (YPos is False) and (YNeg is True) and (XPos is False) and (XNeg is False):
                            w1 = self.elements[i].loads[j][0].size[0][1]
                            w2 = self.elements[i].loads[j][0].size[1][1]
                            self.pm.append([-w1, -w2, l1,l2])
                        #Case Load on Y and Positive
                        if (YPos is True) and (YNeg is False) and (XPos is False) and (XNeg is False):
                            w1 = self.elements[i].loads[j][0].size[0][1]
                            w2 = self.elements[i].loads[j][0].size[1][1]
                            self.pm.append([w1, w2, l1,l2])
                        #Case Load on X

                    #Case Axial Point Load
                    if self.elements[i].loads[j][0].type[0] == 5:
                        #No Case Load on Y
                        #Case Load on X and Negative
                        if (YPos is False) and (YNeg is False) and (XPos is False) and (XNeg is True):
                            w1 = self.elements[i].loads[j][0].size[0][0]
                            self.pm.append([-w1, 0, l1,0])
                        #Case Load on X and Positive
                        if (YPos is False) and (YNeg is False) and (XPos is True) and (XNeg is False):
                            w1 = self.elements[i].loads[j][0].size[0][0]
                            self.pm.append([w1, 0, l1,0])

                    #Case Axial Uniform load
                    if self.elements[i].loads[j][0].type[0] == 6:
                        #No Case Load on Y
                        #Case Load on X and Negative
                        if (YPos is False) and (YNeg is False) and (XPos is False) and (XNeg is True):
                            w1 = self.elements[i].loads[j][0].size[0][1]
                            self.pm.append([-w1, 0, l1,l2])
                        #Case Load on X and Positive
                        if (YPos is False) and (YNeg is False) and (XPos is True) and (XNeg is False):
                            w1 = self.elements[i].loads[j][0].size[0][1]
                            self.pm.append([w1, 0, l1,l2])
            #Case Moment
            if len(self.elements[i].moments) != 0:
                for j in range(len(self.elements[i].moments)):
                    M = self.elements[i].moments[j][0].size[0]
                    l1 = self.elements[i].moments[j][1]
                    #Case Point Moment
                    self.pm.append([M, 0, l1,0])
        return self.pm

    def gen_ndof(self):
        nr = 0
        for i in range(len(self.nodes)):
            for j in range(3):
                if self.nodes[i].res[j] == 1:
                    nr += 1
        self.ndof = 3 * (len(self.nodes)) - nr

        return self.ndof

    # generate structure coordinate number vector
    def gen_nsc(self):
        x=[]
        coord_num = 1
        for i in range(len(self.nodes)):
            for j in range(3):
                if self.nodes[i].res[j] == 0:
                    x.append(['R'])
                if self.nodes[i].res[j] == 1:
                    x.append(['UR'])
        for i in range(len(x)):
            if x[i][0] == 'R':
                x[i][0] = coord_num
                coord_num+=1
        for i in range(len(x)):
            if x[i][0] == 'UR':
                x[i][0] = coord_num
                coord_num+=1
        for i in range(len(x)):
            self.nsc.append(x[i])

        return self.nsc

    # transform nsc so that element in tnsc = joint
    def gen_tnsc(self):
        i = 0
        while i < len(self.nsc):
            self.tnsc.append([self.nsc[i][0], self.nsc[i + 1][0], self.nsc[i + 2][0]])
            i += 3
        return self.tnsc

    # generate joint loading vector matrix
    def gen_jlv(self):
        x=[]
        for i in range(len(self.tnsc)):
            x.append([0,0,0])

        for i in range(len(self.jp)):
            x[self.jp[i]-1] = self.pj[i]

        for i in range(len(self.tnsc)):
            for j in range(3):
                if self.tnsc[i][j] <= self.ndof:
                    self.jlv.append([x[i][j]])

        return self.jlv

    #generate global member stiffness matrix
    def gen_global_k(self):
        for i in range(len(self.elements)):

            #Dimensions
            XStartminEnd = self.elements[i].nodes[1].coord[0]-self.elements[i].nodes[0].coord[0]
            YStartminEnd = self.elements[i].nodes[1].coord[1]-self.elements[i].nodes[0].coord[1]
            ZStartminEnd = self.elements[i].nodes[1].coord[2]-self.elements[i].nodes[0].coord[2]

            L = ((XStartminEnd**2)+(YStartminEnd**2)+(ZStartminEnd**2))**0.5
            cosX = XStartminEnd/L
            cosY = YStartminEnd/L
            cosZ = ZStartminEnd/L
            #Values
            A = self.elements[i].area
            E = self.elements[i].em
            EApL = E*A/L
            # Local K
            a = EApL
            b = -EApL
            localk = np.array([[a,b],[b,a]])
            # Transformation Matrix
            Trow1 = [cosX,cosY,cosZ,  0 ,  0 ,  0 ]
            Trow2 = [  0 ,  0 ,  0 ,cosX,cosY,cosZ]
            T = np.array([Trow1,Trow2])
            # Transpose of Transformation Matrix
            Tt = T.transpose()
            k = Tt.dot(localk.dot(T))
            self.global_k.append(k.tolist())

        return self.global_k

    #generate structure stiffness matrix
    def gen_ssm(self):

        ttnsc = []
        for i in range(len(self.elements)):
            RowCol1 = self.tnsc[self.elements[i].nodes[0].name-1][0]
            RowCol2 = self.tnsc[self.elements[i].nodes[0].name-1][1]
            RowCol3 = self.tnsc[self.elements[i].nodes[0].name-1][2]
            RowCol4 = self.tnsc[self.elements[i].nodes[1].name-1][0]
            RowCol5 = self.tnsc[self.elements[i].nodes[1].name-1][1]
            RowCol6 = self.tnsc[self.elements[i].nodes[1].name-1][2]
            ttnsc.append([RowCol1,RowCol2,RowCol3,RowCol4,RowCol5,RowCol6])

        self.ssm = np.zeros((self.ndof,self.ndof))
        for i in range(len(self.elements)):
            for j in range(6):
                for k in range(6):
                    if (ttnsc[i][j] <= self.ndof) and (ttnsc[i][k] <= self.ndof):
                        self.ssm[ttnsc[i][j]-1][ttnsc[i][k]-1] += self.global_k[i][j][k]


        return self.ssm

    #Joint Displacement Matrix
    def gen_d(self):
        P = np.array(self.jlv)
        S = np.array(self.ssm)
        self.d = np.linalg.lstsq(S, P,rcond=-1)[0]

        return self.d

    def gen_v(self):
        ttnsc = []
        for i in range(len(self.elements)):
            RowCol1 = self.tnsc[self.elements[i].nodes[0].name-1][0]
            RowCol2 = self.tnsc[self.elements[i].nodes[0].name-1][1]
            RowCol3 = self.tnsc[self.elements[i].nodes[0].name-1][2]
            RowCol4 = self.tnsc[self.elements[i].nodes[1].name-1][0]
            RowCol5 = self.tnsc[self.elements[i].nodes[1].name-1][1]
            RowCol6 = self.tnsc[self.elements[i].nodes[1].name-1][2]
            ttnsc.append([RowCol1,RowCol2,RowCol3,RowCol4,RowCol5,RowCol6])

        for i in range(len(ttnsc)):
            zerov = [[0],[0],[0],[0],[0],[0]]
            for j in range(6):
                if ttnsc[i][j]<=self.ndof:
                    zerov[j][0] += round(float(self.d[ttnsc[i][j]-1]),5)
                else:
                    pass
            self.v.append(zerov)
        return self.v

    def gen_u(self):
        for i in range(len(self.elements)):
            #Dimensions
            XStartminEnd = self.elements[i].nodes[1].coord[0]-self.elements[i].nodes[0].coord[0]
            YStartminEnd = self.elements[i].nodes[1].coord[1]-self.elements[i].nodes[0].coord[1]
            ZStartminEnd = self.elements[i].nodes[1].coord[2]-self.elements[i].nodes[0].coord[2]

            L = ((XStartminEnd**2)+(YStartminEnd**2)+(ZStartminEnd**2))**0.5
            cosX = XStartminEnd/L
            cosY = YStartminEnd/L
            cosZ = ZStartminEnd/L

            # Transformation Matrix
            Trow1 = [cosX,cosY,cosZ,  0 ,  0 ,  0 ]
            Trow2 = [  0 ,  0 ,  0 ,cosX,cosY,cosZ]
            T = np.array([Trow1,Trow2])
            # u
            u = T.dot(self.v[i])
            self.u.append(u.tolist())

        return self.u

    def gen_q(self):
        for i in range(len(self.elements)):
            #Dimensions
            XStartminEnd = self.elements[i].nodes[1].coord[0]-self.elements[i].nodes[0].coord[0]
            YStartminEnd = self.elements[i].nodes[1].coord[1]-self.elements[i].nodes[0].coord[1]
            ZStartminEnd = self.elements[i].nodes[1].coord[2]-self.elements[i].nodes[0].coord[2]
            L = ((XStartminEnd**2)+(YStartminEnd**2)+(ZStartminEnd**2))**0.5

            #Values
            A = self.elements[i].area
            E = self.elements[i].em
            EApL = E*A/L
            # Local K
            a = EApL
            b = -EApL
            localk = np.array([[a,b],[b,a]])
            # q
            q = localk.dot(self.u[i])
            self.q.append(q.tolist())

        return self.q

    def gen_f(self):
        for i in range(len(self.elements)):

            #Dimensions
            XStartminEnd = self.elements[i].nodes[1].coord[0]-self.elements[i].nodes[0].coord[0]
            YStartminEnd = self.elements[i].nodes[1].coord[1]-self.elements[i].nodes[0].coord[1]
            ZStartminEnd = self.elements[i].nodes[1].coord[2]-self.elements[i].nodes[0].coord[2]
            L = ((XStartminEnd**2)+(YStartminEnd**2)+(ZStartminEnd**2))**0.5
            cosX = XStartminEnd/L
            cosY = YStartminEnd/L
            cosZ = ZStartminEnd/L
            # Transformation Matrix
            Trow1 = [cosX,cosY,cosZ,  0 ,  0 ,  0 ]
            Trow2 = [  0 ,  0 ,  0 ,cosX,cosY,cosZ]
            T = np.array([Trow1,Trow2])
            # Transpose of Transformation Matrix
            Tt = T.transpose()
            # f
            f = Tt.dot(self.q[i])
            self.f.append(f.tolist())

        return self.f




    # call every generate methods
    def gen_all(self):
        self.gen_coord()
        self.gen_msup()
        self.gen_em()
        self.gen_cp()
        self.gen_mprp()
        self.gen_jp()
        self.gen_pj()
        self.gen_mp()
        self.gen_pm()
        self.gen_ndof()
        self.gen_nsc()
        self.gen_tnsc()
        self.gen_jlv()
        self.gen_global_k()

        self.gen_ssm()
        self.gen_d()

        self.gen_v()
        self.gen_u()
        self.gen_q()
        self.gen_f()










