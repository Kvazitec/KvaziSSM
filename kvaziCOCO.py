from math import sin, cos, radians
def ecl_to_cart(Beta,Lambda, R):
    cart = {0:'x', 0:'y', 0:'z'}
    Beta = radians(Beta)
    Lambda = radians(Lambda)
    R = radians(R)
    cart['x'] = R*cos(Beta)*cos(Lambda)
    cart['y'] = R*cos(Beta)*sin(Lambda)
    cart['z'] = R*cos(Beta)
    eql_incl =
    return cart
def equ_to_cart(Delta, Alpha, R):
    cart = {0: 'x', 0: 'y', 0: 'z'}
    Delta = radians(Delta)
    Alpha = radians(Alpha)
    R = radians(R)
    cart['x'] = R * cos(Delta) * cos(Alpha)
    cart['y'] = R * cos(Delta) * sin(Alpha)
    cart['z'] = R * cos(Delta)
    return cart
