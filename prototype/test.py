import numpy as np
from scipy.integrate import odeint

# 입력 변수 정의
M_s = 250.0  # 스프렁 질량 (kg)
M_u = 50.0   # 언스프렁 질량 (kg)
K_s = 15000.0  # 스프링 상수 (N/m)
K_t = 200000.0 # 타이어 강성 (N/m)
C = 1000.0   # 댐퍼 상수 (Ns/m)

# 도로 입력 (도로의 불규칙성 변위)
def road_input(t):
    return np.sin(t)  # 예제: sin 함수 형태의 도로 입력

# 초기 조건
x_s0 = 0.1    # 초기 차체 변위 (m)
v_s0 = 0.0    # 초기 차체 속도 (m/s)
x_u0 = 0.0    # 초기 바퀴 변위 (m)
v_u0 = 0.0    # 초기 바퀴 속도 (m/s)
initial_conditions = [x_s0, v_s0, x_u0, v_u0]

# 샘플링 시간 정의
sampling_time = 0.01  # 샘플링 시간 (초)
total_time = 10.0  # 전체 시뮬레이션 시간 (초)
t = np.arange(0, total_time, sampling_time)  # 샘플링 시간 간격으로 시간 배열 생성

# 차체의 가속도 함수 정의
def a_s_function(v_s, v_u, x_s, x_u, x_r):
    return (-K_s * (x_s - x_u) - C * (v_s - v_u)) / M_s

# 바퀴의 가속도 함수 정의
def a_u_function(v_s, v_u, x_s, x_u, x_r):
    return (K_s * (x_s - x_u) + C * (v_s - v_u) - K_t * (x_u - x_r)) / M_u

# 운동 방정식
def quarter_car_model(y, t):
    x_s, v_s, x_u, v_u = y
    x_r = road_input(t)
    
    # 차체의 가속도
    a_s = a_s_function(v_s, v_u, x_s, x_u, x_r)
    
    # 바퀴의 가속도
    a_u = a_u_function(v_s, v_u, x_s, x_u, x_r)
    
    return [v_s, a_s, v_u, a_u]

# 방정식 풀기
solution = odeint(quarter_car_model, initial_conditions, t)

# 결과에서 각 변수 추출
x_s = solution[:, 0]
v_s = solution[:, 1]

# 속도를 이용하여 이동 거리 계산
distance = np.trapz(v_s, t)

# 차체의 위치 계산
x_s_position = np.cumsum(v_s) * sampling_time

# 결과 출력
print(f"차체의 가속도와 바퀴의 가속도를 반영한 총 이동 거리: {distance:.2f} m")
print("시간에 따른 x축 좌표 위치:")
for i, x_position in enumerate(x_s_position):
    print(f"시간: {t[i]:.2f} s, x축 좌표 위치: {x_position:.2f} m")
    if (x_position > 0.9):
        break
