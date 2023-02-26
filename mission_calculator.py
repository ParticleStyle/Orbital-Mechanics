#Program which performs calculations for a mission to a celestial body
#Caleb Bessit
#15 October 2022

import math
from datetime import *
import numpy
from PyAstronomy import pyasl

def period(semi_major):
    return  toDays( ( (2*math.pi)  / math.sqrt(G*M_sun) )* math.sqrt(  (semi_major**3)  ))

def printResults():
    print("MISSION TO {:s}: SUMMARY".format(body_name.upper()))
    print()
    
    print("KNOWN FACTS ABOUT {:s}".format(body_name.upper()))
    print("{:50s}{:.3f} {:s}".format("Orbital period: ", T_body, "days" ))
    print("{:50s}{:.3f} {:s}".format("Angular speed of destination body: ",w_body, "radians per day" ))
    
    print()
    #Stage 1
    print("STAGE 1: LAUNCH TO GEOSTATIONARY ORBIT")
    print("{:50s}{:.3e} {:s}".format("Geostationary orbit radius: ", R_geo_stat," meters" ))
    print("{:50s}{:.3e} {:s}".format("Escape velocity: ", v_esc, " meters per second" ))
    
    #Stage 2
    print()
    print("STAGE 2: TRANSFER TO HOHMANN ORBIT")
    print("{:50s}{:.3e} {:s}".format("Speed of Hohmann orbit at launch point: ", v_launch, "meters per second" ))
    print("{:50s}{:.3e} {:s}".format("Current speed of spacecraft at launch point: ", v_current, "meters per second" ))
    
    if thrust_l:
        print("{:50s}{:.3e} {:s}".format("Thrust to be provided: ",v_thrust, "meters per second, forward thrust" ))
    else:
        print("{:50s}{:.3e} {:s}".format("Thrust to be provided: ",v_thrust, "meters per second, reverse thrust" ))
    
    #Stage 3
    print()
    print("STAGE 3: JOURNEY TO " + body_name.upper())

    print("{:50s}{:.3f} {:s}".format("Time of flight: ", toDays(T_flight), "days"))
    print("{:50s}{:.3f} {:s}".format("Synodic period: ",T_synodic, "days" ))
    print("{:50s}{:s}".format("Launch window date: ", dateString(launch_window) ))
    print("{:50s}{:s}".format("Arrival window date: ", dateString(arrive_date) ))
    
    #Stage 4
    print()
    print("STAGE 4: DROP DOWN INTO ORBIT ABOUT " + body_name.upper())
    
    print("{:50s}{:.3e} {:s}".format("Speed of Hohmann orbit at rendezvous point: ", v_rendezvous, "meters per second" ))
    print("{:50s}{:.3e} {:s}".format("Current speed of spacecraft at rendezvous point: ", v_current2, "meters per second" ))
    
    if thrust_r:
        print("{:50s}{:.3e} {:s}".format("Thrust to be provided: ",v_thrust2, "meters per second, forward thrust" ))
    else:
        print("{:50s}{:.3e} {:s}".format("Thrust to be provided: ",v_thrust2, "meters per second, reverse thrust" ))    
    
    #Stage 5
    print()
    print("STAGE 5: RETURN TO EARTH")
    print("{:50s}{:s}".format("Return launch window date: ", dateString(launch_windowR) ))
    print("{:50s}{:s}".format("Return window date: ", dateString(return_date) ))    
    
def toDegrees(radians):
    return (  (radians*180)/math.pi)

def toRadians(degrees):
    return ( (degrees*math.pi)/180  )

def toYears(days):
    return days/365.25

def toDays(seconds):
    return seconds/86400

def dateString(year):
    date_l = pyasl.decimalYearGregorianDate(year, "tuple")
    return "{:d} {:s} {:d}".format( int(date_l[2]), datetime.strptime(str(date_l[1]) , "%m").strftime("%B")  , int(date_l[0]) )

def effectiveAngle(angle):
    if angle>0: return angle
    else: return ((2*math.pi)+angle)

##CONSTANTS AND OTHER ORBITAL INFORMATION
G             = 6.67e-11
M_sun         = 1.99e30
M_earth       = 6e24
r_earth       = 6.37e6
R_earth       = 1.49e11
curr_year     = date.today().year + (  (  datetime.now().timetuple().tm_yday  ) /365.25   ) #Determine the current year exactly, to be used to find the launch window

