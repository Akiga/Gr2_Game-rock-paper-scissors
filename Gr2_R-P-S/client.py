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

# Lớp RPSClient để quản lý giao diện và logic của menu chính
class RPSClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Chính - Búa Bao Kéo")
        self.root.geometry("500x400")
        self.root.configure(bg="#dbefff")

        self.main_menu()

    # Hàm để hiển thị menu chính
    def main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()

        tk.Label(self.root, text="BÚA – KÉO – BAO", font=("Arial", 20, "bold"), bg="#dbefff", fg="#333").pack(pady=30)

        tk.Button(self.root, text="🤖 Chơi với Máy", font=("Arial", 14), width=20, command=self.start_ai_mode).pack(pady=10)
        tk.Button(self.root, text="👥 Chơi với Người", font=("Arial", 14), width=20, command=self.start_online_mode).pack(pady=10)
        tk.Button(self.root, text="📖 Hướng Dẫn", font=("Arial", 14), width=20, command=self.show_instructions).pack(pady=10)
        tk.Button(self.root, text="🚪 Thoát", font=("Arial", 14), width=20, command=self.root.quit).pack(pady=10)

    # Hàm để bắt đầu chế độ chơi với máy
    def start_ai_mode(self):
        self.root.destroy()
        import subprocess
        subprocess.Popen(["python", "Gr2_R-P-S/client_ai_mode.py"])

    # Hàm để bắt đầu chế độ chơi với người
    def start_online_mode(self):
        self.root.destroy()
        import subprocess
        subprocess.Popen(["python", "Gr2_R-P-S/client_online_mode.py"])

    # Hàm hiển thị hướng dẫn trò chơi
    def show_instructions(self):
        messagebox.showinfo(
            "Hướng dẫn chơi",
            "📌 Cách chơi:\n"
            "• Chọn 'Chơi với Máy' để đấu với máy tính (AI)\n"
            "• Chọn 'Chơi với Người' để đấu trực tuyến với người khác\n"
            "• Nhấn biểu tượng Búa, Bao hoặc Kéo để ra tay\n"
            "• Kết quả và điểm sẽ được hiển thị sau mỗi lượt chơi"
        )

# Khởi động menu chính
if __name__ == "__main__":
    root = tk.Tk()
    app = RPSClient(root)
    root.mainloop()
