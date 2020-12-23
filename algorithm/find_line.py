import random as rd
import math
import numpy as np

def find_critical_points(img, imgSize):
    a1, a2, b1, b2, c1, c2, d1, d2 = -1, -1, -1, -1, -1, -1, -1, -1
    s = imgSize - 1
    for i in range(imgSize):
    	if img[i][0] == 255:
		    a1 = i
		    break
    for i in range(imgSize):
	    if img[s - i][0] == 255:
		    a2 = s - i
		    break
    for i in range(imgSize):
	    if img[i][s] == 255:
		    b1 = i		
		    break
    for i in range(imgSize):
	    if img[s - i][s] == 255:
		    b2 = s - i		
		    break
    for i in range(imgSize):
    	if img[0][i] == 255:
		    c1 = i		
		    break
    for i in range(imgSize):
	    if img[0][s - i] == 255:
		    c2 = s - i		
		    break
    for i in range(imgSize):
	    if img[s][i] == 255:
		    d1 = i		
		    break
    for i in range(imgSize):
	    if img[s][s - i] == 255:
		    d2 = s - i		
		    break
    return float(a1), float(a2), float(b1), float(b2), float(c1), float(c2), float(d1), float(d2)


def cornerAC (critical_points, imgSize):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if a1 == 0.0 and c1 == 0.0:
	    return True
    else:
	    return False


def cornerBC (critical_points, imgSize):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if c2 == imgSize - 1 and b1 == 0:
	    return True
    else:
	    return False


def cornerAD (critical_points, imgSize):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if a2 == imgSize - 1 and d1 == 0:
	    return True
    else:
	    return False


def cornerBD (critical_points, imgSize):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if d2 == imgSize - 1 and b2 == imgSize - 1:
	    return True
    else:
	    return False


def borderA (critical_points):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if a1 == -1 and a2 == -1:
	    return False
    else:
	    return True


def borderB (critical_points):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if b1 == -1 and b2 == -1:
	    return False
    else:
	    return True


def borderC (critical_points):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if c1 == -1 and c2 == -1:
	    return False
    else:
	    return True


def borderD (critical_points):
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    if d1 == -1 and d2 == -1:
	    return False
    else:
	    return True


def linepoints (critical_points, imgSize, lineWidth): # lineWidth is determined by experiment
    p = critical_points
    a1, a2, b1, b2, c1, c2, d1, d2 = critical_points
    s = imgSize - 1
    w = lineWidth/2.0

	# 4
    if borderA(p) and borderB(p) and borderC(p) and borderD(p):
        if cornerAC(p, imgSize) and cornerBD(p, imgSize) and not cornerAD(p, imgSize) and not cornerBC(p, imgSize):
            return a1/2, c1/2, (s + b2)/2, (s + d2)/2
        elif not cornerAC(p, imgSize) and not cornerBD(p, imgSize) and cornerAD(p, imgSize) and cornerBC(p, imgSize):
            return b1/2, d1/2, (s + a2)/2, (s + c2)/2
        elif not cornerAC(p, imgSize) and cornerBD(p, imgSize) and cornerAD(p, imgSize) and cornerBC(p, imgSize):
            return b1, s, s, d1
        elif cornerAC(p, imgSize) and not cornerBD(p, imgSize) and cornerAD(p, imgSize) and cornerBC(p, imgSize):
            return 0, c2, a2, 0
        elif cornerAC(p, imgSize) and cornerBD(p, imgSize) and not cornerAD(p, imgSize) and cornerBC(p, imgSize):
            return 0, c1, b2, s 
        elif cornerAC(p, imgSize) and cornerBD(p, imgSize) and cornerAD(p, imgSize) and not cornerBC(p, imgSize):
            return a1, 0, s, d2
        else:
            return rd.randint(0, s), rd.randint(0, s), rd.randint(0, s), rd.randint(0, s)	

	# 3
    elif not borderA(p) and borderB(p) and borderC(p) and borderD(p):
        return 0, c1, s, d1
    elif borderA(p) and not borderB(p) and borderC(p) and borderD(p):
        return 0, c2, s, d2
    elif borderA(p) and borderB(p) and not borderC(p) and borderD(p):
        return a1, 0, b1, s
    elif borderA(p) and borderB(p) and borderC(p) and not borderD(p):
        return a2, 0, b2, s

	# 2
    elif not borderA(p) and not borderB(p) and borderC(p) and borderD(p):
        return 0, (c1 + c2)/2, s, (d1 + d2)/2
    elif borderA(p) and borderB(p) and not borderC(p) and not borderD(p):
        return (a1 + a2)/2, 0, (b1 + b2)/2, s
    elif borderA(p) and not borderB(p) and not borderC(p) and borderD(p):
        return (a1 + a2)/2, 0, s, (d1 + d2)/2
    elif not borderA(p) and borderB(p) and borderC(p) and not borderD(p):
        return 0, (c1 + c2)/2, (b1 + b2)/2, s
    elif borderA(p) and not borderB(p) and borderC(p) and not borderD(p):
        return 0, (c1 + c2)/2, (a1 + a2)/2, 0
    elif not borderA(p) and borderB(p) and not borderC(p) and borderD(p):
        return (b1 + b2)/2, s, s, (d1 + d2)/2

	# 1
    elif borderA(p) and not borderB(p) and not borderC(p) and not borderD(p):
        return a1, 0, a2, 0
    elif not borderA(p) and borderB(p) and not borderC(p) and not borderD(p):
        return b1, s, b2, s
    elif not borderA(p) and not borderB(p) and borderC(p) and not borderD(p):
        return 0, c1, 0, c2
    elif not borderA(p) and not borderB(p) and not borderC(p) and borderD(p):
        return s, d1, s, d2

	# 0
    else:
        return rd.randint(0, s), rd.randint(0, s), rd.randint(0, s), rd.randint(0, s)

def determine_direction(a, b, c, d, imgSize):
    fix = 16
    a = float(a)
    b = float(b)
    c = float(c)
    d = float(d)
    p = (imgSize-1)/2

    if a <= c:
        sign1 = 1
    else:
        sign1 = -1

    if (c-a)*p+(b-d)*(2*p-c)+d*(a-c) <= 0:
        sign2 = 1
    else:
        sign2 = -1

    direction_vector = sign1*np.array((b-d, c-a))*fix/math.sqrt((b-d)**2 + (c-a)**2)
    phase_vector = sign2*np.array((c-a,d-b))*abs((c-a)*p+(b-d)*(2*p-c)+d*(a-c))/((b-d)**2 + (c-a)**2)

    # Composition of the direction vector and phase vector
    v = direction_vector + phase_vector

    # Calculate direction
    cos = v[1]/math.sqrt(v[0]**2 + v[1]**2)
    if v[0] >= 0:
        sign3 = 1
    else:
        sign3 = -1
    theta = sign3*math.acos(cos)
    direction = 2*theta/math.pi
    return direction
