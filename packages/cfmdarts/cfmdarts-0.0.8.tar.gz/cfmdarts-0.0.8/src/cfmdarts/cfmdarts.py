import math
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Creating Phase I.
# assuming no air resistance, 
# asuming dart always hits wall,
# frame of reference: shot origin has same coordinates [z,y] aas the bullseye 
# 1.73m is from floor to bullseye (height)
# 2.37m is distance from throw to board (8ft)

class Projectile(object):
    
    """
    A class for the projectile motion of the dart.
    """

    ##using constructors instantiate the object which initializes
    ##The data values to the class
    def __init__(self,tilt_angle, swivel_angle, initial_velocity):
        self.tilt_angle = tilt_angle
        self.swivel_angle = swivel_angle
        self.initial_velocity = initial_velocity
    
    
    def range(self):
        """
        this is the range of the projectile assuming it hits the board at d = 8m. 
        """
        d = 2.37 # distance  metres away from dartboard
        
        k = (math.pi / 180) ## degrees to radians converter since trig fucntions take radians
        
        return  d / (math.cos(self.swivel_angle * k))
    
    
    
    def height(self):
        """
        this is the distance in the y-direction relative to the bullseye.
        """
        
        g = 9.81
        k = (math.pi / 180)
        
        global R_x
        R_x = Projectile.range(self)
        
     
        return (math.tan(k*self.tilt_angle)*R_x) - ((g * R_x**2) / (2 * (self.initial_velocity *  math.cos(k*self.tilt_angle))**2 ))   
    
    
    def shift(self):
                                                 
        """
        this is the distance in the z-direction relative to the bullseye.
        """

        d=2.37
        k = (math.pi / 180)
       
        if self.swivel_angle > 0:
            return d * (math.tan(abs(self.swivel_angle*k)))
        if self.swivel_angle <0:
            return d * -(math.tan(abs(self.swivel_angle*k)))
        if self.swivel_angle == 0 or self.initial_velocity ==0:
            return 0


class Coordinates(object): 
    ##using constructors instantiate the object which initializes
    ##The data values to the class
    def __init__(self,tilt_angle, swivel_angle, initial_velocity):
        self.tilt_angle = tilt_angle
        self.swivel_angle = swivel_angle
        self.initial_velocity = initial_velocity


    
    def cartesian_coordinates(self):
        """
        Returns the cartesian coordinates in relation to the given tilt angle,
        swivel angle and initial velocity.
        """

        z = Projectile.shift(self)
        y = Projectile.height(self)

        return [z,y]


    
    def theta(self):
        """
        this gives us our theta value used to determine score
        """

        k = math.pi / 180 ## this is used to counteract the radians output of the functions math does. 

        z = Projectile.shift(self)
        y = Projectile.height(self)

        if z==0 and y>0:
            return 90
        if z==0 and y<0:
            return 270
        if y==0 and z>0:
            return 0
        if y==0 and z<0 :
            return 180
        if z>0 and y>0:
            return math.atan(y/z) * (k**-1)
        if z<0 and y>0:
            return 180 - math.atan(abs(y/z)) * (k**-1)
        if z<0 and y<0: 
            return  180 + math.atan(y/z) * (k**-1)
        if z>0 and y<0:
            return 360 - math.atan(abs(y/z)) * (k**-1)
    
    
    def r(self):
        """
        this gives us our r value used to determine score
        """

        z = Projectile.shift(self)
        y = Projectile.height(self)

        r = math.sqrt((z)**2 + (y)**2)
    
        return r 
    
    
    def polar_coordinates(self):
        """
        this function combines the projectiles and coordinates class to create the r and theta used in the scores class.
        """

        r = Coordinates.r(self)
        theta = Coordinates.theta(self)

        
        return [r, theta]


