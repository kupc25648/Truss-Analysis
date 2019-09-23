'''
==================================================================
Truss-Analysis : Analysis Part
Req. python,numpy,pandas,matplotlib
2019.09

Input Required
==================================================================
'''

'''
====================================================================
Import Part
====================================================================
'''

import numpy as np
from Input import *
from render import *


'''
====================================================================
Input Part
====================================================================
'''
'''
Load
1. Set Name
2. Set Load type (for Truss == 1)
3. Set size (fx,fy,fz,mx,my,mz) - righthand - y=vertical axis
'''
l1 = Load()
l1.set_name(1)
l1.set_type(1)
l1.set_size(0,-100,0,0,-100,0)

l2 = Load()
l2.set_name(2)
l2.set_type(1)
l2.set_size(0,0,-50,0,0,-50)

'''
Node
1. Set Name
2. Set Coord (x,y,z)  - righthand - y=vertical axis
3. Set Restrctions 0=No Restiction, 1=Restiction
4. Add Loads to nodes
'''
n1 = Node()
n1.set_name(1)
n1.set_coord(-6*12,0*12,8*12)
n1.set_res(1,1,1)

n2 = Node()
n2.set_name(2)
n2.set_coord(12*12,0*12,8*12)
n2.set_res(1,1,1)

n3 = Node()
n3.set_name(3)
n3.set_coord(6*12,0*12,-8*12)
n3.set_res(1,1,1)

n4 = Node()
n4.set_name(4)
n4.set_coord(-12*12,0*12,-8*12)
n4.set_res(1,1,1)

n5 = Node()
n5.set_name(5)
n5.set_coord(0*12,24*12,0*12)
n5.set_res(0,0,0)
n5.set_load(l1)
n5.set_load(l2)

'''
Element
1. Set Name
2. Set Node start and Node end
3. Set Load(No Load on Element for Truss)
4. Set Eleastic Modulus
5. Set Cross sectional Area
6. Set Moment of Inertia ( Not use in Truss)
'''
e1 = Element()
e1.set_name(1)
e1.set_nodes(n1,n5)
e1.set_em(10000)
e1.set_area(8.4)

e2 = Element()
e2.set_name(2)
e2.set_nodes(n2,n5)
e2.set_em(10000)
e2.set_area(8.4)

e3 = Element()
e3.set_name(3)
e3.set_nodes(n3,n5)
e3.set_em(10000)
e3.set_area(8.4)

e4 = Element()
e4.set_name(4)
e4.set_nodes(n4,n5)
e4.set_em(10000)
e4.set_area(8.4)

'''
Model
1.Add Loads
2.Add Moments
3.Add Nodes
4.Add Elements
5.Generate all matrix
'''
m1 = Model()

m1.add_load(l1)
m1.add_load(l2)

m1.add_node(n1)
m1.add_node(n2)
m1.add_node(n3)
m1.add_node(n4)
m1.add_node(n5)

m1.add_element(e1)
m1.add_element(e2)
m1.add_element(e3)
m1.add_element(e4)

m1.gen_all()

print('COORD {0}'.format(m1.coord))
print('________________')
print('MSUP {0}'.format(m1.msup))
print('________________')
print('EM {0}'.format(m1.em))
print('________________')
print('CP {0}'.format(m1.cp))
print('________________')
print('MPRP {0}'.format(m1.mprp))
print('________________')
print('JP {0}'.format(m1.jp))
print('________________')
print('PJ {0}'.format(m1.pj))
print('________________')
print('MP {0}'.format(m1.mp))
print('________________')
print('PM {0}'.format(m1.pm))
print('________________')
print('nDOF {0}'.format(m1.ndof))
print('________________')
print('Q_ALL {0}'.format(m1.Qall))
print('________________')
print('NSC {0}'.format(m1.nsc))
print('________________')
print('TNSC {0}'.format(m1.tnsc))
print('________________')
print('P_MATRIX {0}'.format(m1.p_matrix))
print('________________')
print('JLV {0}'.format(m1.jlv))
print('________________')
print('GLOBAL_K {0}'.format(m1.global_k))
print('________________')
print('SSM {0}'.format(m1.ssm))
print('________________')
print('________________')
print('D {0}'.format(m1.d))
print('________________')
print('v {0}'.format(m1.v))
print('________________')
print('u {0}'.format(m1.u))
print('________________')
print('q {0}'.format(m1.q))
print('________________')
print('f {0}'.format(m1.f))
print('________________')

plt.show()
