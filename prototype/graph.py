import numpy as np
from scipy.integrate import solve_ivp
import tkinter as tk

# 파라미터 설정
m1 = 250  # 차체 질량 (kg)
m2 = 50   # 휠 질량 (kg)
k1 = 80000  # 서스펜션 스프링 상수 (N/m)
k2 = 500000  # 타이어 스프링 상수 (N/m)
c1 = 1000   # 서스펜션 댐퍼 계수 (Ns/m)
c2 = 2000   # 타이어 댐퍼 계수 (Ns/m)

# 초기 조건 설정 (초기 위치와 속도)
initial_conditions = [0.0, 0.0, 0.0, 0.0]  # [x1, v1, x2, v2]

# 도로 입력 함수 정의
def road_input(t, bumpstart, bumpend, bumpamp):
    if bumpstart <= t <= bumpend:
        return bumpamp * np.sin(np.pi * (t - bumpstart) / (bumpend - bumpstart))
    else:
        return 0

# 요철 파라미터 설정
bumpstart = 2.0  # 요철 시작 시간 (s)
bumpend = 2.5    # 요철 종료 시간 (s)
bumpamp = 0.001   # 요철 진폭 (m)

# 시스템의 미분 방정식 정의
def quarter_car_model(t, y):
    x1, v1, x2, v2 = y
    z = road_input(t, bumpstart, bumpend, bumpamp)
    
    dx1_dt = v1
    dv1_dt = (1/m1) * (-k1*(x1-x2) - c1*(v1-v2))
    dx2_dt = v2
    dv2_dt = (1/m2) * (k1*(x1-x2) + c1*(v1-v2) - k2*(x2-z) - c2*(v2-0))
    
    return [dx1_dt, dv1_dt, dx2_dt, dv2_dt]

# 시간 범위 설정
t_span = [0, 5]
t_eval = np.linspace(t_span[0], t_span[1], 1000)

# 미분 방정식 풀이
sol = solve_ivp(quarter_car_model, t_span, initial_conditions, t_eval=t_eval)

# tkinter 윈도우 설정
root = tk.Tk()
root.title("Quarter Car Simulation")

# Canvas 설정
canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.pack()

# 스케일 설정
scale_x = 160  # 시간 5초를 800 픽셀에 매핑
scale_y = 4000  # 변위 0.01m를 40 픽셀에 매핑 (진폭 기준)

# 도로 입력 그리기
road_points = [(t * scale_x, 200 - road_input(t, bumpstart, bumpend, bumpamp) * scale_y) for t in sol.t]
for i in range(len(road_points) - 1):
    canvas.create_line(road_points[i][0], road_points[i][1], road_points[i + 1][0], road_points[i + 1][1], fill="black", dash=(2, 2))

# 애니메이션 설정
body = canvas.create_oval(0, 0, 20, 20, fill="blue")
wheel = canvas.create_oval(0, 0, 20, 20, fill="red")

def animate(i):
    body_x = sol.t[i] * scale_x
    body_y = 180 - sol.y[0, i] * scale_y  # body_y를 wheel_y보다 20픽셀 위로 설정
    wheel_x = sol.t[i] * scale_x
    wheel_y = 200 - sol.y[2, i] * scale_y
    
    canvas.coords(body, body_x - 10, body_y - 10, body_x + 10, body_y + 10)
    canvas.coords(wheel, wheel_x - 10, wheel_y - 10, wheel_x + 10, wheel_y + 10)
    
    if i < len(sol.t) - 1:
        root.after(20, animate, i + 1)

# 애니메이션 시작
root.after(0, animate, 0)

# 종료 버튼 추가
def on_closing():
    root.quit()
    root.destroy()

button = tk.Button(root, text="Quit", command=on_closing)
button.pack(side=tk.BOTTOM)

# tkinter 메인 루프 시작
tk.mainloop()