#Orbital parameters
body_name     = input("Enter destination body's name: ")
r_aphelion    = float(input("Enter destination aphelion distance: "))
r_perihelion  = float(input("Enter destination perihelion distance: "))

ang_sep       = float(input("Enter angular separation at a particular known time (in degrees): ")) 
                  #The angular separation at a particular known time. Should be 
                  # given as the angle by which Earth is advanced with,
                  # respect to the body
ang_sep       = toRadians(ang_sep)

ang_sep_time  = input("Enter the date of the mentioned angular separation <DD-MM-YYYY> : ") #The time at which the above mentioned angular separation is known
ang_sep_time  = datetime.strptime(ang_sep_time, '%d-%m-%Y').date()
ang_sep_time  = ang_sep_time.year + (ang_sep_time.timetuple().tm_yday/365.25)

#Value setting
T_earth       = 365.25
R_body        = 0.5*(r_aphelion + r_perihelion)

if R_body > R_earth: outer = True
else: outer = False

T_body        = period(R_body)
w_earth       = (2* math.pi)/(T_earth)
w_body        = (2* math.pi)/T_body
T_synodic     = (2*math.pi)/( abs(w_earth-w_body)  )

##CALCULATIONS

#Stage 1: Earth's surface to geostationary orbit
R_geo_stat    = numpy.cbrt ( (  (G*M_earth)   /  (  (  2*math.pi/(24*3600)  )   **2)  ) )
v_esc         = math.sqrt(   (G*M_earth) * (  (2/r_earth)  -  (1/R_geo_stat)  )    )

#Stage 2: Transfer from geostationary to Hohmann orbit

v_launch      = math.sqrt(    2*G*M_sun * ( (1/R_earth)  -  (1/ ( R_earth+R_body ) )  )    )
v_current     = math.sqrt(    (G*M_sun)/R_earth      )

thrust_l      = False
if v_launch > v_current: thrust_l  = True
    
v_thrust      = abs(v_launch - v_current)

#Stage 3: Journey to celestial body

T_flight      = (math.pi/  (2* math.sqrt(2*G*M_sun))) * math.sqrt(  (R_earth + R_body  )**3  )
if outer:
    theta_sep_L   = math.pi*(    1-   (1/ (2*math.sqrt(2))) *  math.sqrt(  (1 + (R_earth/R_body)  )**3  )   )
    advance_time  = abs(  (  effectiveAngle(theta_sep_L)- ( (2*math.pi)-ang_sep)) /(  w_body-w_earth  )  )
else:
    theta_sep_L   = math.pi*(    1-   (1/ (2*math.sqrt(2))) *  math.sqrt(  (1 + (R_body/R_earth)  )**3  )   )
    advance_time  = abs(  (  effectiveAngle(theta_sep_L) - effectiveAngle(ang_sep )) /(  w_body-w_earth  )  )

launch_window = ang_sep_time + ( toYears(advance_time) )

while launch_window < curr_year:
    launch_window = launch_window+ ( toYears(T_synodic))
    
arrive_date   = launch_window + ( toYears(toDays(T_flight)) )

#Stage 4: Drop down into geostationary orbit at destination
v_rendezvous  = math.sqrt(    2*G*M_sun * ( (1/R_body)  -  (1/ ( R_earth+R_body ) )  )    )
v_current2    = math.sqrt(    (G*M_sun)/R_body     )

thrust_r      = False

if v_rendezvous > v_current2: thrust_r = True
v_thrust2     = abs(v_rendezvous - v_current2)


#Stage 5: Return journey
if outer:
    theta_sep_R   = math.pi*(    1-   (1/ (2*math.sqrt(2))) *  math.sqrt(  (1 + (R_body/R_earth)  )**3  )   )
    advance_timeR = abs(  (  effectiveAngle(theta_sep_R)-  ang_sep) /(  w_earth-w_body  )  )
else:
    theta_sep_R   = math.pi*(    1-   (1/ (2*math.sqrt(2))) *  math.sqrt(  (1 + (R_body/R_earth)  )**3  )   )
    advance_timeR = abs(  (  effectiveAngle(theta_sep_R)-  ((2*math.pi)-ang_sep)) /(  w_earth-w_body  )  )    

launch_windowR = ang_sep_time + (advance_timeR/365.25)

while launch_windowR < arrive_date:
    launch_windowR += (toYears(T_synodic))  
return_date   = launch_windowR + (toYears(toDays(T_flight)))

printResults()

