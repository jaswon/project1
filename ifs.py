import pygame
from pygame.locals import *
import random
import math
from itertools import product

ws = 700 # window size
bs = 50 # buffer size
ds = ws - bs * 2 # draw window size

rt3 = math.sqrt(3)

def density(x,y,w,h,s):
    # pxarray = pygame.surfarray.array2d(s)
    wcnt = 0
    tcnt = w*h
    white = pygame.Color(255,255,255)
    for p in product(xrange(x,x+w),xrange(y,y+h)):
        if s.get_at(p) == white:
            wcnt += 1
    return wcnt/float(tcnt)

def tMatrix(a,b,c,d,e,f):
    return lambda x,y: (a*x+b*y+e,c*x+d*y+f)

def sngon(n): # 3 <= n <= 8
    s = .5/(1+math.sin(math.pi*max(.5-2/float(n),0)))
    r = .5*(1-s)
    return [lambda x,y,i=i,n=n: (x*s+r*math.sin(2*math.pi/n*i),y*s+r*math.cos(2*math.pi/n*i)) for i in xrange(n)]

def roulette (t):
    c = random.random() * sum([i[1] for i in t])
    for v in t:
        c -= v[1]
        if c <= 0:
            return v[0]


def main():
    # init screen
    pygame.init()
    screen = pygame.display.set_mode((2*ws,ws))

    ### sierpinski fractions
    ifs = [ (i,1) for i in sngon(7)]
    dim = [-.5,.5,-.5,.5]
    p = (0,.5)
    q = (0,.5)

    ### fern
    # ifs = [
    #     (tMatrix(0,0,0,.16,0,0),.01),
    #     (tMatrix(.2,-.26,.23,.22,0,1.6),.07),
    #     (tMatrix(-.15,.28,.26,.24,0,.44),.07),
    #     (tMatrix(.85,.04,-.04,.85,0,1.6),.85)
    # ]
    # dim = [-3,3,0,10]
    # p = (0,0)
    # q = (0,0)

    ### koch snowflake (hexagon generation)
    # ifs = [
    #     (tMatrix(.5,-rt3/6.0,rt3/6.0,.5,0,0),1),
    #     (tMatrix(1/3.0,0,0,1/3.0,1/rt3,1/3.0),1),
    #     (tMatrix(1/3.0,0,0,1/3.0,0,2/3.0),1),
    #     (tMatrix(1/3.0,0,0,1/3.0,-1/rt3,1/3.0),1),
    #     (tMatrix(1/3.0,0,0,1/3.0,-1/rt3,-1/3.0),1),
    #     (tMatrix(1/3.0,0,0,1/3.0,0,-2/3.0),1),
    #     (tMatrix(1/3.0,0,0,1/3.0,1/rt3,-1/3.0),1)
    # ]
    # dim = [-1,1,-1,1]
    # p = (0,1)
    # q = (0,1)

    ### koch snowflake (dragon generation)
    ### http://ecademy.agnesscott.edu/~lriddle/ifs/ksnow/IFSdetailsLineFractal.htm
    # ifs = [
    #     (tMatrix(-1/6.,rt3/6.,-rt3/6.,-1/6.,1/6.,rt3/6.),1),
    #     (tMatrix(1/6.,-rt3/6.,rt3/6.,1/6.,1/6.,rt3/6.),1),
    #     (tMatrix(1/3.,0,0,1/3.,1/3.,rt3/3.),1),
    #     (tMatrix(1/6.,rt3/6.,-rt3/6.,1/6.,2/3.,rt3/3.),1),
    #     (tMatrix(.5,-rt3/6.,rt3/6.,.5,1/3.,0),1),
    #     (tMatrix(-1/3.,0,0,-1/3.,2/3.,0),1),
    #     (tMatrix(1/3.,0,0,1/3.,2/3.,0),1)
    # ]
    # dim = [0,1,-rt3/6.,rt3/2.]
    # p = (0,0)
    # q = (0,0)

    ### pentigree
    # ifs = [
    #     (tMatrix(.309,-.255,.255,.309,0,0),1),
    #     (tMatrix(-.118,-.363,.363,-.118,.309,.225),1),
    #     (tMatrix(.309,.255,-.255,.309,.191,.588),1),
    #     (tMatrix(-.118,.363,-.363,-.118,.5,.363),1),
    #     (tMatrix(.309,.255,-.255,.309,.382,0),1),
    #     (tMatrix(.309,-.255,.255,.309,.691,-.225),1)
    # ]
    # dim = [-.1,1.1,-.3,.8]
    # p = (1,0)
    # q = (1,0)

    qlim = 5 # max depth
    qcount = 0
    qlast = []
    qmem = 10 # max memory

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                return
        for i in xrange(500):
            screen.fill((255,255,255), ((round(bs+((p[0]-dim[0])/float(dim[1]-dim[0]))*ds),round(bs+(1-(p[1]-dim[2])/float(dim[3]-dim[2]))*ds)), (1, 1)))
            screen.fill((255,255,255), ((round(ws+bs+((q[0]-dim[0])/float(dim[1]-dim[0]))*ds),round(bs+(1-(q[1]-dim[2])/float(dim[3]-dim[2]))*ds)), (1, 1)))
            # if i == 499:
            #     ld = density(bs,bs,ds,ds,screen)
            #     rd = density(bs+ws,bs,ds,ds,screen)
            #     print "{:.5f},{:.5f},{:.5f}".format(ld, rd, ld/rd)
            if qcount < qlim:
                qcount += 1
                q = roulette(ifs)(*q)
                qlast.append(q)
                if len(qlast) > qmem:
                    qlast.pop(0)
            else:
                qcount = 0
                q = random.choice(qlast)
                # q = (0,.5)
            if 1:
                p = roulette(ifs)(*p)
        pygame.display.update()

if __name__ == '__main__': main()
