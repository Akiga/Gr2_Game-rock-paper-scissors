import socket
import threading

# Địa chỉ IP và cổng kết nối của server
HOST = '127.0.0.1'
PORT = 12345

# Tạo các biến toàn cục để quản lý phòng chơi và lựa chọn của người chơi
rooms = {}   # room_name -> [conn1, conn2]
choices = {} # room_name -> {conn: choice}
lock = threading.Lock()

# Hàm để xác định kết quả của trò chơi
def determine_winner(choice1, choice2):
    rules = {
        "rock": "scissors", # Búa thắng Kéo
        "scissors": "paper", # Kéo thắng Bao
        "paper": "rock"      # Bao thắng Búa
    }
    if choice1 == choice2:
        return "draw"
    elif rules[choice1] == choice2:
        return "win"
    else:
        return "lose"
    # Hàm để xử lý logic của một phòng chơi
def handle_room(room_name):
    while True:
        with lock:
            if room_name not in rooms or len(rooms[room_name]) < 2: # Kiểm tra xem phòng có đủ người chơi không
                continue

            room_players = rooms[room_name]
            room_choices = choices.get(room_name, {})

            if len(room_choices) == 2: #nếu đủ hai người chơi đã chọn
                p1, p2 = room_players
                c1 = room_choices.get(p1) # Lấy lựa chọn của người chơi 1
                c2 = room_choices.get(p2) # Lấy lựa chọn của người chơi 2

                r1 = determine_winner(c1, c2)
                r2 = determine_winner(c2, c1)

                try:  # Gửi kết quả cho cả hai người chơi
                    # Gửi kết quả cho người chơi 1
                    p1.send(f"Your choice: {c1}, Opponent: {c2}, Result: {r1}".encode())
                    #  Gửi kết quả cho người chơi 2
                    p2.send(f"Your choice: {c2}, Opponent: {c1}, Result: {r2}".encode())
                except:
                    pass

                choices[room_name] = {} # Xóa lựa chọn sau khi thông báo kết quả

# Hàm để xử lý kết nối của người chơi                
def handle_client(conn, addr):
    room_name = None
    print(f"[+] {addr} connected.")
    
# Hàm để xử lý kết nối của người chơi
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[STARTED] Server listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()               