def initial_score(theta):

    '''
    this function takes the value of 
    theta and outputs the INITIAL
    score that is obtained from that value.
    '''
    ## 
    
    if theta >= 0 and theta < 9:
        return 6
    elif theta >= 9 and theta < 27:
        return 13
    elif theta >= 27 and theta < 45:
        return 4
    elif theta >= 45 and theta < 63:
        return 18
    elif theta >= 63 and theta < 81:
        return 1
    elif theta >= 81 and theta < 99:
        return 20
    elif theta >= 99 and theta < 117:
        return 5
    elif theta >= 117 and theta < 135:
        return 12 
    elif theta >= 135 and theta < 153:
        return 9
    elif theta >= 153 and theta < 171:
        return 14 
    elif theta >= 171 and theta < 189:
        return 11
    elif theta >= 207 and theta < 225:
        return 8
    elif theta >= 225 and theta < 243:
        return 7
    elif theta >= 243 and theta < 261:
        return 19
    elif theta >= 261 and theta < 279:
        return 3
    elif theta >= 279 and theta < 297:
        return 17
    elif theta >= 297 and theta < 315:
        return 2
    elif theta >= 315 and theta < 333 :
        return 15
    elif theta >= 333 and theta < 351:
        return 10
    elif theta >= 351 and theta < 360:
        return 6
    elif theta < 0 or theta >= 360:
        return "error"
        


def final_score(r, theta):
    
    """
    this function will take the initial_score value and depending solely 
    on our r value  (in accordance to the points system of darts) will output 
    the following:
    0 <= r < r_1   ---   bullseye, gives 50
    r_1 <= r < r_2   ---   25 ring, gives 25
    r_2 <= r < r_3   ---   blank, gives initial score as is  
    r_3 <= r < r_4   ---   triple ring, multiplies initial score by 3
    r_4 <= r < r_5   ---   blank, gives initial score as is 
    r_5 <= r < r_6   ---   double ring, multiplies initial score by 2
    r >= r_6   ---   missed shot, null score (0)
    """

    ## defining dartboard r_n values in meters [m]
    ## https://dartsavvy.com/dart-board-dimensions-and-sizes/

    r_1 = 0.0127 / 2
    r_2 = 0.0318 / 2
    r_3 = 0.107
    r_4 = 0.107 + 0.008
    r_5 =  0.170 - 0.008
    r_6 = 0.170

    ## defining intial_score

    global score_i 
    score_i = initial_score(theta) 

    if r < r_1:
        return 50
    elif  r_1 <= r and r < r_2:
        return 25
    elif r_2 <= r and r < r_3:
        return score_i
    elif r_3 <= r and r < r_4: 
        return score_i * 3
    elif r_4 <= r and r < r_5: 
        return score_i
    elif r_5 <= r and r < r_6:
        return score_i * 2 
    elif r >= r_6: 
        return  0   


def dart_simulation(tilt_angle, swivel_angle, initial_velocity):
    
    """
    this function will combine phase I and II's functions in order to calculate the final score. 
    """
    Coordinates_simulation = Coordinates(tilt_angle, swivel_angle, initial_velocity)
    
    r = Coordinates_simulation.r()
    theta = Coordinates_simulation.theta()
    
    if tilt_angle >= 90 or tilt_angle <= -90 or swivel_angle >= 90 or swivel_angle <= -90 or initial_velocity ==0:
        return "null shot, please ensure the tilt and swivel angles are both between -90 and 90, and that the velocity is positive"
    else:
        return final_score(r, theta)  

def display_dartboard(r, theta):
    """ A function that displays an image of a dartboard with a cross of where the dart hits,
    if no cross appears it means the shot is out of the 0.243m x 0.243m square"""
   
    img = mpimg.imread('dartboard.png') #Reads the png image of the dartboard
    imgplot = plt.imshow(img, extent = (-0.2478,0.2478,-0.2478,0.2478)) #Displays the image to the figure, extent places the image on  the coordinates stated
    ax = plt.gca() #Creates an instance to create the axis

    ax.get_xaxis().set_visible(False) #Hides the axis for a better UI
    ax.get_yaxis().set_visible(False)

    cartesian_coordinate_x = r * math.cos(theta * math.pi / 180)
    cartesian_coordinate_y = r * math.sin(theta * math.pi / 180)

    plt.xlim([-0.243, 0.243]) #Sets the respective coordinate limits
    plt.ylim([-0.243, 0.243])
    plt.plot([cartesian_coordinate_x],[cartesian_coordinate_y], color = "magenta", marker = "x") #Plots an "x" marker on the figure
    plt.show() #Runs the figure to display it
