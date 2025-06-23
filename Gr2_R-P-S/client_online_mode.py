import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from playsound import playsound
import pygame
import os
from tkinter import simpledialog
import client  # Import client.py để gọi lại menu chính


# Địa chỉ IP và cổng kết nối của server
HOST = '127.0.0.1'
PORT = 12345

# Lớp RPSServerClient để quản lý giao diện và logic của trò chơi trực tuyến
class RPSServerClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors - Online")
        self.root.geometry("700x600")
        self.root.configure(bg="#e6f2ff")

        self.score = 0
        self.sound_on = True
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.room_name = self.ask_room()
        self.setup_ui()
        self.init_background_music()

        try:
            self.client.connect((HOST, PORT))
            self.client.send(f"JOIN:{self.room_name}".encode())
            threading.Thread(target=self.receive_result, daemon=True).start()
        except:
            messagebox.showerror("Error", "Không thể kết nối tới server")
            self.root.destroy()
    # Hàm để hỏi tên phòng từ người dùng
    def ask_room(self):
        return tk.simpledialog.askstring("Room Name", "Nhập tên phòng:") or "default"
    # Hàm để thiết lập giao diện người dùng
    def setup_ui(self):
        self.score_label = tk.Label(self.root, text=f"Your Score: {self.score}", font=("Arial", 14, "bold"), fg="blue", bg="#e6f2ff")
        self.score_label.pack(pady=5)

        self.buttons_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.buttons_frame.pack(pady=10)

        self.rock_img = ImageTk.PhotoImage(Image.open("rock.png").resize((80, 80)))
        self.paper_img = ImageTk.PhotoImage(Image.open("paper.png").resize((80, 80)))
        self.scissors_img = ImageTk.PhotoImage(Image.open("scissors.png").resize((80, 80)))

        tk.Button(self.buttons_frame, image=self.rock_img, command=lambda: self.send_choice("rock"), bg="#e6f2ff", bd=0).grid(row=0, column=0, padx=20)
        tk.Button(self.buttons_frame, image=self.paper_img, command=lambda: self.send_choice("paper"), bg="#e6f2ff", bd=0).grid(row=0, column=1, padx=20)
        tk.Button(self.buttons_frame, image=self.scissors_img, command=lambda: self.send_choice("scissors"), bg="#e6f2ff", bd=0).grid(row=0, column=2, padx=20)

        self.result_text = tk.Text(self.root, height=12, width=80, bg="white", font=("Consolas", 11))
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

        chat_frame = tk.Frame(self.root, bg="#e6f2ff")
        chat_frame.pack(pady=5)

        self.chat_entry = tk.Entry(chat_frame, width=50, font=("Arial", 11))
        self.chat_entry.pack(side=tk.LEFT, padx=5)

        self.send_button = tk.Button(chat_frame, text="Send", command=self.send_chat, bg="#2196F3", fg="white")
        self.send_button.pack(side=tk.LEFT)

        self.toggle_sound_button = tk.Button(self.root, text="🔊 Sound: ON", command=self.toggle_sound, bg="#cccccc")
        self.toggle_sound_button.pack(pady=5)

        # Thêm nút Quay lại
        tk.Button(self.root, text="Quay lại", font=("Arial", 14), width=20, command=self.back_to_menu, bg="#ff6666", fg="white").pack(pady=10)
    # Hàm để khởi tạo nhạc nền
    def init_background_music(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("background.wav")
            pygame.mixer.music.set_volume(0.3 if self.sound_on else 0)
            pygame.mixer.music.play(-1)
        except:
            pass
# Hàm để phát âm thanh khi có sự kiện
    def play_sound(self, filename):
        if self.sound_on and os.path.exists(filename):
            threading.Thread(target=lambda: playsound(filename), daemon=True).start()
    # Hàm để bật/tắt âm thanh
    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.toggle_sound_button.config(text="🔇 Sound: OFF" if not self.sound_on else "🔊 Sound: ON")
        try:
            pygame.mixer.music.set_volume(0.3 if self.sound_on else 0)
        except:
            pass
            # Hàm để gửi lựa chọn của người chơi tới server
    def send_choice(self, choice):
        self.play_sound("click.wav")
        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f"You chose: {choice}\n", "info")
        self.result_text.config(state=tk.DISABLED)
        try:
            self.client.send(f"GAME:{choice}".encode())
        except:
            messagebox.showerror("Error", "Không thể gửi lựa chọn tới server")
    # Hàm để gửi tin nhắn chat tới server
    def send_chat(self):
        message = self.chat_entry.get().strip()
        if message:
            try:
                self.client.send(f"CHAT:{message}".encode())
                self.result_text.config(state=tk.NORMAL)
                self.result_text.insert(tk.END, f"You: {message}\n", "chat")
                self.result_text.config(state=tk.DISABLED)
                self.chat_entry.delete(0, tk.END)
            except:
                messagebox.showerror("Error", "Không thể gửi tin nhắn")
    # Hàm để nhận kết quả từ server
    def receive_result(self):
        while True:
            try:
                result = self.client.recv(1024).decode()
                self.result_text.config(state=tk.NORMAL)

                if result.startswith("[CHAT]"):
                    self.result_text.insert(tk.END, f"{result}\n", "chat")
                elif result.startswith("[INFO]"):
                    self.result_text.insert(tk.END, f"{result}\n", "info")
                elif "result: win" in result.lower():
                    self.play_sound("win.wav")
                    self.score += 1
                    self.result_text.insert(tk.END, f"{result}\n\n", "win")
                elif "result: lose" in result.lower():
                    self.play_sound("lose.wav")
                    self.result_text.insert(tk.END, f"{result}\n\n", "lose")
                elif "result: draw" in result.lower():
                    self.play_sound("draw.wav")
                    self.result_text.insert(tk.END, f"{result}\n\n", "draw")
                self.score_label.config(text=f"Your Score: {self.score}")
                self.result_text.config(state=tk.DISABLED)
            except:
                break
     # Hàm để quay lại menu chính           
    def back_to_menu(self):
        try:
            self.client.send("QUIT".encode())  # Gửi tín hiệu thoát tới server
            self.client.close()  # Đóng kết nối
        except:
            pass
        pygame.mixer.music.stop()  # Dừng nhạc nền
        self.root.destroy()  # Đóng cửa sổ hiện tại
        new_root = tk.Tk()  # Tạo cửa sổ mới
        app = client.RPSClient(new_root)  # Khởi tạo menu chính
        new_root.mainloop()
# # Hàm để khởi động lại ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = RPSServerClient(root)
    app.result_text.tag_config("win", foreground="green", font=("Consolas", 11, "bold"))
    app.result_text.tag_config("lose", foreground="red", font=("Consolas", 11, "bold"))
    app.result_text.tag_config("draw", foreground="orange", font=("Consolas", 11, "italic"))
    app.result_text.tag_config("chat", foreground="purple")
    app.result_text.tag_config("info", foreground="blue")
    root.mainloop()