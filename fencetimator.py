#!/bin/python3

from math import pi
import numpy as np
import matplotlib.pyplot as plt

mu0=4*pi*1e-7 # T*m/A

class wire:
    def __init__(self,icurr,ax,ay):
        self.ax=ax
        self.ay=ay
        self.icurr=icurr
    def bwire(self,x,y):
        prefactor=mu0*self.icurr/(2*pi)/((x-self.ax)**2+(y-self.ay)**2)
        bwire_x=prefactor*(-(y-self.ay))
        bwire_y=prefactor*(x-self.ax)
        return bwire_x,bwire_y

class coil:
    def __init__(self):
        self.wires=[]
    def addwire(self,icurr,ax,ay):
        thiswire=wire(icurr,ax,ay)
        self.wires.append(thiswire)
    def bcoil(self,x,y):
        bx=np.zeros_like(x)
        by=np.zeros_like(x)
        for thiswire in self.wires:
            bxwire,bywire=thiswire.bwire(x,y)
            bx=bx+bxwire
            by=by+bywire
        return bx,by
# Wall are located at x=-c and x=+c

c=1.2 # m

ax=1.1 # m
ay=0 # m

icurr=.175 # A

ys=np.arange(-1000*icurr,1001*icurr,icurr)
mycoil=coil()
for y in ys:
    mycoil.addwire(icurr,ax,y)
    mycoil.addwire(-icurr,-ax,y)
#mycoil.addwire(icurr,ax,ay)

mirror=coil()
for order in range(10):
    for thiswire in mycoil.wires:
        ax=thiswire.ax
        ay=thiswire.ay
        icurr=thiswire.icurr
        if(order==0):
            x=(4*order+2)*c-ax
            mirror.addwire(icurr,x,ay)
        else:
            x=4*order*c+ax
            mirror.addwire(icurr,x,ay)
            x=4*(-order)*c+ax
            mirror.addwire(icurr,x,ay)            
            x=(4*order+2)*c-ax
            mirror.addwire(icurr,x,ay)
            x=(4*(-order)+2)*c-ax
            mirror.addwire(icurr,x,ay)

outer_roi=1.5 # m, for range of plot
x2d,y2d=np.mgrid[1.15:1.25:101j,-outer_roi:outer_roi:101j]
#x2d,y2d=np.mgrid[-outer_roi:outer_roi:101j,-outer_roi:outer_roi:101j]
bx2d,by2d=mycoil.bcoil(x2d,y2d)
bx2d_mirror,by2d_mirror=mirror.bcoil(x2d,y2d)
bx2d=bx2d#+bx2d_mirror
by2d=by2d#+by2d_mirror
bmod=np.sqrt(bx2d**2+by2d**2)

figouter,(axouter1,axouter2,axouter3)=plt.subplots(nrows=3)
plt.set_cmap('bwr')

vmin=-2e-8
vmax=+2e-8

#im=axouter1.pcolor(x2d,y2d,bx2d,vmin=vmin,vmax=vmax)
im=axouter1.pcolor(x2d,y2d,bx2d)
figouter.colorbar(im,ax=axouter1,format='%.3e',label="Tesla")
axouter1.set_xlabel("x (m)")
axouter1.set_ylabel("y (m)")
#axouter1.axvline(-c)
axouter1.axvline(+c)

#im=axouter2.pcolor(x2d,y2d,by2d,vmin=vmin,vmax=vmax)
im=axouter2.pcolor(x2d,y2d,by2d)
figouter.colorbar(im,ax=axouter2,format='%.3e',label="Tesla")
axouter2.set_xlabel("x (m)")
axouter2.set_ylabel("y (m)")
#axouter2.axvline(-c)
axouter2.axvline(+c)

#im=axouter3.pcolor(x2d,y2d,bmod,vmin=vmin,vmax=vmax)
im=axouter3.pcolor(x2d,y2d,bmod)
figouter.colorbar(im,ax=axouter3,format='%.3e',label="Tesla")
axouter3.set_xlabel("x (m)")
axouter3.set_ylabel("y (m)")
#axouter3.axvline(-c)
axouter3.axvline(+c)

bxcoil,bycoil=mycoil.bcoil(0,0)
bxmirror,bymirror=mirror.bcoil(0,0)
print(bxcoil,bycoil)
print(bxmirror,bymirror)

plt.show()

