from symutils import *

C=CoordSys3D('C')
uvecs=[C.i,C.j,C.k]
coords=[C.x,C.y,C.z]

#evaluates a symbolic vector at a position and returns a numpy array
def evalsym(symvec,pos):
    numvec=np.zeros(3)
    numvec[0]=symvec.evalf(subs={C.x:pos[0],C.y:pos[1],C.z:pos[2]}).dot(C.i)
    numvec[1]=symvec.evalf(subs={C.x:pos[0],C.y:pos[1],C.z:pos[2]}).dot(C.j)
    numvec[2]=symvec.evalf(subs={C.x:pos[0],C.y:pos[1],C.z:pos[2]}).dot(C.k)
    return numvec

def lambdifyVector(symvec):
    symvec=symvec.subs([(C.x,x),(C.y,y),(C.z,z)])
    x_lam=lambdify((x,y,z),symvec.dot(C.i))
    y_lam=lambdify((x,y,z),symvec.dot(C.j))
    z_lam=lambdify((x,y,z),symvec.dot(C.k))
    return lambda xx,yy,zz:np.array([x_lam(xx,yy,zz),y_lam(xx,yy,zz),z_lam(xx,yy,zz)])

#computed the gradient of a vector (which is a dyad)
def nablavec(symvec):
    result=[[0,0,0] for i in range(0,3)]
    for i in range(0,3):
        for j in range(0,3):
            result[i][j]=diff(symvec.dot(uvecs[i]),coords[j])
    return result

#multiplies a dyad with a vector
def tensmul(tens,vec):
    comps=[]
    for i in range(0,3):
        comps.append(tens[i][0]*vec.dot(C.i)+tens[i][1]*vec.dot(C.j)+tens[i][2]*vec.dot(C.k))
    return comps[0]*C.i+comps[1]*C.j+comps[2]*C.k

#computes the euclidean norm of the vector
def norm(vec):
    return sym.sqrt(vec.dot(C.i)**2+vec.dot(C.j)**2+vec.dot(C.k)**2)