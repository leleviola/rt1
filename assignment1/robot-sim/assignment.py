from __future__ import print_function
import time
from sr.robot import *


R = Robot()
a_th = 2.0 
d_th = 0.4
d_rel = 0.6 # distance between tokens in the stack
grabbed = False # this variable indicates if he grabbed a token or not



def drive(speed, seconds):
    """
    Function for setting a linear velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def turn(speed, seconds):
    """
    Function for setting an angular velocity
    
    Args: speed (int): the speed of the wheels
	  seconds (int): the time interval
    """
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(seconds)
    R.motors[0].m0.power = 0
    R.motors[0].m1.power = 0

def find_mindist_untaken_token(marker_list, marker_taken):
    """
    Function to find the closest token that is in marker_list and not in marker_taken

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    index (int): the index in marker_list of the token (-1 if no token is detected)
    """
    dist=100
    i = -1
    indmin = 0
    for token in marker_list :
        i = i+1
        if token.dist < dist and not(find_same_token(marker_taken, token)):
            indmin = i
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1, -1
    else:
   	    return dist, rot_y, indmin

def find_mindist_taken_token(marker_list, marker_taken):
    """
    Function to find the closest token of tokens that are in marker_list and also in marker_taken

    Returns:
	dist (float): distance of the closest token (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)
    index (int): the index in marker_list of the token (-1 if no token is detected)
    """
    dist=100
    i = -1
    indmin = 0
    for token in marker_list :
        i = i+1
        if token.dist < dist and (find_same_token(marker_taken, token)):
            indmin = i
            dist=token.dist
            rot_y=token.rot_y
    if dist==100:
        return -1, -1, -1
    else:
   	    return dist, rot_y, indmin
   	    
def find_maxdist_token(marker_list):
    """
    Function to find of the most distant token

    Returns:
	dist (float): distance (-1 if no token is detected)
    rot_y (float): angle between the robot and the token (-1 if no token is detected)

    """
    
    dist = 100
    maxdist = 0
    indmax = 0
    i = -1
    for token in marker_list:
        i = i+1
        if token.dist < dist:
            if token.dist > maxdist:
                indmax = i
                maxdist=token.dist
                rot_y=token.rot_y
    
    return maxdist, rot_y, indmax

def find_same_token(list, mark):
        
    for token in list:
        token_code = token.info.code
        if mark.info.code == token_code:
            
            return True
    return False



markers = R.see() #for calculate the radius

marker_taken = [] # list

radius = find_maxdist_token(markers)[0]/2 # for first cycle we want to find the center, so we go to the  opposite marker and we stop in the middle

print("robot initialized")
while 1: # main cicle that repeats every time robot release a token

    print("new cycle started")
    while(grabbed==False): 
        
        markers = R.see()
        dist, rot_y, index = find_mindist_untaken_token(markers, marker_taken)  # we look for markers untaken
        

        if dist==-1:
            print("I don't see any token :(")
            exit()  # if no markers are detected, the program ends
        
        if dist <d_th: 
            print("found it :)")
            R.grab() # if we are close to the token, we grab it.
            
            grabbed = True
            print("marker taken") 
            tk_grabb = markers[index] 
            
            if(len(marker_taken)>0): # if it isn't the first token grabbed, turn of circa 180 degrees
                turn(10,7)
                
            else:
                print("let's go to the center")
                
            
        elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
            print("let's go to take marker with code ",markers[index].info.code)
            drive(30, 0.25)
        # if the robot is not well aligned with the token, we move it on the left or on the right
        elif rot_y < -a_th: 
            print("turn left a bit...")
            turn(-4, 0.25)
        elif rot_y > a_th:
            print("turn right a bit...")
            turn(+4, 0.25)
            
    while(grabbed==True):
        
        markers = R.see()
        
        if len(marker_taken) == 0:  #starting cycle
            
            dist, rot_y, index = find_maxdist_token(markers) # for first cycle we want to find the center, so we go to the  opposite marker and we stop in the middle
            
            if dist==-1:
                print("I don't see any token :(")
                exit()  # if no markers are detected, the program ends
            if dist < radius :
                
                R.release() 
                print("released token ", tk_grabb.info.code) 
                marker_taken.append(tk_grabb) #add the marker to the marker_taken
                
                
                grabbed = False
                drive(-20,3)
                
                turn(8,3.5)
                print("giving a look around...")
                
                
                             
            elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
                print("let's go straight on")
                drive(30, 0.25)
            # if the robot is not well aligned turn left or right
            elif rot_y < -a_th: 
                print("turn left a bit...")
                turn(-4, 0.25)
            elif rot_y > a_th:
                print("turn right a bit...")
                turn(+4, 0.25)

        else: # generic cycle from the second marker taken to the last
            
            dist, rot_y, index = find_mindist_taken_token(markers, marker_taken)  # we look for the nearest token already taken
            
            if dist==-1:
                print("I don't see any token :(")
                exit()  # if no markers are detected, the program ends
        
            if dist <d_rel: 
                print("found markers stack :)")
                R.release()
                marker_taken.append(tk_grabb) # add the marker to marker_list
                grabbed = False
                

                drive(-20,3)   # go away from the stack of token         
                turn(8,3.5) # turn to see other tokens
                if(len(marker_taken)==6):
                    print("all marker moved!")
                    exit()
                print("giving a look around...")
            elif -a_th<= rot_y <= a_th: # if the robot is well aligned with the token, we go forward
                print("let's go straight on")
                drive(30, 0.25)
            # if the robot is not well aligned with the token, we move it on the left or on the right
            elif rot_y < -a_th: 
                print("turn left a bit...")
                turn(-4, 0.25)
            elif rot_y > a_th:
                print("turn right a bit...")
                turn(+4, 0.25)       

