import socket
import threading
import tkinter as tk

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
            display_message(message)
        except:
            break
    client_socket.close()

def display_message(message):
    global text_widget
    text_widget.insert(tk.END, message + '\n')

def run_gui():
    global text_widget
    root = tk.Tk()
    root.title("서버")
    
    text_widget = tk.Text(root)
    text_widget.pack()

    threading.Thread(target=start_server, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    run_gui()
