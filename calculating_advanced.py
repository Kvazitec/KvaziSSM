from kvaziSSM_GUI import *
import threading
from numpy import array
from math import sqrt
from kvazi_dts import datasearch
from time import time
vis = False
bodies = []
file_name = 'info.txt'
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
for i in range(int(datasearch(file_name, 'General', 'NUM_BODIES'))):
    pos = [float(datasearch(file_name,f'Body_{i}', 'x')), float(datasearch(file_name,f'Body_{i}', 'y')), float(datasearch(file_name,f'Body_{i}', 'z'))]
    vel = [float(datasearch(file_name, f'Body_{i}', 'Vx')), float(datasearch(file_name, f'Body_{i}', 'Vy')), float(datasearch(file_name, f'Body_{i}', 'Vz'))]
    bodies.append(Body(datasearch(file_name, f'Body_{i}', 'name'), pos[0], pos[1], pos[2], vel[0], vel[1], vel[2], 0, 0, 0, datasearch(file_name, f'Body_{i}', 'radius'), float(datasearch(file_name, f'Body_{i}', 'mass'))))
def date():
    global start_date
    global mcombo
    global CalcSpeed
    global now_date
    mod = mcombo.get()
    date = '00:00:00/01/01/2000'
    months = {1: 31, 21: 29, 20: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    second = date[0:2]
    minute = date[4:6]
    hour = date[8:10]
    day = date[12:14]
    month = date[16:18]
    year = date[20:22]
    lasttime = time.time()
    if mod == 'Расчёт координат для даты':
        speed = 3600*24*365*5
    while True:
        if time.time() - lasttime > 1/speed:
            if year % 4 != 0:
                vis = False
            elif year % 100 == 0:
                if year % 400 == 0:
                    vis = True
                else:
                    vis = False
            else:
                vis = True
            if month > 12:
                year = year + 1
                month = 1
            if month != 2:
                if day > months[month]:
                    month = month + 1
                    day = 1
            else:
                if day > months[int('2' + str(int(vis)))]:
                    month = month + 1
                    day = 1
            if hour > 24:
                day = day + 1
            if minute > 60:
                hour = hour+1
            if second > 60:
                minute = minute + 1
            second = second + 1
            now_date = f'{second}:{minute}:{hour}/{day}/{month}/{year}'
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
def integ_initiator():
    lasttime = time()
    while True:
        if time()-lasttime > 1:
            num_integr(3600)
            lasttime = time()
thrINTEGR = threading.Thread(target = integ_initiator)
thrINTEGR.start()
thrGUI = threading.Thread(target = managment_initiator(bodies))
thrGUI.start()
thrDAT = threading.Thread(target = date)
thrDAT.start()
"""while True:
    if year % 4 != 0:
        vis = False
    elif year % 100 == 0:
        if year % 400 == 0:
            vis = True
        else:
            vis = False
    else:
        vis = True
    if month > 12:
        year = year + 1
        month = 1
    if month != 2:
        if day > months[month]:
            month = month + 1
            day = 1
        datestr = f'{year}/{month}/{day}'
    else:
        if day > months[int('2'+str(int(vis)))]:
            month = month + 1
            day = 1
        datestr = f'{year}/{month}/{day}'
    Jup.compute(datestr, epoch='2000')
    day = day+1
    print(datestr)
    print(Jup.sun_distance)
    print(dms_deg(str(Jup.hlon)))
    print(dms_deg(str(Jup.hlat)))
    jup_polar_coords = SkyCoord(
        lon=dms_deg(str(Jup.hlon))*u.deg,  # долгота (например, эклиптическая)
        lat=dms_deg(str(Jup.hlat))*u.deg,  # широта
        distance=float(Jup.sun_distance)*u.AU,# расстояние от Солнца
        frame = 'heliocentrictrueecliptic'
    )
    print(datestr)
    jup_cartesian_coords = jup_polar_coords.cartesian
    print(jup_cartesian_coords.x, jup_cartesian_coords.y, jup_cartesian_coords.z)"""