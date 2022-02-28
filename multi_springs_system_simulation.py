from vpython import *
GlowScript 3.0 VPython

## UI
drag = False
chosenObj = None

def down():
    global drag, chosenObj
    chosenObj = scene.mouse.pick()
    drag = True

def up():
    global drag, chosenObj
    chosenObj = None
    drag = False

def move():
    global drag, chosenObj, ballNum, ball, spring
    if drag == True:
        if chosenObj == ball[0]:
            ball[0].pos = scene.mouse.pos
            spring[0].axis = ball[0].pos - ceiling.pos
            spring[1].pos = ball[0].pos
            spring[1].axis = ball[1].pos - ball[0].pos
        for i in range(1, ballNum-1):
            if chosenObj == ball[i]:
                ball[i].pos = scene.mouse.pos
                spring[i].axis = ball[i].pos - ball[i-1].pos
                spring[i+1].pos = ball[i].pos
                spring[i+1].axis = ball[i+1].pos - ball[i].pos
        if chosenObj == ball[ballNum-1]:
            ball[ballNum-1].pos = scene.mouse.pos
            spring[ballNum-1].axis = ball[ballNum-1].pos - ball[ballNum-2].pos
            
scene.bind("mousedown", down)
scene.bind("mouseup", up)
scene.bind("mousemove", move)


## Object
ceiling = box(pos = vec(0,0,0), size = vec(0.3, 0.01, 0.3))

ballNum = int(input('how many balls?'))
ball = list()
spring = list()

#list() -> append안하고 index로 초기화 가능
for i in range(ballNum):
    ball[i] = sphere(pos = vec(0, -0.25*(i+1), 0), radius = 0.03, texture = textures.metal)

for i in range(ballNum):
    if (i==0):
        spring[i] = helix(pos = ceiling.pos, axis = ball[0].pos-ceiling.pos, color = color.black, thickness = 0.003, coils = 30, radius = 0.01)
    else:
        spring[i] = helix(pos = ceiling.pos + ball[i-1].pos, axis = ball[i].pos - ball[i-1].pos, color = color.black, thickness = 0.003, coils = 30, radius = 0.01)


#physical properties & const.
g = 9.8
m = 1    # mass
ks = 100 # stiffness coeff.
kd = 1  # damping coeff.

l0 = 0.25   # rest length

#initialize velocity
for i in range(ballNum):
    ball[i].v = vec(0,0,0)
    
#time setting
t = 0
dt = 0.01

#display
scene.background = color.white   
scene.autoscale = False     
scene.center = vec(0, -l0*ballNum/2, 0)
scene.waitfor('click') 

#simulation loop
while True:
    rate(1/dt)
    Fgrav = m*g*vec(0,-1,0)
    for i in range(ballNum):
        if(i==0):
            l = mag(ball[i].pos - ceiling.pos) #spring mag
            s = l-l0
            lhat = norm(ball[i].pos - ceiling.pos) #spring norm vector
            
            #damping force
            ball[i].Fdamp = -kd*dot(ball[i].v , lhat)*lhat
        else:
            l = mag(ball[i].pos - ball[i-1].pos)
            s = l - l0
            lhat = norm(ball[i].pos - ball[i-1].pos)
            #damping force
            ball[i].Fdamp = -kd*dot(ball[i].v-ball[i-1].v, lhat)*lhat
        
        #spring force
        ball[i].Fspr = -ks*s*lhat
    
    
    for i in range(ballNum):
        if(i==ballNum-1):
            ball[i].Fnet = Fgrav + ball[i].Fspr+ball[i].Fdamp
        else:
            ball[i].Fnet = Fgrav + ball[i].Fspr + ball[i].Fdamp - ball[i+1].Fspr - ball[i+1].Fdamp
    
    for i in range(ballNum):
        Fnet = ball[i].Fnet
        ball[i].v = ball[i].v + Fnet/m * dt
        ball[i].pos = ball[i].pos + ball[i].v * dt
        
        if (i==0):
            spring[i].axis = ball[i].pos - ceiling.pos
        else:
            spring[i].pos = ball[i-1].pos
            spring[i].axis = ball[i].pos - ball[i-1].pos
    
    t = t + dt
    
    if drag == True:
        for i in range(ballNum):
            ball[i].Fnet = vec(0,0,0)
            ball[i].v = vec(0,0,0)
    
