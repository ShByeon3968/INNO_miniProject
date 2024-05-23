import socket
import threading
import tkinter as tk
from tkinter import ttk, filedialog
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.integrate import odeint
import csv

class CarSimulationApp:
    def __init__(self, root, t, distance_A, distance_B, sampling_time):
        self.root = root
        self.t = t
        self.distance_A = distance_A
        self.distance_B = distance_B
        self.sampling_time = sampling_time

        screen_height = self.root.winfo_screenheight()
        self.canvas = tk.Canvas(root, width=800, height=screen_height // 3, bg='white')
        self.canvas.pack(pady=10)

        self.car_A = self.canvas.create_rectangle(50, 50, 100, 100, fill='blue', outline='blue', tags="car_A")
        self.car_B = self.canvas.create_rectangle(50, screen_height // 3 - 100, 100, screen_height // 3 - 50, fill='red', outline='red', tags="car_B")

        # Entry fields for x position
        self.x_start_A = tk.DoubleVar(value=0.0)
        self.x_end_A = tk.DoubleVar(value=1.0)
        self.x_start_B = tk.DoubleVar(value=0.0)
        self.x_end_B = tk.DoubleVar(value=1.0)

        tk.Label(root, text="Car A Start X").pack(side=tk.LEFT)
        self.entry_x_start_A = tk.Entry(root, textvariable=self.x_start_A)
        self.entry_x_start_A.pack(side=tk.LEFT)

        tk.Label(root, text="Car A End X").pack(side=tk.LEFT)
        self.entry_x_end_A = tk.Entry(root, textvariable=self.x_end_A)
        self.entry_x_end_A.pack(side=tk.LEFT)

        tk.Label(root, text="Car B Start X").pack(side=tk.LEFT)
        self.entry_x_start_B = tk.Entry(root, textvariable=self.x_start_B)
        self.entry_x_start_B.pack(side=tk.LEFT)

        tk.Label(root, text="Car B End X").pack(side=tk.LEFT)
        self.entry_x_end_B = tk.Entry(root, textvariable=self.x_end_B)
        self.entry_x_end_B.pack(side=tk.LEFT)

        self.frame_idx = 0
        self.update_simulation()

    def update_simulation(self):
        if self.frame_idx < len(self.t):
            screen_height = self.root.winfo_screenheight()

            # Update the car positions based on the y-displacement and x-range
            y_A = 50 + (self.distance_A[self.frame_idx] * (screen_height // 3 - 100))
            y_B = (screen_height // 3 - 100) - (self.distance_A[self.frame_idx] * (screen_height // 3 - 100))

            x_range_A = self.x_end_A.get() - self.x_start_A.get()
            x_A = 50 + (self.x_start_A.get() * 700) + (self.distance_A[self.frame_idx] * x_range_A * 700)
            
            x_range_B = self.x_end_B.get() - self.x_start_B.get()
            x_B = 50 + (self.x_start_B.get() * 700) + (self.distance_A[self.frame_idx] * x_range_B * 700)

            self.canvas.coords(self.car_A, x_A, y_A, x_A + 50, y_A + 50)
            self.canvas.coords(self.car_B, x_B, y_B, x_B + 50, y_B + 50)

            self.frame_idx += 1
            self.root.after(int(self.sampling_time * 1000), self.update_simulation)

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', 9999))
    server_socket.listen(5)
    print("서버 시작됨, 포트 9999에서 대기 중...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"연결됨: {addr}")
        threading.Thread(target=handle_client, args=(client_socket,)).start()

def handle_client(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"메시지 수신됨: {message}")
            process_message(message)
        except:
            break
    client_socket.close()

def process_message(message):
    global text_widget, plot_button, save_button, var_dict

    variables = message.split(',')
    var_dict = {}
    
    for var in variables:
        name, value = var.split('=')
        var_dict[name] = float(value)
    
    formatted_message = (
        f"M_s: {var_dict['M_s']} kg\n"
        f"M_u: {var_dict['M_u']} kg\n"
        f"K_s: {var_dict['K_s']} N/m\n"
        f"K_t: {var_dict['K_t']} N/m\n"
        f"C: {var_dict['C']} Ns/m\n"
        f"sampling_time: {var_dict['sampling_time']} s\n"
        f"total_time: {var_dict['total_time']} s\n"
    )
    
    text_widget.insert(tk.END, formatted_message + '\n')
    plot_button.config(state=tk.NORMAL)
    save_button.config(state=tk.NORMAL)

def run_simulation():
    global var_dict, canvas, figure, x_s, x_u, x_r, t, v_s, distance_A, distance_B
    
    M_s = var_dict['M_s']
    M_u = var_dict['M_u']
    K_s = var_dict['K_s']
    K_t = var_dict['K_t']
    C = var_dict['C']
    sampling_time = var_dict['sampling_time']
    total_time = var_dict['total_time']

    t = np.arange(0, total_time, sampling_time)

    def road_input(t):
        return 0.1 * np.sin(2 * np.pi * 0.5 * t)

    def quarter_car_model(y, t, M_s, M_u, K_s, K_t, C):
        x_s, v_s, x_u, v_u = y
        x_r = road_input(t)
        a_s = (-K_s * (x_s - x_u) - C * (v_s - v_u)) / M_s
        a_u = (K_s * (x_s - x_u) + C * (v_s - v_u) - K_t * (x_u - x_r)) / M_u
        return [v_s, a_s, v_u, a_u]

    initial_conditions = [0.0, 0.0, 0.0, 0.0]
    solution = odeint(quarter_car_model, initial_conditions, t, args=(M_s, M_u, K_s, K_t, C))

    x_s = solution[:, 0]
    v_s = solution[:, 1]
    x_u = solution[:, 2]
    x_r = road_input(t)

    distance_A = np.cumsum(v_s) * sampling_time
    distance_B = 1.0 - distance_A

    figure.clear()
    
    ax1 = figure.add_subplot(131)
    ax1.plot(t, x_s, label='Sprung Mass (x_s)')
    ax1.set_xlabel('Time (s)')
    ax1.set_ylabel('Displacement (m)')
    ax1.set_title('Sprung Mass Displacement')
    ax1.legend()
    ax1.grid()

    ax2 = figure.add_subplot(132)
    ax2.plot(t, x_u, label='Unsprung Mass (x_u)')
    ax2.set_xlabel('Time (s)')
    ax2.set_title('Unsprung Mass Displacement')
    ax2.legend()
    ax2.grid()

    ax3 = figure.add_subplot(133)
    ax3.plot(t, x_r, label='Road Input (x_r)')
    ax3.set_xlabel('Time (s)')
    ax3.set_title('Road Input')
    ax3.legend()
    ax3.grid()

    canvas.draw()
    
    # Car simulation in GUI
    CarSimulationApp(root, t, distance_A, distance_B, sampling_time)


def save_csv():
    global x_s, x_u, x_r, t, var_dict
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if not filepath:
        return

    data = {'Time (s)': t}
    
    if var_dict['x_s']:
        data['Sprung Mass Displacement (x_s)'] = x_s
    if var_dict['x_u']:
        data['Unsprung Mass Displacement (x_u)'] = x_u
    if var_dict['x_r']:
        data['Road Input (x_r)'] = x_r

    with open(filepath, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        for i in range(len(t)):
            row = {key: data[key][i] for key in data}
            writer.writerow(row)

def run_gui():
    global text_widget, plot_button, save_button, var_dict, canvas, figure, root

    root = tk.Tk()
    root.title("서버 프로그램")
    root.geometry("1200x800")

    text_widget = tk.Text(root, height=10)
    text_widget.pack()

    plot_button = tk.Button(root, text="그래프 생성", command=run_simulation, state=tk.DISABLED)
    plot_button.pack()

    save_button = tk.Button(root, text="CSV 저장", command=save_csv, state=tk.DISABLED)
    save_button.pack()

    figure = plt.Figure(figsize=(10, 6), dpi=100)
    canvas = FigureCanvasTkAgg(figure, root)
    canvas.get_tk_widget().pack()

    check_frame = tk.Frame(root)
    check_frame.pack(pady=10)

    var_dict = {
        'x_s': tk.BooleanVar(),
        'x_u': tk.BooleanVar(),
        'x_r': tk.BooleanVar()
    }

    tk.Checkbutton(check_frame, text="Sprung Mass Displacement (x_s)", variable=var_dict['x_s']).pack(side=tk.LEFT)
    tk.Checkbutton(check_frame, text="Unsprung Mass Displacement (x_u)", variable=var_dict['x_u']).pack(side=tk.LEFT)
    tk.Checkbutton(check_frame, text="Road Input (x_r)", variable=var_dict['x_r']).pack(side=tk.LEFT)

    threading.Thread(target=start_server, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
