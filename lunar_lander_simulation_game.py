from vpython import *
GlowScript 3.0 VPython

# 화면 설정
scene.range = 20

#높이 설정
height = -10.05

#배경 (curve() 이용)
obs = curve()
obspos = list()

#착륙지점 생성
land = list()
landpos = list()
landcount = 0

interval = 0 
st = True #시작지점인지 아닌지 판별하기위한 변수

for i in range(40):
    flag = random()
    # 바닥에서시작
    if st == True:
        obspos.append(vec(random()*2+interval, height, 0))
        st = False
    else:
        if flag < 0.2 :
            temppos = vec(random()+interval, random()*10+random(), 0)
            obspos.append(temppos)
            flag2 = random()
            if flag2 < 0.5:
                landpos.append(temppos)
                landcount += 1
        elif flag < 0.4:
            temppos = vec(random()+interval, random()*10*2, 0)
            obspos.append(temppos)
            flag2 = random()
            if flag2 < 0.5:
                landpos.append(temppos)
                landcount += 1
        elif flag < 0.6:
            temppos = vec(random()+interval, random()*10*4, 0)
            obspos.append(temppos)
            flag2 = random()
            if flag2 < 0.5:
                landpos.append(temppos)
                landcount += 1
        else:
            obspos.append(vec(random()+interval, height, 0))
    interval += 10
obs.append(obspos)


for i in range(landcount):
    land.append(cylinder(pos = landpos[i], axis = vec(0, 1, 0), radius = 2, color = color.blue))

#달착륙선 만들기
spaceship = box(pos = vec(0,8,0), size = vec(2,5,2), color = color.yellow)


# 물리성질 & 상수 초기화
spaceship.m = 1 #달 착륙선 질량 
spaceship.v = vector (0 ,0 ,0) #달 착륙선 초기속도 
g = 1/6 * vector(0,-10,0) #달 중력가속도(지구의 1/6배)


# 시간 설정
t = 0
dt = 0.05

scale = 5.0 #크기조정을 위한 변수

#연료 & 점수 설정
fuel = 200
point = 0
gametxt = label( pos = scene.center - vec(scene.range, 0,0), text='left fuel : ' + fuel + '\n' + 'point : ' + point )


# 벡터 Fthrust 지정 (추력)
Fthrust  = vec(0,0,0) 


# 중력, 추력 벡터 표현
FgravArrow = arrow(pos = spaceship.pos, axis = scale*spaceship.m*g, color = color.red) 
FthrustArrow = arrow(pos = spaceship.pos, axis = Fthrust, color = color.cyan) 


# 키보드 조작 함수1 (키를 누를 경우)
def keydown(evt):
    # 키에 따라 추력벡터 값 변환
    s = evt.key 
    if s == 'left': 
        global Fthrust
        Fthrust = vec(-2,0,0) 
    if s == 'right':
        global Fthrust
        Fthrust = vec(2,0,0)

# 키보드 조작 함수2 (키를 눌렀다 뗄 경우)
def keyup(evt):
    # 추력 제거
    s = evt.key
    if s == 'left' or s == 'right' : 
        global Fthrust
        global fuel
        Fthrust = vec(0,0,0)
        fuel -=5
        
        
clickcount = 0 #클릭횟수

# 마우스 조작 함수1 (마우스 버튼이 눌릴 경우 추력벡터의 y값 변환)
def down(ev):
    global Fthrust
    global fuel
    global clickcount
    #처음 클릭시 연료 사용 X(waitfor에서 사용)
    if clickcount != 0:
        fuel -= 5
    clickcount +=1
    Fthrust = vec(0,4,0)

# 마우스 조작 함수2 (마우스 버튼을 눌렀다 뗄 경우 추력 제거)
def up(ev):
    global Fthrust
    Fthrust = vec(0,0,0)


# 키보드/마우스 조작함수 등록
scene.bind('mouseup', up)
scene.bind('mousedown', down)
scene.bind('keydown', keydown)
scene.bind('keyup', keyup)
scene.waitfor('click')


Flag = True #중력이 작용하는지 체크
cFlag = False #충돌이 된 상태인지 체크


# 시뮬레이션 루프
while t < 1000:
    rate(100)
    
    
    if Flag == True:
        Fgrav = spaceship.m * g
        Fnet = Fgrav + Fthrust
    else:
        scene.waitfor('click')
        Fthrust = vec(0,4,0)
        Flag = True
        cFlag = True
    
    if (spaceship.pos.y - spaceship.size.y/2) - (land[i].pos.y + land[i].size.y/2) > 1 and cFlag == True:
            cFlag = False
            Flag = True
            Fthrust = vec(0,0,0)
            
        
    spaceship.v = spaceship.v + Fnet/spaceship.m*dt 
    spaceship.pos = spaceship.pos + spaceship.v*dt
            
    if cFlag == False :
        for i in range(landcount):
            if abs(spaceship.pos.x - land[i].pos.x) < 2 and 0 <= (spaceship.pos.y - spaceship.size.y/2) - (land[i].pos.y + land[i].size.y/2) <= 0.5:
                Flag = False
                spaceship.pos = vec(land[i].pos.x, land[i].pos.y + spaceship.size.y/2, 0)
                spaceship.v = vec(0,0,0)
                point += 5 
                break
    
    #연료&점수 라벨 업데이트
    gametxt.pos = scene.center - vec(scene.range, 0,0)
    gametxt.text = 'left fuel : ' + fuel + '\n' + 'point : ' + point 
    
    #화면 업데이트
    scene.center = vec(spaceship.pos.x, 0,0)
    if spaceship.pos.y > 20:
        scene.range = spaceship.pos.y + 5
    
    # 중력, 추력벡터 업데이트 
    FgravArrow.pos = spaceship.pos
    FgravArrow.axis = scale*Fgrav
    FthrustArrow.pos = spaceship.pos
    FthrustArrow.axis = scale*Fthrust
    
    if fuel <= 0:
        print("연료부족")
        spaceship.pos = vec(spaceship.pos.x, height, 0)
        FgravArrow.visible = False
        FthrustArrow.visible = False
        break
    
    if spaceship.pos.y < height:
        print("바닥과충돌")
        break
    
    # 시간 업데이트
    t = t + dt

