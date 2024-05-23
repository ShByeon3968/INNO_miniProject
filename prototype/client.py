import socket
import tkinter as tk

def send_message():
    global M_s, M_u, K_s, K_t, c1, c2, sampling_time, total_time
    M_s = entry_M_s.get()
    M_u = entry_M_u.get()
    K_s = entry_K_s.get()
    K_t = entry_K_t.get()
    c1 = entry_c1.get()
    c2 = entry_c2.get()
    sampling_time = entry_sampling_time.get()
    total_time = entry_total_time.get()
    
    message = f"M_s={M_s},M_u={M_u},K_s={K_s},K_t={K_t},c1={c1},c2={c2},sampling_time={sampling_time},total_time={total_time}"
    client_socket.send(message.encode('utf-8'))

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = entry_ip.get()
    client_socket.connect((server_ip, 9999))
    print(f"서버 {server_ip}에 연결됨")

def run_gui():
    global entry_ip, entry_M_s, entry_M_u, entry_K_s, entry_K_t, entry_c1, entry_c2, entry_sampling_time, entry_total_time
    root = tk.Tk()
    root.title("클라이언트")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    label_ip = tk.Label(frame, text="서버 IP:")
    label_ip.pack(side=tk.LEFT)
    
    entry_ip = tk.Entry(frame, width=20)
    entry_ip.pack(side=tk.LEFT)

    button_connect = tk.Button(frame, text="연결", command=connect_to_server)
    button_connect.pack(side=tk.LEFT)

    # 입력 필드
    fields = [
        ("스프렁 질량 (kg)", "250.0"),
        ("언스프렁 질량 (kg)", "50.0"),
        ("스프링 상수 (N/m)", "15000.0"),
        ("타이어 강성 (N/m)", "200000.0"),
        ("서스펜션 댐퍼 계수 (Ns/m)", "1000.0"),
        ("타이어 댐퍼 계수 (Ns/m)", "2000.0"),
        ("샘플링 시간 (초)", "0.01"),
        ("전체 시뮬레이션 시간 (초)", "10.0")
    ]

    entries = {}
    for label_text, default_value in fields:
        frame = tk.Frame(root)
        frame.pack(pady=2)
        label = tk.Label(frame, text=label_text, width=20, anchor='w')
        label.pack(side=tk.LEFT)
        entry = tk.Entry(frame, width=20)
        entry.pack(side=tk.LEFT)
        entry.insert(0, default_value)
        entries[label_text] = entry

    entry_M_s = entries["스프렁 질량 (kg)"]
    entry_M_u = entries["언스프렁 질량 (kg)"]
    entry_K_s = entries["스프링 상수 (N/m)"]
    entry_K_t = entries["타이어 강성 (N/m)"]
    entry_c1 = entries["서스펜션 댐퍼 계수 (Ns/m)"]
    entry_c2 = entries["타이어 댐퍼 계수 (Ns/m)"]
    entry_sampling_time = entries["샘플링 시간 (초)"]
    entry_total_time = entries["전체 시뮬레이션 시간 (초)"]

    button_send = tk.Button(root, text="전송", command=send_message)
    button_send.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    run_gui()
