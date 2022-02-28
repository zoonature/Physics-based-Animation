from vpython import *
GlowScript 3.0 VPython

# 수조, 박스 만들기
# 투명도 50% 적용
water = box(size = vec(10,10,10), color = color.blue, opacity = 0.5)
wood = box(pos = vec(0,10,0), size = vec(2,2,2), texture = textures.wood)

# 물리 성질 & 상수 초기화
wood.v = vec(0,0,0) #박스 초기속도
wood.rho = 500 #박스 밀도
wood.volume = wood.size.x*wood.size.y*wood.size.z #박스 부피
wood.volume_im = 0 #물에 잠긴 박스 부피
wood.m = wood.rho*wood.volume #박스 질량
water.rho = 1000 #물 밀도
air_rho = 1.2 #공기 밀도
rho = air_rho #현재 공기 중
Cd = 1.06 #저항계수
g = vec(0,-9.8,0) #중력가속도

# 시간 설정
t = 0
dt = 0.001

# 바닥과의 충돌처리 함수
def collision_with_bottom(pBox,pbox):
    col_check = (pbox.pos.y - 0.5*pbox.size.y) - (pBox.pos.y - 0.5*pBox.size.y)
    if col_check < 0:
        return True
    else:
        return False

# 잠긴 부피와 밀도 계산 함수     
def calc_im(pBox,pbox): 
    float_height = (pbox.pos.y + 0.5*pbox.size.y) - (pBox.pos.y + 0.5*pBox.size.y)
    if float_height < 0:
        pbox.volume_im = pbox.volume
    else:
        pbox.volume_im = max(0, pbox.volume - float_height *  pbox.size.x * pbox.size.z)
    if pbox.volume_im > 0:
        rho = water.rho
    else:
        rho = air_rho
    return pbox.volume_im, rho

# 화면 설정
scene.waitfor('click')

# 시뮬레이션 루프
while t < 100:
    rate(1/dt)
    # 충돌 확인
    if collision_with_bottom(water, wood):
        print("collision!")
        break
    # 잠긴정도에 따라서 부피와 밀도 변경
    wood.volume_im, rho = calc_im(water, wood)
    
    # 중력
    grav = wood.m*g
    # 부력
    bouy = -water.rho*wood.volume_im*g
    # 저항력
    drag = -0.5*rho*Cd*(wood.size.x*wood.size.y)*mag(wood.v)**2*norm(wood.v)
  
    # 알짜힘
    wood.f = grav + bouy + drag
    
    # 속도, 위치 업데이트
    wood.v = wood.v + wood.f/wood.m*dt
    wood.pos = wood.pos + wood.v*dt
    
    # 시간 업데이트
    t = t + dt
