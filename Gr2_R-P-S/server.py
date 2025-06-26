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
        return "Hòa"
    elif rules[choice1] == choice2:
        return "Thắng "
    else:
        return "Thua"
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
                    p1.send(f"Bạn chọn: {c1}, Đối thủ chọn: {c2}, Kết quả: {r1}".encode())
                    #  Gửi kết quả cho người chơi 2
                    p2.send(f"Bạn chọn: {c2}, Đối thủ chọn: {c1}, Kết quả: {r2}".encode())
                except:
                    pass

                choices[room_name] = {} # Xóa lựa chọn sau khi thông báo kết quả

# Hàm để xử lý kết nối của người chơi                
def handle_client(conn, addr):
    room_name = None
    print(f"[+] {addr} Đã kết nối.")
    try:
        while True:
            # Nhận dữ liệu từ client
            data = conn.recv(1024).decode().strip()
            if not data:
                break  # Nếu không có dữ liệu thì thoát khỏi vòng lặp
    
            # Yêu cầu danh sách phòng hiện có
            if data == "LIST":
                with lock:
                    # Lấy tên tất cả các phòng, nếu không có thì thông báo "(no rooms)"
                    room_list = "\n".join(rooms.keys()) if rooms else "(Không có phòng nào)"
                # Gửi danh sách phòng về cho client
                conn.send(f"[ROOMS]\n{room_list}".encode())
    
            # Yêu cầu tham gia một phòng
            elif data.startswith("JOIN:"):
                room_name = data[5:]  # Tách tên phòng từ dữ liệu
                with lock:
                    # Tạo phòng mới nếu chưa tồn tại
                    if room_name not in rooms:
                        rooms[room_name] = []
                        choices[room_name] = {}
    
                    # Nếu phòng đã đủ 2 người thì từ chối
                    if len(rooms[room_name]) >= 2:
                        conn.send("[LỗI] Phòng đầy.".encode())
                        continue
    
                    # Thêm client vào phòng
                    rooms[room_name].append(conn)
                    conn.send(f"[THÔNG BÁO] Đã tham gia phòng '{room_name}'. Đang chờ đối thủ...".encode())
    
                    # Nếu đủ 2 người, thông báo cho cả 2 người và tạo luồng xử lý game
                    if len(rooms[room_name]) == 2:
                        for c in rooms[room_name]:
                            c.send(f"[THÔNG BÁO] Đối thủ đã tham gia. Bạn có thể bắt đầu chơi.".encode())
                        threading.Thread(target=handle_room, args=(room_name,), daemon=True).start()
    
            # Client rời khỏi phòng
            elif data == "QUIT" and room_name:
                with lock:
                    if conn in rooms.get(room_name, []):
                        rooms[room_name].remove(conn)
                        # Xóa lượt chọn nếu có
                        if conn in choices.get(room_name, {}):
                            del choices[room_name][conn]
                        # Thông báo cho người còn lại
                        for c in rooms.get(room_name, []):
                            c.send(f"[THÔNG BÁO] Đối thủ đã rời phòng.".encode())
                        # Nếu phòng không còn ai thì xóa phòng
                        if len(rooms.get(room_name, [])) == 0:
                            del rooms[room_name]
                            if room_name in choices:
                                del choices[room_name]
                break
    
            # Nhắn tin trong phòng
            elif data.startswith("CHAT:") and room_name:
                msg = data[5:]
                with lock:
                    for c in rooms.get(room_name, []):
                        if c != conn:
                            c.send(f"[CHAT] {addr}: {msg}".encode())
    
            # Nhận lựa chọn game (ví dụ oẳn tù tì)
            elif data.startswith("GAME:") and room_name:
                choice = data[5:].lower()
                with lock:
                    if room_name not in choices:
                        choices[room_name] = {}
                    choices[room_name][conn] = choice
    
    except:
        # Nếu có lỗi thì bỏ qua (khuyến nghị nên log lỗi)
        pass
    
    finally:
        with lock:
            if room_name:
                if conn in rooms.get(room_name, []):
                    rooms[room_name].remove(conn)
                    if conn in choices.get(room_name, {}):
                        del choices[room_name][conn]
                    for c in rooms.get(room_name, []):
                        c.send(f"[THÔNG BÁO] Đối thủ đã rời phòng thi.".encode())
                    if len(rooms.get(room_name, [])) == 0:
                        del rooms[room_name]
                        if room_name in choices:
                            del choices[room_name]
        # Đóng kết nối và thông báo ngắt kết nối
        conn.close()
        print(f"[-] {addr} Đã ngắt kết nối.")
    
# Hàm để xử lý kết nối của người chơi
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print(f"[BẮT ĐẦU] Máy chủ đang kết nối {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()               
