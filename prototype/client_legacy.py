import socket
import tkinter as tk

def send_message():
    message = entry.get()
    client_socket.send(message.encode('utf-8'))
    entry.delete(0, tk.END)

def connect_to_server():
    global client_socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = entry_ip.get()
    client_socket.connect((server_ip, 9999))
    print(f"서버 {server_ip}에 연결됨")

def run_gui():
    global entry, entry_ip
    root = tk.Tk()
    root.title("클라이언트")

    frame = tk.Frame(root)
    frame.pack(pady=10)

    label_ip = tk.Label(frame, text="서버 IP:")
    label_ip.pack(side=tk.LEFT)

    entry_ip = tk.Entry(frame)
    entry_ip.pack(side=tk.LEFT)

    button_connect = tk.Button(frame, text="연결", command=connect_to_server)
    button_connect.pack(side=tk.LEFT)

    label = tk.Label(root, text="메시지:")
    label.pack()

    entry = tk.Entry(root, width=50)
    entry.pack(pady=10)

    button_send = tk.Button(root, text="전송", command=send_message)
    button_send.pack()

    root.mainloop()

if __name__ == "__main__":
    run_gui()