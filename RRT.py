'''
Created on Mar 3, 2014

@author: Dennis
'''
#!/usr/bin/env python

# rrt.py
# This program generates a simple rapidly
# exploring random tree (RRT) in a rectangular region.
#
# Written by Steve LaValle
# May 2011
###################
import sys, random, math, pygame
from pygame.locals import *
from math import sqrt,cos,sin,atan2
import time
import numpy as np

#constants
XDIM = 1024
YDIM = 768
WINSIZE = [XDIM, YDIM]
EPSILON = 7.0 # 7.0
NUMNODES = 100000

def dist(p1,p2):
    return sqrt((p1[0]-p2[0])*(p1[0]-p2[0])+(p1[1]-p2[1])*(p1[1]-p2[1]))

def find_mid(p1, p2):
    midpoint = ((p1[0]+p2[0])/2.0, (p1[1]+p2[1])/2.0)
    return midpoint

def step_from_to(p1,p2):
    if dist(p1,p2) < EPSILON:
        return p2
    else:
        theta = atan2(p2[1]-p1[1],p2[0]-p1[0])
        return p1[0] + EPSILON*cos(theta), p1[1] + EPSILON*sin(theta)

def point_in_object(x, y, x21, y21, x22, y22):
    if x > x21 and x < x22 and y > y21 and y < y22:
        return True
    else:
        return False

def node_in_rect(node, rect):
    x = node[0]
    y = node[1]
    x21 = rect[0]
    x22 = rect[0] + rect[2]
    y21 = rect[1]
    y22 = rect[1] + rect[3]
    if x > x21 and x < x22 and y > y21 and y < y22:
        return True
    else:
        return False

def obstacle_collision(node, obstacles):
    collision = False
    for rect in obstacles:
        if node_in_rect(node, rect):
            collision = True
            #break
    return collision

def get_line_points(line):
    linepoints = []
    if int(line[0][0]) == int(line[1][0]): # vertical
        if int(line[0][1]) < int(line[1][1]):
            for y in range(int(line[0][1]),int(line[1][1]+1)):
                linepoints.append((line[0][0],y))
        elif int(line[0][1]) > int(line[1][1]):
            rnge = range(int(line[1][1]),int(line[0][1]+1))
            for y in rnge[::-1]:
                linepoints.append((int(line[0][0]),y))
        else:
            print 'DDDD'
    else:
        xp1 = float(int(line[0][0])-int(line[1][0]))
        m1 = float(int(line[0][1])-int(line[1][1]))/xp1
        b1 = int(line[0][1])-m1*int(line[0][0])
        if int(line[0][0]) < int(line[1][0]):
            for x in range(int(line[0][0]),int(line[1][0]+1)):
                linepoints.append((x,int(m1*x+b1)))
        elif int(line[0][0]) > int(line[1][0]):
            rnge = range(int(line[1][0]),int(line[0][0]+1))
            for x in rnge[::-1]:
                linepoints.append((x,int(m1*x+b1)))
        else:
            print 'HELP'
    return linepoints

