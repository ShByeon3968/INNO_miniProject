import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt

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
x_s0 = 0.0    # 초기 차체 변위 (m)
v_s0 = 0.0    # 초기 차체 속도 (m/s)
x_u0 = 0.0    # 초기 바퀴 변위 (m)
v_u0 = 0.0    # 초기 바퀴 속도 (m/s)
initial_conditions = [x_s0, v_s0, x_u0, v_u0]

# 샘플링 시간 정의
sampling_time = 0.01  # 샘플링 시간 (초)
total_time = 10.0  # 전체 시뮬레이션 시간 (초)
t = np.arange(0, total_time, sampling_time)  # 샘플링 시간 간격으로 시간 배열 생성

# 운동 방정식
def quarter_car_model(y, t, M_s, M_u, K_s, K_t, C):
    x_s, v_s, x_u, v_u = y
    x_r = road_input(t)
    
    # 차체의 가속도
    a_s = (-K_s * (x_s - x_u) - C * (v_s - v_u)) / M_s
    
    # 바퀴의 가속도
    a_u = (K_s * (x_s - x_u) + C * (v_s - v_u) - K_t * (x_u - x_r)) / M_u
    
    return [v_s, a_s, v_u, a_u]

# 방정식 풀기
solution = odeint(quarter_car_model, initial_conditions, t, args=(M_s, M_u, K_s, K_t, C))

# 결과에서 각 변수 추출
x_s = solution[:, 0]
x_u = solution[:, 2]

# 결과 시각화
plt.figure(figsize=(10, 6))
plt.plot(t, x_s, label='Sprung Mass Displacement (x_s)')
plt.plot(t, x_u, label='Unsprung Mass Displacement (x_u)')
plt.plot(t, road_input(t), label='Road Input (x_r)', linestyle='--')
plt.xlabel('Time (s)')
plt.ylabel('Displacement (m)')
plt.title('Quarter Car Model Response')
plt.legend()
plt.grid()
plt.show()
