import time

from numpy import array
from math import sqrt
from kvazi_dts import datasearch
from multiprocessing import Queue

start = False
vis = False
bodies = []
file_name = 'info.txt'
now_date = '00:00/12/04/2021'
speed = 1
ifstart = False
G = 0
i_save = 0
class Body(object):
    def __init__(self, name, x, y, z, Vx, Vy, Vz, ax, ay, az, radius, mass):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.Vx = Vx
        self.Vy = Vy
        self.Vz = Vz
        self.ax = ax
        self.ay = ay
        self.az = az
        self.radius = radius
        self.mass = mass
def downloader():
    global G
    global bodies
    global i_save
    bodies.clear()
    for i in range(int(datasearch(file_name, 'General', 'NUM_BODIES'))):
        pos = [float(datasearch(file_name, f'Body_{i}', 'x')), float(datasearch(file_name, f'Body_{i}', 'y')),
               float(datasearch(file_name, f'Body_{i}', 'z'))]
        vel = [float(datasearch(file_name, f'Body_{i}', 'Vx')), float(datasearch(file_name, f'Body_{i}', 'Vy')),
               float(datasearch(file_name, f'Body_{i}', 'Vz'))]
        bodies.append(Body(datasearch(file_name, f'Body_{i}', 'name'), pos[0], pos[1], pos[2], vel[0], vel[1], vel[2], 0, 0, 0,
                 float(datasearch(file_name, f'Body_{i}', 'radius')), float(datasearch(file_name, f'Body_{i}', 'mass'))))
        G = float(datasearch('info.txt', 'General', 'GRAVITY_CONSTANT'))
        i_save = i
downloader()
lasttime1 = time.time()
def num_integr(dt, qbod, qnewb, ifstart1):
    global bodies
    global Body
    global lasttime1
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
    bodies_data = [(body.name, body.x, body.y, body.z, body.Vx, body.Vy, body.Vz, body.ax, body.ay, body.az, body.radius,
                   body.mass) for body in bodies]
    if not ifstart1 or time.time() - lasttime1 > 0.03: #0.016:
        qbod.put(bodies_data)
        lasttime1 = time.time()
    #print(time.time()-lasttime1)