from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def bball_court_half():

    ang_1=np.arange(0,np.pi,0.00001)
    ang_2=np.arange(np.pi,2*np.pi,0.00001)

    # Court Lines
    plt.plot([0,50],[0,0],'k',linewidth=3)
    plt.plot([0,50],[47,47],'k',linewidth=3)
    plt.plot([0,0],[0,47],'k',linewidth=3)
    plt.plot([50,50],[0,47],'k',linewidth=3)
    plt.plot([17,17],[0,19],'k',linewidth=3)
    plt.plot([33,33],[0,19],'k',linewidth=3)
    plt.plot([19,19],[0,19],'k',linewidth=3)
    plt.plot([31,31],[0,19],'k',linewidth=3)
    plt.plot([17,33],[19,19],'k',linewidth=3)
    plt.plot([17,33],[19,19],'k',linewidth=3)
    plt.plot([22,28],[4,4],'k',linewidth=3)

    plt.plot([3,3],[0,14],'k',linewidth=3)
    plt.plot([47,47],[0,14],'k',linewidth=3)

    # Hoop
    h = plt.plot(25+(9.0/12)*np.cos(ang_1),(4 + 9.0/12)+(9.0/12)*np.sin(ang_1),linewidth=1,color='orange')
    h = plt.plot(25+(9.0/12)*np.cos(ang_2),(4 + 9.0/12)+(9.0/12)*np.sin(ang_2),linewidth=1,color='orange')

    # Arc
    plt.plot(25+6*np.cos(ang_1),19+6*np.sin(ang_1),'k',linewidth=3)
    plt.plot(25+6*np.cos(ang_2),19+6*np.sin(ang_2),'k--',linewidth=3)

    # 3-Point
    extra =np.arcsin((14 - 4 - 9/12)/(23 + 9./12))
    print extra
#    extra = 0.401
    ang_3= np.arange(extra,np.pi-extra,0.00001)
    three_pt_xs = 25+(23 + 9/12)*np.cos(ang_3)
    three_pt_ys = (4 + 9/12)+(23 + 9/12)*np.sin(ang_3)
    print three_pt_ys
    print three_pt_xs
    plt.plot(three_pt_xs, three_pt_ys,'k',linewidth=3)
    ax = plt.gca()
    ax.set_xlim(0,50)
    ax.set_ylim(0,47)
    return ax
