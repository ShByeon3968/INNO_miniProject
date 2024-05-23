import numpy as np
from scipy.integrate import solve_ivp
import tkinter as tk

# 도로 입력 함수 정의
def road_input(t, bumpstart, bumpend, bumpamp):
    if bumpstart <= t <= bumpend:
        return bumpamp * np.sin(np.pi * (t - bumpstart) / (bumpend - bumpstart))
    else:
        return 0

# 시스템의 미분 방정식 정의
def quarter_car_model(t, y, bumpstart, bumpend, bumpamp, m1, m2, k1, k2, c1, c2):
    x1, v1, x2, v2 = y
    z = road_input(t, bumpstart, bumpend, bumpamp)
    
    dx1_dt = v1
    dv1_dt = (1/m1) * (-k1*(x1-x2) - c1*(v1-v2))
    dx2_dt = v2
    dv2_dt = (1/m2) * (k1*(x1-x2) + c1*(v1-v2) - k2*(x2-z) - c2*(v2-0))
    
    return [dx1_dt, dv1_dt, dx2_dt, dv2_dt]

# 애니메이션 함수 정의
def animate(i, sol, scale_x, scale_y, wheelbase):
    global anim_id
    body_x = sol.t[i] * scale_x
    body_y = 180 - sol.y[0, i] * scale_y  # body_y를 wheel_y보다 약간 위로 설정
    wheel1_x = body_x - wheelbase / 2
    wheel1_y = 200 - sol.y[2, i] * scale_y
    wheel2_x = body_x + wheelbase / 2
    wheel2_y = 200 - sol.y[2, i] * scale_y

    # 각도 계산 (바퀴 간의 높이 차이로 인한 각도)
    angle = np.arctan2(wheel2_y - wheel1_y, wheel2_x - wheel1_x)
    angle_deg = np.degrees(angle)

    # 차체 회전
    canvas.coords(body, 
                  wheel1_x, body_y - 15, 
                  wheel1_x + wheelbase * np.cos(angle), body_y - 15 + wheelbase * np.sin(angle),
                  wheel1_x + wheelbase * np.cos(angle), body_y + 15 + wheelbase * np.sin(angle),
                  wheel1_x, body_y + 15)
    canvas.coords(wheel1, wheel1_x - 10, wheel1_y - 10, wheel1_x + 10, wheel1_y + 10)
    canvas.coords(wheel2, wheel2_x - 10, wheel2_y - 10, wheel2_x + 10, wheel2_y + 10)
    
    if i < len(sol.t) - 1:
        anim_id = root.after(20, animate, i + 1, sol, scale_x, scale_y, wheelbase)

# 시뮬레이션 시작 함수 정의
def start_simulation():
    global anim_id

    # 입력 값 가져오기
    m1 = float(entry_m1.get())
    m2 = float(entry_m2.get())
    k1 = float(entry_k1.get())
    k2 = float(entry_k2.get())
    c1 = float(entry_c1.get())
    c2 = float(entry_c2.get())
    bumpstart = float(entry_bumpstart.get())
    bumpend = float(entry_bumpend.get())
    bumpamp = float(entry_bumpamp.get())
    
    # 초기 조건 설정
    initial_conditions = [0.0, 0.0, 0.0, 0.0]  # [x1, v1, x2, v2]

    # 시간 범위 설정
    t_span = [0, 5]
    t_eval = np.linspace(t_span[0], t_span[1], 1000)

    # 미분 방정식 풀이
    sol = solve_ivp(quarter_car_model, t_span, initial_conditions, t_eval=t_eval, args=(bumpstart, bumpend, bumpamp, m1, m2, k1, k2, c1, c2))

    # 도로 입력 그리기
    canvas.delete("all")
    road_points = [(t * scale_x, 200 - road_input(t, bumpstart, bumpend, bumpamp) * scale_y) for t in sol.t]
    for i in range(len(road_points) - 1):
        canvas.create_line(road_points[i][0], road_points[i][1], road_points[i + 1][0], road_points[i + 1][1], fill="black", dash=(2, 2))

    global body, wheel1, wheel2
    body = canvas.create_polygon(0, 0, 0, 0, 0, 0, 0, 0, fill="blue")
    wheel1 = canvas.create_oval(0, 0, 20, 20, fill="red")
    wheel2 = canvas.create_oval(0, 0, 20, 20, fill="red")
    
    # 애니메이션 시작
    anim_id = root.after(0, animate, 0, sol, scale_x, scale_y, 40)

# 시뮬레이션 중지 함수 정의
def stop_simulation():
    global anim_id
    if anim_id is not None:
        root.after_cancel(anim_id)
        anim_id = None
        canvas.delete("all")

# tkinter 윈도우 설정
root = tk.Tk()
root.title("Quarter Car Simulation")

# 입력 위젯 생성
tk.Label(root, text="m1 (kg)").pack()
entry_m1 = tk.Entry(root)
entry_m1.pack()
entry_m1.insert(0, "250")

tk.Label(root, text="m2 (kg)").pack()
entry_m2 = tk.Entry(root)
entry_m2.pack()
entry_m2.insert(0, "50")

tk.Label(root, text="k1 (N/m)").pack()
entry_k1 = tk.Entry(root)
entry_k1.pack()
entry_k1.insert(0, "80000")

tk.Label(root, text="k2 (N/m)").pack()
entry_k2 = tk.Entry(root)
entry_k2.pack()
entry_k2.insert(0, "500000")

tk.Label(root, text="c1 (Ns/m)").pack()
entry_c1 = tk.Entry(root)
entry_c1.pack()
entry_c1.insert(0, "1000")

tk.Label(root, text="c2 (Ns/m)").pack()
entry_c2 = tk.Entry(root)
entry_c2.pack()
entry_c2.insert(0, "2000")

tk.Label(root, text="bumpstart (s)").pack()
entry_bumpstart = tk.Entry(root)
entry_bumpstart.pack()
entry_bumpstart.insert(0, "2.0")

tk.Label(root, text="bumpend (s)").pack()
entry_bumpend = tk.Entry(root)
entry_bumpend.pack()
entry_bumpend.insert(0, "2.5")

tk.Label(root, text="bumpamp (m)").pack()
entry_bumpamp = tk.Entry(root)
entry_bumpamp.pack()
entry_bumpamp.insert(0, "0.01")

# Canvas 설정
canvas = tk.Canvas(root, width=800, height=400, bg="white")
canvas.pack()

# 스케일 설정
scale_x = 160  # 시간 5초를 800 픽셀에 매핑
scale_y = 4000  # 변위 0.01m를 40 픽셀에 매핑 (진폭 기준)

# 시뮬레이션 제어 버튼
start_button = tk.Button(root, text="Start Simulation", command=start_simulation)
start_button.pack()

stop_button = tk.Button(root, text="Stop Simulation", command=stop_simulation)
stop_button.pack()

# 종료 버튼 추가
def on_closing():
    stop_simulation()
    root.quit()
    root.destroy()

quit_button = tk.Button(root, text="Quit", command=on_closing)
quit_button.pack(side=tk.BOTTOM)

# 애니메이션 ID 초기화
anim_id = None

# tkinter 메인 루프 시작
tk.mainloop()
