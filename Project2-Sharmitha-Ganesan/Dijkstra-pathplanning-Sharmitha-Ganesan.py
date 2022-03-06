# -*- coding: utf-8 -*-
"""
Author Sharmitha Ganesan

"""

import numpy as np
import math
import heapq
import time
import cv2
import pygame


start_time = time.time()

'''8 ACTION SETS FUNCTION'''

def ActionMoveUp(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_y = curr_node[0]
    new_node_y-=1
    new_node = (new_node_y,curr_node[1])
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)

def ActionMoveLeft(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_x = curr_node[1]
    new_node_x-=1
    new_node = (curr_node[0],new_node_x)
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)
     
def ActionMoveRight(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_x = curr_node[1]
    new_node_x+=1
    new_node = (curr_node[0],new_node_x)
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)
   
def ActionMoveDown(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_y = curr_node[0]
    new_node_y+=1
    new_node = (new_node_y,curr_node[1])
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)

def ActionMoveUL(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_y = curr_node[0]
    new_node_y-=1
    new_node_x = curr_node[1]
    new_node_x-=1
    new_node = (new_node_y,new_node_x)
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)

def ActionMoveUR(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_y = curr_node[0]
    new_node_y-=1
    new_node_x = curr_node[1]
    new_node_x+=1
    new_node = (new_node_y,new_node_x)
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)

def ActionMoveDL(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_y = curr_node[0]
    new_node_y+=1
    new_node_x = curr_node[1]
    new_node_x-=1
    new_node = (new_node_y,new_node_x)
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)

def ActionMoveDR(curr_node):
    x = curr_node[0]
    y = curr_node[1]
    curr_node = (x,y)
    new_node=()
    new_node_y = curr_node[0]
    new_node_y+=1
    new_node_x = curr_node[1]
    new_node_x+=1
    new_node = (new_node_y,new_node_x)
    if new_node[0]>=0 and new_node[1]>=0:
        return(new_node,True)
    else:
        return(curr_node,False)

def graph_to_cover(start,size_x,size_y): #remember that this size_x and size_y are the sizes of the matrix, so not the end coordinates
    i = start[0] #x coordinate
    j = start[1] #y coordinate
    if i <size_x and j<size_y:
        graph={}
        #for the origin
        if i==0 and j==0: 
            graph[(i,j)]={(i+1,j+1),(i+1,j),(i,j+1)}
        #for the last point
        elif i==size_x-1 and j==size_y-1:
            graph[(i,j)]={(i-1,j),(i-1,j-1),(i,j-1)}
        #when Y =0
        elif i==size_x-1 and j ==0:
            graph[(i,j)]={(i-1,j),(i-1,j+1),(i,j+1)}
        #when X = 0
        elif j==size_y-1 and i ==0:
            graph[(i,j)]={(i,j-1),(i+1,j-1),(i+1,j)}
        #for points along borders
        elif i == 0 and j!=0 and j!=size_y-1:
            graph[(i,j)]={(i,j-1),(i,j+1),(i+1,j-1),(i+1,j),(i+1,j+1)}
        elif i == size_x-1 and j!=0 and j!=size_y-1:
            graph[(i,j)]={(i,j-1),(i,j+1),(i-1,j-1),(i-1,j),(i-1,j+1)}
        elif j == 0 and i!=0 and i!=size_x-1:
            graph[(i,j)]={(i-1,j),(i+1,j),(i+1,j+1),(i,j+1),(i-1,j+1)}
        elif j == size_y-1 and i!=0 and i!=size_x-1:
            graph[(i,j)]={(i-1,j),(i+1,j),(i+1,j-1),(i,j-1),(i-1,j-1)} 
        #for all other points
        else: 
            graph[(i,j)]={(i-1,j),(i-1,j+1),(i-1,j-1),(i+1,j-1),(i+1,j),(i+1,j+1),(i,j-1),(i,j+1)}

        return(graph)
    else:
        pass

def costFunction(graph,start):
    new_dict={}
    for key,value in graph.items():
        new_dict[key]={}
        for next_one in value:
            #all possible movements from the parent
            R = ActionMoveRight(key)
            L = ActionMoveLeft(key)
            U =ActionMoveUp(key)
            D = ActionMoveDown(key)
            TL = ActionMoveUL(key)
            TR =ActionMoveUR(key)
            DL = ActionMoveDL(key)
            DR = ActionMoveDR(key)
            #checking for parent nodes nearby
            if (next_one==R[0]) or (next_one==L[0]) or (next_one==U[0]) or (next_one==D[0]):
                new_dict[key][next_one]=1 #Assigning cost of 1 in this case
           
            elif (next_one==TL[0]) or (next_one==TR[0]) or (next_one==DL[0]) or (next_one==DR[0]):
                new_dict[key][next_one]=1.414 #Assigning cost of 1.414 in this case
    return(new_dict)

