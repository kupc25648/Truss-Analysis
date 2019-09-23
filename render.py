'''
==================================================================
Truss-Analysis : Render Part
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
import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from Analysis import *
fig = plt.figure().gca(projection='3d')
fig.set_xlabel('X axis')
fig.set_ylabel('Z axis')
fig.set_zlabel('Y axis')

'''
====================================================================
Initial Structure
====================================================================
'''

# NODES
Xcoord = []
Ycoord = []
Zcoord = []
for i in range(len(m1.nodes)):
    Xcoord.append(m1.nodes[i].coord[0])
    Zcoord.append(m1.nodes[i].coord[1])
    Ycoord.append(m1.nodes[i].coord[2])


Nodes = {'X':Xcoord, 'Y':Ycoord, 'Z':Zcoord}
nodeplot = pd.DataFrame(Nodes, columns = ['X','Y','Z'])
fignodeplot = fig.scatter(xs=nodeplot['X'],ys=nodeplot['Y'],zs=nodeplot['Z'],color ='black')

# ELEMENTS
for i in range(len(m1.elements)):
    xstart = m1.elements[i].nodes[0].coord[0]
    xend = m1.elements[i].nodes[1].coord[0]
    zstart = m1.elements[i].nodes[0].coord[1]
    zend = m1.elements[i].nodes[1].coord[1]
    ystart = m1.elements[i].nodes[0].coord[2]
    yend = m1.elements[i].nodes[1].coord[2]


    Xcoord = [xstart,xend]
    Zcoord = [zstart,zend]
    Ycoord = [ystart,yend]

    Elements = {'X':Xcoord, 'Y':Ycoord, 'Z':Zcoord}
    elementplot = pd.DataFrame(Elements, columns = ['X','Y','Z'])
    figelementplot = fig.plot(xs=elementplot['X'],ys=elementplot['Y'],zs=elementplot['Z'],color ='black')


# SUPPORT
#CASE 1 (m1.nodes[i].res[0] == 0) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 0)
Xcoord_Zres=[]
Zcoord_Zres=[]
Ycoord_Zres=[]
#CASE 2 (m1.nodes[i].res[0] == 1) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 0)
Xcoord_ZresXres=[]
Zcoord_ZresXres=[]
Ycoord_ZresXres=[]
#CASE 3 (m1.nodes[i].res[0] == 0) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 1)
Xcoord_ZresYres=[]
Zcoord_ZresYres=[]
Ycoord_ZresYres=[]
#CASE 4 (m1.nodes[i].res[0] == 1) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 1)
Xcoord_ZresXresYres=[]
Zcoord_ZresXresYres=[]
Ycoord_ZresXresYres=[]

for i in range(len(m1.nodes)):
    if (m1.nodes[i].res[0] == 0) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 0):
        Xcoord_Zres.append(m1.nodes[i].coord[0])
        Zcoord_Zres.append(m1.nodes[i].coord[1])
        Ycoord_Zres.append(m1.nodes[i].coord[2])

    if (m1.nodes[i].res[0] == 1) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 0):
        Xcoord_ZresXres.append(m1.nodes[i].coord[0])
        Zcoord_ZresXres.append(m1.nodes[i].coord[1])
        Ycoord_ZresXres.append(m1.nodes[i].coord[2])

    if (m1.nodes[i].res[0] == 0) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 1):
        Xcoord_ZresYres.append(m1.nodes[i].coord[0])
        Zcoord_ZresYres.append(m1.nodes[i].coord[1])
        Ycoord_ZresYres.append(m1.nodes[i].coord[2])

    if (m1.nodes[i].res[0] == 1) and (m1.nodes[i].res[1] == 1) and (m1.nodes[i].res[2] == 1):
        Xcoord_ZresXresYres.append(m1.nodes[i].coord[0])
        Zcoord_ZresXresYres.append(m1.nodes[i].coord[1])
        Ycoord_ZresXresYres.append(m1.nodes[i].coord[2])
    else:
        pass

if Xcoord_Zres != 0:
    Zres = {'X':Xcoord_Zres, 'Y':Ycoord_Zres, 'Z':Zcoord_Zres}
    Zresplot = pd.DataFrame(Zres, columns = ['X','Y','Z'])
    figZresplot = fig.scatter(xs=Zresplot['X'],ys=Zresplot['Y'],zs=Zresplot['Z'],color ='silver',marker="^",s=100)

if Xcoord_ZresXres != 0:
    ZresXres = {'X':Xcoord_ZresXres, 'Y':Ycoord_ZresXres, 'Z':Zcoord_ZresXres}
    ZresXresplot = pd.DataFrame(ZresXres, columns = ['X','Y','Z'])
    figZresXresplot = fig.scatter(xs=ZresXresplot['X'],ys=ZresXresplot['Y'],zs=ZresXresplot['Z'],color ='grey',marker="^",s=100)

if Xcoord_ZresYres != 0:
    ZresYres = {'X':Xcoord_ZresYres, 'Y':Ycoord_ZresYres, 'Z':Zcoord_ZresYres}
    ZresYresplot = pd.DataFrame(ZresYres, columns = ['X','Y','Z'])
    figZresYresplot = fig.scatter(xs=ZresYresplot['X'],ys=ZresYresplot['Y'],zs=ZresYresplot['Z'],color ='grey',marker="^",s=100)

if Xcoord_ZresXresYres != 0:
    ZresXresYres = {'X':Xcoord_ZresXresYres, 'Y':Ycoord_ZresXresYres, 'Z':Zcoord_ZresXresYres}
    ZresXresYresplot = pd.DataFrame(ZresXresYres, columns = ['X','Y','Z'])
    figZresXresYresplot = fig.scatter(xs=ZresXresYresplot['X'],ys=ZresXresYresplot['Y'],zs=ZresXresYresplot['Z'],color ='black',marker="^",s=100)
else:
    pass


'''
====================================================================
Deformed Structure
====================================================================
'''

# NODES
NewXcoord = []
NewYcoord = []
NewZcoord = []
for i in range(len(m1.nodes)):
    NewXcoord.append(m1.nodes[i].coord[0])
    NewZcoord.append(m1.nodes[i].coord[1])
    NewYcoord.append(m1.nodes[i].coord[2])
for i in range(len(m1.d)):
    for j in range(len(m1.tnsc)):
        if m1.tnsc[j][0] == i + 1:
            NewXcoord[j] += m1.d[i][0]
        if m1.tnsc[j][1] == i + 1:
            NewZcoord[j] += m1.d[i][0]
        if m1.tnsc[j][2] == i + 1:
            NewYcoord[j] += m1.d[i][0]
NewNodes = {'X':NewXcoord, 'Y':NewYcoord, 'Z':NewZcoord}
Newnodeplot = pd.DataFrame(NewNodes, columns = ['X', 'Y', 'Z'])
figNewnodeplot = fig.scatter(xs=Newnodeplot['X'],ys=Newnodeplot['Y'],zs=Newnodeplot['Z'],color ='red')
# ELEMENTS
for i in range(len(m1.elements)):
    Newxstart = m1.elements[i].nodes[0].coord[0]
    Newxend = m1.elements[i].nodes[1].coord[0]
    Newzstart = m1.elements[i].nodes[0].coord[1]
    Newzend = m1.elements[i].nodes[1].coord[1]
    Newystart = m1.elements[i].nodes[0].coord[2]
    Newyend = m1.elements[i].nodes[1].coord[2]

    for k in range(len(m1.d)):
        if m1.tnsc[m1.elements[i].nodes[0].name-1][0] == k + 1:
            Newxstart += m1.d[k][0]
        if m1.tnsc[m1.elements[i].nodes[1].name-1][0] == k + 1:
            Newxend += m1.d[k][0]
        if m1.tnsc[m1.elements[i].nodes[0].name-1][1] == k + 1:
            Newzstart += m1.d[k][0]
        if m1.tnsc[m1.elements[i].nodes[1].name-1][1] == k + 1:
            Newzend += m1.d[k][0]
        if m1.tnsc[m1.elements[i].nodes[0].name-1][2] == k + 1:
            Newystart += m1.d[k][0]
        if m1.tnsc[m1.elements[i].nodes[1].name-1][2] == k + 1:
            Newyend += m1.d[k][0]
        else:
            pass

    NewXcoord = [Newxstart,Newxend]
    NewZcoord = [Newzstart,Newzend]
    NewYcoord = [Newystart,Newyend]

    NewElements = {'X':NewXcoord, 'Y':NewYcoord, 'Z':NewZcoord}
    Newelementplot = pd.DataFrame(NewElements, columns = ['X','Y','Z'])
    figNewelementplot = fig.plot(xs=Newelementplot['X'],ys=Newelementplot['Y'],zs=Newelementplot['Z'],color ='red',alpha=0.7)

plt.axis('equal')
plt.show()

