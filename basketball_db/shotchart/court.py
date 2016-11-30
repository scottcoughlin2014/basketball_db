from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def bball_court_half():

    ang_1=np.arange(0,np.pi,0.00001)
    ang_2=np.arange(np.pi,2*np.pi,0.00001)

    # Court Lines
    plt.plot([0,50],[0,0],'k',linewidth=1)
    plt.plot([0,50],[47,47],'k',linewidth=1)
    plt.plot([0,0],[0,47],'k',linewidth=1)
    plt.plot([50,50],[0,47],'k',linewidth=1)
    plt.plot([17,17],[0,19],'k',linewidth=1)
    plt.plot([33,33],[0,19],'k',linewidth=1)
    plt.plot([19,19],[0,19],'k',linewidth=1)
    plt.plot([31,31],[0,19],'k',linewidth=1)
    plt.plot([17,33],[19,19],'k',linewidth=1)
    plt.plot([17,33],[19,19],'k',linewidth=1)
    plt.plot([22,28],[4,4],'k',linewidth=1)

    plt.plot([3,3],[0,14],'k',linewidth=1)
    plt.plot([47,47],[0,14],'k',linewidth=1)

    # Hoop
    h = plt.plot(25+(9.0/12)*np.cos(ang_1),(4 + 9.0/12)+(9.0/12)*np.sin(ang_1),linewidth=1,color='orange')
    h = plt.plot(25+(9.0/12)*np.cos(ang_2),(4 + 9.0/12)+(9.0/12)*np.sin(ang_2),linewidth=1,color='orange')

    # Arc
    plt.plot(25+6*np.cos(ang_1),19+6*np.sin(ang_1),'k',linewidth=1)
    plt.plot(25+6*np.cos(ang_2),19+6*np.sin(ang_2),'k--',linewidth=1)

    # 3-Point
    extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
#    extra = 0.401
    ang_3= np.arange(extra,np.pi-extra,0.00001)
    three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
    three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)
    plt.plot(three_pt_xs, three_pt_ys,'k',linewidth=1)
    ax = plt.gca()
    ax.set_xlim(0,50)
    ax.set_ylim(0,47)
    return ax

def bball_court_three(X,Y):
    # 3-Point
    extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
    ang_3= np.arange(extra,np.pi-extra,0.00001)
    three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
    three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)

    idx = np.argsort(three_pt_xs)
    three_pt_xs = three_pt_xs[idx]
    three_pt_ys = three_pt_ys[idx]

    xs = X.flatten()
    ys = Y.flatten()
    zs = np.zeros(xs.shape)

    ii = 0
    for x,y in zip(xs,ys):
        point = -1
        if x < three_pt_xs[0]:
            point = 3
        elif x > three_pt_xs[-1]:
            point = 3
        else:
            ythree = np.interp(x,three_pt_xs,three_pt_ys)
            if y < ythree:
                point = 2
            else:          
                point = 3
        zs[ii] = point
        ii = ii + 1
    points = zs.reshape(X.shape)
    return points

def bball_court_blocks(X,Y):
    types = ["0to3","3to16","16to3pt","3pt"] 

    # Hoop
    hoop=[25.0,4.0 + 9.0/12]

    # 3-Point
    extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
    ang_3= np.arange(extra,np.pi-extra,0.00001)
    three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
    three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)

    idx = np.argsort(three_pt_xs)
    three_pt_xs = three_pt_xs[idx]
    three_pt_ys = three_pt_ys[idx]

    xs = X.flatten()
    ys = Y.flatten()

    data = {}
    for type in types:
        data[type] = np.zeros(xs.shape)

    ii = 0
    for x,y in zip(xs,ys):
        if x < three_pt_xs[0]:
            data["3pt"][ii] = 1
        elif x > three_pt_xs[-1]:
            data["3pt"][ii] = 1
        else:
            ythree = np.interp(x,three_pt_xs,three_pt_ys)
            if y < ythree:
                dist = np.sqrt((x-hoop[0])**2 + (y-hoop[1])**2)
                if dist < 3:
                    data["0to3"][ii] = 1
                elif (dist >=3) and (dist < 16):
                    data["3to16"][ii] = 1
                elif dist >= 16:
                    data["16to3pt"][ii] = 1
            else:          
                data["3pt"][ii] = 1
        ii = ii + 1

    for type in types:
        data[type] = data[type].reshape(X.shape)

    return data

def bball_shot_points(xs,ys):
    # 3-Point
    extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
    ang_3= np.arange(extra,np.pi-extra,0.00001)
    three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
    three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)

    idx = np.argsort(three_pt_xs)
    three_pt_xs = three_pt_xs[idx]
    three_pt_ys = three_pt_ys[idx]

#    xs = X.flatten()
#    ys = Y.flatten()
    zs = np.zeros(xs.shape)

    ii = 0
    for x,y in zip(xs,ys):
        point = -1
        if x < three_pt_xs[0]:
            point = 3
        elif x > three_pt_xs[-1]:
            point = 3
        else:
            ythree = np.interp(x,three_pt_xs,three_pt_ys)
            if y < ythree:
                point = 2
            else:          
                point = 3
        zs[ii] = point
        ii = ii + 1
    return zs

def bball_court_blocks(X,Y):
    types = ["0to3","3to16","16to3pt","3pt"] 

    # Hoop
    hoop=[25.0,4.0 + 9.0/12]

    # 3-Point
    extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
    ang_3= np.arange(extra,np.pi-extra,0.00001)
    three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
    three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)

    idx = np.argsort(three_pt_xs)
    three_pt_xs = three_pt_xs[idx]
    three_pt_ys = three_pt_ys[idx]

    xs = X.flatten()
    ys = Y.flatten()

    data = {}
    for type in types:
        data[type] = np.zeros(xs.shape)

    ii = 0
    for x,y in zip(xs,ys):
        if x < three_pt_xs[0]:
            data["3pt"][ii] = 1
        elif x > three_pt_xs[-1]:
            data["3pt"][ii] = 1
        else:
            ythree = np.interp(x,three_pt_xs,three_pt_ys)
            if y < ythree:
                dist = np.sqrt((x-hoop[0])**2 + (y-hoop[1])**2)
                if dist < 3:
                    data["0to3"][ii] = 1
                elif (dist >=3) and (dist < 16):
                    data["3to16"][ii] = 1
                elif dist >= 16:
                    data["16to3pt"][ii] = 1
            else:          
                data["3pt"][ii] = 1
        ii = ii + 1

    for type in types:
        data[type] = data[type].reshape(X.shape)

    return data