all_distance = {}
backtracking = {}
covered = []
#variable to exit out of the while loop in the djialgorithm function
check=0
def djialgorithm(graph,start):
    #adding the global variables
    global check
    global covered
    #when the function starts
    all_distance[start]=0
    covered.append(start)
                                                               
    for vertex,edge in graph.items():                       
        all_distance[vertex]=math.inf                                            #setting all nodes in infinity distance
    #starting the priority queue with the start node
    priority_queue = [(0,start)]
    #checking the length of the priority queue
    #and, inserting the while loop exit condition
    while len(priority_queue)>0 and check!=[]:
        #popping the current distance and the currenyt vertex 
        #from the priority queue
        curr_dist,curr_vert = heapq.heappop(priority_queue)
        #checking the value of the current distance and 
        if curr_dist>all_distance[curr_vert]:
            continue
        for next_one,cost in graph[curr_vert].items():
            #Updating the cost
            distance = curr_dist + cost 
           
            if distance < all_distance[next_one]:
                backtracking[next_one]={}
                #adding to the backtracking dictionary
                backtracking[next_one][distance]=curr_vert
                all_distance[next_one]=distance
                #pushing from the priority queue
                heapq.heappush(priority_queue, (distance, next_one))
                #checking of the next_one is not added to the covered
                #checks what node to go to next
                if next_one not in covered:
                    #appending to the covered list
                    covered.append(next_one)
                    #checking if the next_one is the goal
                    if next_one==goal:
                        print('GOAL REACHED')
                        #changing check variable for the exit condition
                        check=[]
                        #breaking out of the loop
                        break
    #returning all_distance, covered list and backtracked dictionary
    return(all_distance,covered,backtracking)     

def BackTrack(backtrack_dict,goal,start):                                       #goal is the starting point now and start is the goal point now
    #initializing the backtracked list
    back_track_list = []
    #appending the start variable to the back_track_list list
    back_track_list.append(start)
    #while the goal is not found
    while goal!=[]:
        #for key and values in the backtracking dictionary 
        for k,v in backtracking.items():
            #for the key and values in the values, v
            for k2,v2 in v.items():
                #checking if the first key is the start
                if k==start:
                    #checking if not in the backtrackedlist
                    if v2 not in back_track_list:
                        back_track_list.append(start)
                    #updating the start variable
                    start=v2
                    #checking if it is the goal
                    if v2==goal:
                        goal=[]
                        break
    #returns the backtracked list
    return(back_track_list)

def Pointdjikstra(Maximum_size_x,Maximum_size_y,start,goal):
    '''
    function to define obsatcle space and run the djikstra algorithm 
    '''
    Maximum_size_x+=1                                                           #max width
    Maximum_size_y+=1                                                           #max height
    
    all_points = []
    for i in range(0,401):
        for j in range(251): 
            all_points.append((i,j)) #appending to the list
    print('Length ofall_points')
    print(len(all_points))
    #empty list to store points that are in the obstacle
    list_of_all_points = [] #points that are in the shapes | obstacles
    clearance_points =[]
    highlight=[]
    #for every such point
    for c in all_points:
        x = c[0]
        y = c[1]
        #circle shaped obstacle with 5mm clearance
        if((x-300)**2 + (y-185)**2 <= (45)**2):
            list_of_all_points.append((x,y))
    
        #polygon shaped obstacle with 5mm clearance
        if y - (0.316)*x <=178.607:
            if y+(1.232)*x >= 224.348:
                if y+(3.2)*x <=441 or y-(0.857)*x >=106.429:
                    list_of_all_points.append((x,y))
       
        #hexagon obstacle with 5mm clearance
        if x>=160 and x<=240 and y+(0.577)*x<=260.883 and y+(0.577)*x >=170.057 and y-(0.577)*x <=29.945 and y-(0.577)*x >= -60.885:
            list_of_all_points.append((x,y))
           
        #highlighting_clearance
        if ((x-300)**2 + (y-185)**2 <= (40)**2):
            clearance_points.append((x,y))
            
        if x>=165 and x<=235 and y+(0.577)*x<=255.883 and y+(0.577)*x >=175.057 and y-(0.577)*x <=24.945 and y-(0.577)*x >= -55.885:
            clearance_points.append((x,y))
                
        if y - (0.316)*x <=173.607:
            if y+(1.232)*x >= 229.348:
                if y+(3.2)*x <=436 or y-(0.857)*x >=111.429:
                    clearance_points.append((x,y))
                    
    #checking if the GOAL entered is within these points
    if goal in list_of_all_points:
        print('Goal is in obstacle space. Please try again')
    
    #checking the length of all the points within the obstacles itself
    print(' Length of points in obstacle space : ')
    print(len(list_of_all_points))
    #generating the base graph of all the coordinates
    djigraph = {}
    for i in range(Maximum_size_x-1,-1,-1):
        for j in range(Maximum_size_y-1,-1,-1):
            graph = graph_to_cover((i,j),Maximum_size_x,Maximum_size_y)
            djigraph[(i,j)]=graph[(i,j)] 
    #checking the length of this graph
    print('Total djikstra graph nodes ')
    print(len(djigraph))
    
    #removing all the coordinates that are within the points in the obtsacle and all that
    #are connected to it as well
    for key,value in djigraph.items():
        value_copy = value.copy()
        for coordinates in value_copy:
            if coordinates in list_of_all_points:
                value.remove(coordinates) 
    djigraph_copy=djigraph.copy()
    for key,value in djigraph_copy.items():
        if key in list_of_all_points:
            del djigraph[key]
    print('Nodes to be explored excluding obstacle space')
    print(len(djigraph))
    #checking all the costs
    costs_calculated = costFunction(djigraph,start)
    actual_graph = costs_calculated
    #empty dictionary with all the distances
    all_distance = {}
    #empty dictionary for backtracking from child to parent upto the start
    backtracking = {}
    #list of all the covered nodes
    covered = []
    #variable to exit out of the while loop in the djialgorithm function
    #returning all the essential lists after calculating using
    #djialgorithm
    all_distance,covered,backtracking= djialgorithm(actual_graph,start) #can alter the start here
    #creating a copy so that the dictionary can be modified
    all_distance_copy = all_distance.copy()
    for k,v in all_distance_copy.items():
        if all_distance_copy[k] == math.inf:
            del all_distance[k]
    #returning all_distance, backtracking and list_of_all_points
    return(all_distance,covered,backtracking,list_of_all_points,clearance_points)

