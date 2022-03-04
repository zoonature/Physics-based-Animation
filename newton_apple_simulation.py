from vpython import *
GlowScript 3.1 VPython

ground = box(pos = vec(0,0,0), size = vec(20,0.1, 10), color = color.white)
tree = cylinder (pos = vec(-5, 0,0), axis = vec(0,4, 0), color = vec(111/256, 79/256,40/256), radius = 0.5)
leaf = sphere(pos = vec(tree.pos.x, tree.pos.y+tree.axis.y, 0), radius = 1.5, color = color.green)
apple_radius = 0.1
apple = sphere(pos = vec(tree.pos.x + leaf.radius + apple_radius, tree.pos.y+tree.axis.y, 0), color = color.red, radius = apple_radius)
car_height= 0.5
car = box(pos = vec(apple.pos.x,car_height/2,0), size = vec(1, 0.5,1), color = color.blue)

#si unit 
apple.m = 0.5 #kg
g_earth = vec(0,-9.81,0)
g_moon = g_earth/6;


apple.a = vec(0,0,0)
apple.v = vec(2,5,0)
car.a = vec(2.6,0,0) #v-t graph
car.v = vec(0,0,0)


t = 0
dt = 0.01

scene.waitfor('click')

while (True) :
    rate(1/dt)
    
    F_grav = apple.m * g_earth #F = mg
    apple.a = F_grav/apple.m #a = F/m 
        
    apple.v = apple.v + apple.a * dt
    apple.pos = apple.pos + apple.v * dt
    
    car.v = car.v + car.a * dt
    car.pos = car.pos + car.v * dt
    
    if (apple.pos.y < ground.pos.y):
        print("time = ", t)
        break
    
    t = t + dt
    
