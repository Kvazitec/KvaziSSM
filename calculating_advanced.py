from kvaziSSM_GUI import *
from numbers_integration import lasttime

year = 2025
month = 4
day = 7
mod = 'Static'
vis = False
name_months = {31 : 'jan', 28 : 'feb_f', 29 : 'feb_t', 31 : 'mar', 30 : 'apr', 31 :'may', 30 : 'jun', 31 : 'jul', 31 : 'aug', 30 : 'sep', 31 : 'oct', 30 : 'nov', 31 : 'dec'}
months = {1 : 31, 21 : 29, 20 : 28, 3 : 31, 4 : 30, 5 : 31, 6 : 30, 7 : 31, 8 : 31, 9 : 30, 10 : 31, 11 : 30, 12 : 31}
class Body(object):
    def __init__(self, name, x, y, z, Vx, Vy, Vz, ax, ay, az, radius, mass):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.Vx = x
        self.Vy = y
        self.Vz = z
        self.ax = x
        self.ay = y
        self.az = z
        self.radius = radius
        self.mass = mass
for i in range(int(datasearch(file_name, 'General', 'NUM_BODIES'))):
    pos = [float(datasearch(file_name,f'Body_{i}', 'x')), float(datasearch(file_name,f'Body_{i}', 'y')), float(datasearch(file_name,f'Body_{i}', 'z'))]
    vel = [float(datasearch(file_name, f'Body_{i}', 'Vx')), float(datasearch(file_name, f'Body_{i}', 'Vy')), float(datasearch(file_name, f'Body_{i}', 'Vz'))]
    bodies.append(Body(datasearch(file_name, f'Body_{i}', 'name'), pos[0], pos[1], pos[2], vel[0], vel[1], vel[2], 0, 0, 0, datasearch(file_name, f'Body_{i}', 'radius'), float(datasearch(file_name, f'Body_{i}', 'mass'))))
def date(date, mod, speed, datestr):
    second = date[0:2]
    minute = date[4:6]
    hour = date[8:10]
    day = date[12:14]
    month = date[16:18]
    year = date[20:22]
    lasttime = time.time()
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
                datestr = f'{year}/{month}/{day}'
            else:
                if day > months[int('2' + str(int(vis)))]:
                    month = month + 1
                    day = 1
                datestr = f'{year}/{month}/{day}'
            if hour > 24:
                day = day + 1
            if minute > 60:
                hour = hour+1
            if second > 60:
                minute = minute + 1
            second = second + 1

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