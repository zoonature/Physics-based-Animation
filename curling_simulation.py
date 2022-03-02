from vpython import *
GlowScript 3.1 VPython


# stone radius
r = 0.9144/(2*pi) ##m

# ground size
GROUND_SIZEX = 45.720 ##m
GROUND_SIZEY = 5 ##m
GROUND_SIZEZ = 1 ##m

# object
sheet = box(size = vec(GROUND_SIZEX, GROUND_SIZEY, GROUND_SIZEZ), color = color.white)
wall1 = box(pos = vec(0, GROUND_SIZEY/2+0.1, 0.25), size = vec(GROUND_SIZEX, 0.2, 1.5))
wall1 = box(pos = vec(0, -GROUND_SIZEY/2-0.1, 0.25), size = vec(GROUND_SIZEX, 0.2, 1.5))

startPoint = box(pos = vec(-GROUND_SIZEX/2+1.22,0,0), size = vec(0.1, 1, GROUND_SIZEZ+0.01), color = color.black)
endPoint = box(pos = vec(GROUND_SIZEX/2-1.22,0,0), size = vec(0.1, 1, GROUND_SIZEZ+0.01), color = color.black)


start_circle_1st = cylinder(pos = vec(startPoint.pos.x + 3.66, 0, -0.496), axis = vec(0,0,1), radius = 0.15, color = color.white)
start_circle_2nd = cylinder(pos = vec(startPoint.pos.x + 3.66, 0, -0.497), axis = vec(0,0,1), radius = 0.61, color = color.red)
start_circle_3rd = cylinder(pos = vec(startPoint.pos.x + 3.66, 0, -0.498), axis = vec(0,0,1), radius = 1.22, color = color.white)
start_circle_4th = cylinder(pos = vec(startPoint.pos.x + 3.66, 0, -0.499), axis = vec(0,0,1), radius = 1.83, color = color.blue)

end_circle_1st = cylinder(pos = vec(endPoint.pos.x - 3.66, 0, -0.496), axis = vec(0,0,1), radius = 0.15, color = color.white)
end_circle_2nd = cylinder(pos = vec(endPoint.pos.x - 3.66, 0, -0.497), axis = vec(0,0,1), radius = 0.61, color = color.red)
end_circle_3rd = cylinder(pos = vec(endPoint.pos.x - 3.66, 0, -0.498), axis = vec(0,0,1), radius = 1.22, color = color.white)
end_circle_4th = cylinder(pos = vec(endPoint.pos.x - 3.66, 0, -0.499), axis = vec(0,0,1), radius = 1.83, color = color.blue)


sf = 3

stone = cylinder(pos = vec(-20, 0,1) , axis = vec(0,0,0.1143), radius = r, color = color.black)
stone.radius = stone.radius * sf


# constant and physical properties (related to Force, acc, vel, m)
g = 9.8 #수직항력을 구하려고
mu = 0.05 #ice -> very small
stone.a = vec(0,0,0) #m/s^2
stone.v = vec(5,0,0) ##m/s
stone.m = 19.96 ##kg 

#button
#button activate -> what to do? -> disable 하게함
def drawBtn(b):
    b.disabled = True
    return b.disabled
btnDraw = button(text = 'Draw', bind = drawBtn)


#slider
def myVelocity():
    global stone #전역변수
    stone.v = velocitySlider.value * vec(1,0,0)
velocitySlider = slider(min = 3, max = 7, value = 5, bind = myVelocity)


# time setting
t = 0
dt = 0.01


# simulation loop
while True:
    rate(1/dt)
    if btnDraw.disabled == True:
        # force update (friction)
        Ffr = -mu*stone.m*g*norm(stone.v)
        
        # a, v, p update
        stone.v = stone.v + Ffr/stone.m * dt
        stone.pos = stone.pos + stone.v * dt
        
        
        # ==0 : break
        # 0.01 -> -0.01
        
        if mag(stone.v) < 0.05:
            stone.v = vec(0,0,0)
            
            scene.waitfor('click')
            btnDraw.disabled = False
            stone.pos = vec(-20, 0, 1)
            t = 0
            
        
        t = t + dt
    

