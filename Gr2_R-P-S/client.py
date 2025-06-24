import socket
import threading
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from playsound import playsound
import pygame
import os
import random


# Địa chỉ IP và cổng kết nối của server
HOST = '127.0.0.1'
PORT = 12345

#tạo menu chính
# Lớp RPSClient để quản lý giao diện và logic của trò chơi
class RPSClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock-Paper-Scissors Main Menu")
        self.root.geometry("500x400")
        self.root.configure(bg="#dbefff")

        self.main_menu()
#    # Hàm để hiển thị menu chính
    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="Rock-Paper-Scissors", font=("Arial", 20, "bold"), bg="#dbefff", fg="#333").pack(pady=30)
#        # Tạo các nút để chọn chế độ chơi
        tk.Button(self.root, text="Chơi với máy", font=("Arial", 14), width=20, command=self.start_ai_mode).pack(pady=10)
        tk.Button(self.root, text="Chơi với người", font=("Arial", 14), width=20, command=self.start_online_mode).pack(pady=10)
        tk.Button(self.root, text="Hướng dẫn", font=("Arial", 14), width=20, command=self.show_instructions).pack(pady=10)
        tk.Button(self.root, text="Thoát", font=("Arial", 14), width=20, command=self.root.quit).pack(pady=10)
# Hàm để bắt đầu chế độ chơi với máy
    def start_ai_mode(self):
        self.root.destroy()
        import subprocess
        subprocess.Popen(["python", "Gr2_R-P-S/client_ai_mode.py"])  # Đổi tên file của bạn nếu khác
# Hàm để bắt đầu chế độ chơi với người
    def start_online_mode(self):
        self.root.destroy()
        import subprocess
        subprocess.Popen(["python", "Gr2_R-P-S/client_online_mode.py"])  # Bạn cần tách logic chơi online nếu muốn tách biệt
# Hàm để hiển thị hướng dẫn trò chơi
    def show_instructions(self):
        messagebox.showinfo("Hướng dẫn", "\u2022 Chọn 'Chơi với máy' để đấu với AI\n\u2022 Chọn 'Chơi với người' để đấu trực tuyến\n\u2022 Nhấn biểu tượng để chọn: Kéo, Búa, Bao\n\u2022 Kết quả và điểm sẽ hiển thị bên dưới")
# Hàm để khởi động lại  ứng dụng
if __name__ == "__main__":
    root = tk.Tk()
    app = RPSClient(root)
    root.mainloop()
