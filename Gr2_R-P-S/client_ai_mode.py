import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from playsound import playsound
import pygame
import os
import random
import client  # Import client.py để gọi lại menu chính

class RPSEngineAI:
    def __init__(self, root):
        self.root = root
        self.root.title("Chơi với Máy - Rock-Paper-Scissors")
        self.root.geometry("700x600")
        self.root.configure(bg="#e6f2ff")

        self.score = 0
        self.sound_on = True

        self.setup_ui()
        self.init_background_music()

    def setup_ui(self):
        tk.Label(self.root, text="Chế độ: Chơi với Máy", font=("Arial", 14, "bold"), bg="#e6f2ff").pack(pady=10)

        self.score_label = tk.Label(self.root, text=f"Điểm của bạn: {self.score}", font=("Arial", 14), fg="blue", bg="#e6f2ff")
        self.score_label.pack(pady=5)

        self.buttons_frame = tk.Frame(self.root, bg="#e6f2ff")
        self.buttons_frame.pack(pady=10)

        self.rock_img = ImageTk.PhotoImage(Image.open("img/rock.png").resize((80, 80)))
        self.paper_img = ImageTk.PhotoImage(Image.open("img/paper.png").resize((80, 80)))
        self.scissors_img = ImageTk.PhotoImage(Image.open("img/scissors.png").resize((80, 80)))

        tk.Button(self.buttons_frame, image=self.rock_img, command=lambda: self.play("rock"), bg="#e6f2ff", bd=0).grid(row=0, column=0, padx=20)
        tk.Button(self.buttons_frame, image=self.paper_img, command=lambda: self.play("paper"), bg="#e6f2ff", bd=0).grid(row=0, column=1, padx=20)
        tk.Button(self.buttons_frame, image=self.scissors_img, command=lambda: self.play("scissors"), bg="#e6f2ff", bd=0).grid(row=0, column=2, padx=20)

        self.result_text = tk.Text(self.root, height=12, width=80, bg="white", font=("Consolas", 11))
        self.result_text.pack(pady=10)
        self.result_text.config(state=tk.DISABLED)

        self.toggle_sound_button = tk.Button(self.root, text="🔊 Sound: ON", command=self.toggle_sound, bg="#cccccc")
        self.toggle_sound_button.pack(pady=5)

        # Thêm nút Quay lại
        tk.Button(self.root, text="Quay lại", font=("Arial", 14), width=20, command=self.back_to_menu, bg="#ff6666", fg="white").pack(pady=10)

    def init_background_music(self):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load("music/background.wav")
            pygame.mixer.music.set_volume(0.3 if self.sound_on else 0)
            pygame.mixer.music.play(-1)
        except:
            pass

    def toggle_sound(self):
        self.sound_on = not self.sound_on
        self.toggle_sound_button.config(text="🔇 Sound: OFF" if not self.sound_on else "🔊 Sound: ON")
        try:
            pygame.mixer.music.set_volume(0.3 if self.sound_on else 0)
        except:
            pass

    def play_sound(self, filename):
        if self.sound_on and os.path.exists(filename):
            from threading import Thread
            Thread(target=lambda: playsound(filename), daemon=True).start()

    def play(self, player_choice):
        self.play_sound("click.wav")
        ai_choice = random.choice(["rock", "paper", "scissors"])
        result = self.determine_winner(player_choice, ai_choice)

        self.result_text.config(state=tk.NORMAL)
        self.result_text.insert(tk.END, f"Bạn chọn: {player_choice} | Máy chọn: {ai_choice} => ", "info")

        if result == "win":
            self.play_sound("win.wav")
            self.result_text.insert(tk.END, "Thắng\n", "win")
            self.score += 1
        elif result == "lose":
            self.play_sound("lose.wav")
            self.result_text.insert(tk.END, "Thua\n", "lose")
        else:
            self.play_sound("draw.wav")
            self.result_text.insert(tk.END, "Hòa\n", "draw")

        self.score_label.config(text=f"Điểm của bạn: {self.score}")
        self.result_text.config(state=tk.DISABLED)

    def determine_winner(self, player, ai):
        if player == ai:
            return "draw"
        rules = {"rock": "scissors", "scissors": "paper", "paper": "rock"}
        return "win" if rules[player] == ai else "lose"

    def back_to_menu(self):
        pygame.mixer.music.stop()  # Dừng nhạc nền
        self.root.destroy()  # Đóng cửa sổ hiện tại
        new_root = tk.Tk()  # Tạo cửa sổ mới
        app = client.RPSClient(new_root)  # Khởi tạo menu chính
        new_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = RPSEngineAI(root)

    app.result_text.tag_config("win", foreground="green", font=("Consolas", 11, "bold"))
    app.result_text.tag_config("lose", foreground="red", font=("Consolas", 11, "bold"))
    app.result_text.tag_config("draw", foreground="orange", font=("Consolas", 11, "italic"))
    app.result_text.tag_config("info", foreground="blue")

    root.mainloop()