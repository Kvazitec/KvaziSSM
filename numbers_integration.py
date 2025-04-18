from calculating_advanced import Body, bodies
from math import sqrt
from numpy import array
from kvaziSSM_GUI import datasearch
from time import time
G = float(datasearch('info.txt', 'General', 'GRAVITY_CONSTANT'))
def num_integr(dt):
    global bodies
    global Body
    for body1 in bodies:
        sumvec = array([0.0, 0.0, 0.0])
        for body2 in bodies:
            if body2 != body1:
                r = sqrt(((body1.x-body2.x)**2) + ((body1.y-body2.y)**2) + ((body1.z-body2.z)**2))
                force_abs = G*body1.mass*body2.mass/(r**2)
                k = force_abs/r
                vec = k * array([(body2.x-body1.x), (body2.y-body1.y), (body2.z-body1.z)])
                sumvec += vec
        body1.ax = sumvec[0] / body1.mass
        body1.ay = sumvec[1] / body1.mass
        body1.az = sumvec[2] / body1.mass
    for body in bodies:
        body.x += body.Vx * dt + (body.ax * (dt ** 2) / 2)
        body.y += body.Vy * dt + (body.ay * (dt ** 2) / 2)
        body.z += body.Vz * dt + (body.az * (dt ** 2) / 2)
        body.Vx += body.ax * dt
        body.Vy += body.ay * dt
        body.Vz += body.az * dt
lasttime = time()
while True:
    if time()-lasttime > 1:
        num_integr(3600)
        print(bodies[1].x)
        lasttime = time()