def main():
    done = False

    #initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('RRT      S. LaValle    May 2011')
    white = 255, 240, 200
    black = 20, 20, 40
    level = 0

    while done == False:

        for e in pygame.event.get():
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
                done = True
            if e.type == KEYUP and e.key == K_SPACE:
                    level = 0
        #print level
        if level == 0:
            screen.fill(black)
            
            #rect1 = (1*float(XDIM)/5,0,50,500)
            #rect2 = (2*float(XDIM)/5,YDIM-500,50,500)
            #rect3 = (3*float(XDIM)/5,0,50,500)
            #rect4 = (4*float(XDIM)/5,YDIM-500,50,500)
            
            #obstacles = [rect1, rect2, rect3, rect4]
            
            rect1 = (1*float(XDIM)/5-75,50,250,300)
            rect2 = (2*float(XDIM)/5-75,YDIM-350,250,300)
            rect3 = (3*float(XDIM)/5-75,50,250,300)
            rect4 = (4*float(XDIM)/5-75,YDIM-350,250,300)
        
            obstacles = [rect1, rect2, rect3, rect4]
            
            for rect in obstacles:
                pygame.draw.rect(screen, (255,100,25),rect,0)
                pygame.display.update()

            circsize = EPSILON*2#10.0
            level = 1 
            
        elif level == 1:
            while level == 1:
                mouse_pos = pygame.mouse.get_pos()
                x_mouse = mouse_pos[0]
                y_mouse = mouse_pos[1]            
                breakout = False
                for e in pygame.event.get():
                    if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        startpos = (x_mouse, y_mouse)
                        pygame.draw.circle(screen, (0,255,0), (int(startpos[0]), int(startpos[1])), int(circsize))
                        pygame.display.update()
                        level = 2
                    elif e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")
                        done = True
                    elif e.type == KEYUP and e.key == K_SPACE:
                        print 'space'
                        breakout = True
                        level = 0
                if breakout == True:
                    break
        elif level == 2:
            while level == 2:
                mouse_pos = pygame.mouse.get_pos()
                x_mouse = mouse_pos[0]
                y_mouse = mouse_pos[1] 
                breakout = False
                for e in pygame.event.get():
                    if e.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                        goalpos = (x_mouse, y_mouse)
                        pygame.draw.circle(screen, (0,0,255), (int(goalpos[0]), int(goalpos[1])), int(circsize))
                        pygame.display.update()
                        level = 3
                    elif e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")
                        done = True
                    elif e.type == KEYUP and e.key == K_SPACE:
                        print 'space'
                        breakout = True
                        level = 0
                if breakout == True:
                    break
        
        elif level == 3:
            treestart = time.clock()
            nodes = []
            pardict = {}
            
            nodes.append(startpos) 
            breaknodes = False
            countnodes = 0
            for i in range(NUMNODES):
                countnodes = countnodes + 1
                for e in pygame.event.get():
                    if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                        sys.exit("Leaving because you requested it.")
                        done = True
                    elif e.type == KEYUP and e.key == K_SPACE:
                        print 'space'
                        breakout = True
                        level = 0
                if breakout == True:
                    break
                
                rand = random.random()*float(XDIM), random.random()*float(YDIM)
                
                nn = nodes[0]
                for p in nodes:
                    if dist(p,rand) < dist(nn,rand):
                        nn = p
                        
                newnode = step_from_to(nn,rand)
                collided = obstacle_collision(newnode, obstacles)
                
                if collided == True:
                    pass
                    #print 'collision'
                    #pygame.draw.circle(screen, (100,100,100), (int(newnode[0]), int(newnode[1])), int(2))
                    #pygame.display.update()
                #time.sleep(0.5)
                else:
                    nodes.append(newnode)
                    pygame.draw.line(screen,white,nn,newnode)
                    pardict[newnode] = nn
                    
                    if dist(newnode,goalpos) < circsize:
                        nodes.append(goalpos)
                        pardict[goalpos] = newnode
                        #print 'goal found'
                        treeend = time.clock()
                        treeduration = treeend-treestart
                        print 'Tree finished in', round(treeduration,1), 'seconds'
                        level = 4
                        break
                    pygame.display.update()
            if countnodes > NUMNODES-1:
                print 'limit reached'
                level = 5
                                
        elif level == 4:
            #print len(nodes), 'nodes'
            pathnodes = []
            x = nodes[-1]
            while x != startpos:
                pathnodes.append(x)
                pygame.draw.line(screen, (255,0,0), x, pardict[x], 5)
                #time.sleep(0.01)   
                pygame.display.update()     
                x = pardict[x]
            pathnodes.append(startpos)
            pathnodes = pathnodes[::-1]

            pygame.display.update()
            level = 5
        
        elif level == 5:
            if e.type == KEYUP and e.key == K_1:
                level = 6
            elif e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
                done = True
            elif e.type == KEYUP and e.key == K_SPACE:
                print 'space'
                level = 0
                
        elif level == 6:
            screen.fill(black)
            for rect in obstacles:
                pygame.draw.rect(screen, (255,100,25),rect,0)
            pygame.draw.circle(screen, (0,255,0), (int(startpos[0]), int(startpos[1])), int(circsize))
            pygame.draw.circle(screen, (0,0,255), (int(goalpos[0]), int(goalpos[1])), int(circsize))
            for i in range(len(pathnodes)-1):
                pygame.draw.line(screen, (255,0,255), pathnodes[i], pathnodes[i+1], 5) 
                #time.sleep(0.01)
                #pygame.display.update()
            for i in range(len(pathnodes)):
                pygame.draw.circle(screen,(0,255,255),(int(pathnodes[i][0]),int(pathnodes[i][1])),2)
            pygame.display.update()
            
            level = 7
        
        elif level == 7:
            if e.type == KEYUP and e.key == K_2:
                level = 8
            elif e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
                done = True
            elif e.type == KEYUP and e.key == K_SPACE:
                print 'space'
                level = 0
                
        elif level == 8: # optimization
            optistart = time.clock()
            oldpath = []
            newpath = []
            
            #print len(pathnodes)
            for i in range(len(pathnodes)-1):
                these_points = get_line_points([pathnodes[i],pathnodes[i+1]])
                for p in range(len(these_points)-1):
                    oldpath.append(these_points[p])
            oldpath.append(goalpos)
            for row in range(len(oldpath)):
                newpath.append(oldpath[row])
            #print oldpath
            for i in range(1000):
                if i < len(newpath):
                    rnge = range(i+1,len(oldpath))
                    rnge = rnge[::-1]
                    oprev = []
                    for rr in range(len(rnge)):
                        oprev.append(oldpath[rnge[rr]])
                    #print oprev
                    for j in range(len(oprev)):
                        print oprev[i],oprev[j]
                        colid = False
                        lineps = get_line_points([oldpath[i],oprev[j]])
                        for ps in lineps:
                            if obstacle_collision(ps,obstacles):
                                colid = True
                        if (colid == True):
                            newpath.append(oprev[j])
                        else:
                            pts = lineps
                            pts = pts[::-1]
                            for p in pts:
                                newpath.append(p)
                            break
                oldpath = []
                for row in range(len(newpath)):
                    oldpath.append(newpath[row])
                
                
                """screen.fill(black)
                for rect in obstacles:
                    pygame.draw.rect(screen, (255,100,25),rect,0)
                pygame.draw.circle(screen, (0,255,0), (int(startpos[0]), int(startpos[1])), int(circsize))
                pygame.draw.circle(screen, (0,0,255), (int(goalpos[0]), int(goalpos[1])), int(circsize))
                for i in range(len(pathnodes)-1):
                    pygame.draw.line(screen, (255,0,255), pathnodes[i], pathnodes[i+1], 5) 
                    #time.sleep(0.01)
                    #pygame.display.update()
                for i in range(len(pathnodes)):
                    pygame.draw.circle(screen,(0,255,255),(int(pathnodes[i][0]),int(pathnodes[i][1])),2)
                pygame.display.update()"""
                for i in range(len(oldpath)-1):
                    pygame.draw.line(screen, (255,255,0), newpath[i], newpath[i+1], 2) 
                    pygame.display.update()
                    time.sleep(0.001)
                newpath = []
                ################################3
            pygame.display.update()


                #time.sleep(0.5)
                

            optiend = time.clock()
            optiduration = optiend - optistart
            print 'Optimization finished in', round(optiduration,1), 'seconds'
            level = 9
            
        elif level == 9:
            if e.type == QUIT or (e.type == KEYUP and e.key == K_ESCAPE):
                sys.exit("Leaving because you requested it.")
                done = True
            elif e.type == KEYUP and e.key == K_SPACE:
                print 'space'
                level = 0


            #print 'level 6'
            
                
# if python says run, then we should run
if __name__ == '__main__':
    main()