#Taking inputs
x_start= int(input("Enter the x coordinate of the start:  "))
y_start= int(input("Enter the y coordinate of the start:  "))
x_goal= int(input("Enter the x coordinate of the goal:  "))
y_goal= int(input("Enter the y coordinate of the goal:  "))
start = (x_start,y_start) 
goal =  (x_goal,y_goal)   
Maximum_size_x = 400
Maximum_size_y = 250
all_distance,covered,backtrack,listofallpointsformap,highlight= Pointdjikstra(Maximum_size_x,Maximum_size_y,start,goal)


len(backtrack)
#Backtracking 
backtracked_final = BackTrack(backtrack,start,goal)
print(backtracked_final)
#printing the final time for completion
print("Total Time Taken : ",time.time() - start_time, "seconds")

#defining a blank canvas
new_canvas = np.zeros((251,401,3),np.uint8) 
#for every point that belongs within the obstacle
    
for l in listofallpointsformap: #change the name of the variable l
    x = l[1]
    y = l[0]
    new_canvas[(x,y)]=[0,0,255]                                                 #assigning a red coloured pixel
for d in highlight:
    x = d[1]
    y =d[0]
    new_canvas[(x,y)] = [0,255,255]                                              #assigning a yellow coloured pixel
#flipping the image for correct orientation
new_canvas = np.flipud(new_canvas)
#making a copy for backtracking purpose
new_canvas_copy_backtrack = new_canvas.copy()
#making a copy for showing the covered nodes on the obstacle space
#can be used for the animation
new_canvas_copy_covered = new_canvas.copy()
new_canvas_copy_covered = cv2.resize(new_canvas_copy_covered,(600,400))
#showing the obstacle map
cv2.imshow('new_canvas',new_canvas)
cv2.waitKey(0)
cv2.destroyAllWindows()

pygame.init()
display_width = 400
display_height = 250
gameDisplay = pygame.display.set_mode((display_width,display_height),pygame.FULLSCREEN)
pygame.display.set_caption('Covered Nodes- Animation')
black = (0,0,0)
white = (255,255,255)

surf = pygame.surfarray.make_surface(new_canvas_copy_covered)
clock = pygame.time.Clock()
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    gameDisplay.fill(black)
    for path in covered:
        if path not in new_canvas_copy_covered:
        
            x = path[0]
            y = abs(250-path[1])
            pygame.draw.rect(gameDisplay, white, [x,y,1,1])          
            pygame.display.flip()
    for path in backtracked_final:
        
        pygame.time.wait(5)    
        x = path[0]
        y = abs(250-path[1])
        pygame.draw.rect(gameDisplay, (0,0,255), [x,y,1,1])
        pygame.display.flip()
    done = True
pygame.quit()
#covered path
for path in covered:
    x = path[0]
    y = path[1]
    new_canvas_copy_backtrack[(250-y,x)]=[255,255,255]                                #setting every backtracked pixel to white
#showing the final backtracked path
new_backtracked = cv2.resize(new_canvas_copy_backtrack,(600,400))
cv2.imshow('covered',new_backtracked)
cv2.waitKey(0)
cv2.destroyAllWindows()
#backtracked path
for path in backtracked_final:
    x = path[0]
    y = path[1]
    new_canvas_copy_backtrack[(250-y,x)]=[0,255,0]                              #setting every backtracked pixel to green
#showing the final backtracked path
new_backtracked = cv2.resize(new_canvas_copy_backtrack,(600,400))
cv2.imshow('new_backtracked',new_backtracked)
cv2.waitKey(0)
cv2.destroyAllWindows()
