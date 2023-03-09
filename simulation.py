from vpython import *
import math
import numpy


##CONSTANTS AND OBJECTS
theta_zero = (40.99*math.pi)/180
Sun        = sphere(radius = 6.95e9, pos=vector(0,0,0), mass=1.99e30,color = color.orange)
earth      = sphere(radius = 6.95e9, pos=vector(1.49e11,0,0), mass=5.97e24, v=vector(0,2.97e4,0), color = color.blue,make_trail=True)
eros       = sphere(radius = 6.95e9, pos=(2.81e11)*vector(cos(theta_zero), sin(theta_zero), 0), mass=7.2e15, v= (2.17e4)*vector(-sin(theta_zero),cos(theta_zero),0), color = color.red,make_trail=True)
spacecraft = sphere(radius = 6e9, pos=earth.pos, color=color.green,mass=100000, v=vector(0,3.408e4,0),make_trail=True)



earth.p = earth.mass*earth.v
eros.p = eros.mass*eros.v
p = spacecraft.mass*spacecraft.v

G = 6.67e-11

t      = 0
dt     = 50
T      = 100000
stepper= 0
year   = 2000 + (364/365.25)
arrive = 2023.2667658929433
b=False

while year<10000:
    #rate(100)
    #Force on Earth and position update
    F = (G*Sun.mass*earth.mass)/(mag(earth.pos-Sun.pos)**2) *  norm(Sun.pos-earth.pos)
    
    earth.p = earth.p + F*dt
    earth.pos = earth.pos + (earth.p*dt)/earth.mass
    #spacecraft.pos = earth.pos
    #spacecraft.p = spacecraft.mass*((earth.p*dt)/earth.mass)
   
    
    #Force on eros and position update
    F = (G*Sun.mass*eros.mass)/(mag(eros.pos-Sun.pos)**2) *  norm(Sun.pos-eros.pos)
    
    eros.p = eros.p + F*dt
    eros.pos = eros.pos + (eros.p*dt)/eros.mass  
    
    F = (G*Sun.mass*spacecraft.mass)/(mag(spacecraft.pos-Sun.pos)**2) *  norm(Sun.pos-spacecraft.pos)
    p = p + F*dt
    spacecraft.pos = spacecraft.pos + (p*dt)/spacecraft.mass      
    
    t = t+dt
    stepper += 1
    if stepper==3385:
        year = year + (1/(365.25))
        stepper = 0
    
    
    theta = numpy.arccos(  (dot(earth.pos,eros.pos))  / (mag(earth.pos)*mag(eros.pos)) )
    
    #if eros.pos.y>0 and earth.pos.x>1.49e11:
        #print(t)
        #print(year)
        #break
    
    #if (year>arrive and b==False) or (   abs(  ((theta*180)/math.pi)  -40.99)   <1):
        #spacecraft.make_trail = True
        ##print(year)
        #b=True
        #theta = numpy.arccos(  (dot(earth.pos,eros.pos))  / (mag(earth.pos)*mag(eros.pos)) )
        ##print(theta)
        ##print( str((theta*180)/math.pi) + " degrees")
        
        
        
    #if b:
        #F = (G*Sun.mass*spacecraft.mass)/(mag(spacecraft.pos-Sun.pos)**2) *  norm(Sun.pos-spacecraft.pos)
        
        #spacecraft.p = spacecraft.p + F*dt
        #spacecraft.pos = spacecraft.pos + (spacecraft.p*dt/spacecraft.mass)
        
        
    
print(t)