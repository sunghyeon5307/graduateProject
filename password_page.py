import tkinter as tk
import customtkinter as ctk
import sqlite3
from tkinter import messagebox
import requests

def get_password():
    conn = sqlite3.connect("passwordDB.db")
    cursor = conn.cursor()
    cursor.execute("SELECT pass FROM password ORDER BY ROWID DESC LIMIT 1")
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""



password = get_password()

class Page3(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller 
        ctk.CTkButton(
            self, text="⬅",
            width=100, height=50, corner_radius=14, 
            fg_color="lightgray", text_color="black", hover_color="red",    
            font=("Helvetica", 20, "bold"),
            command=lambda: controller.show_frame("Page1")
        ).grid(row=0, column=0,padx=30,pady=30)

        tk.Label(self, text="기존 비밀번호 입력:", fg="black", bg="white", font=("Helvetica", 30, "bold")).grid(row=1,column=1,padx=(300,5), pady=(250,40))
        self.origin_password = tk.Entry(self, fg="black", bg="lightgray", relief="flat", highlightthickness=0, bd=0, font=("Helvetica", 20),width=20)
        self.origin_password.grid(row=1,column=2,ipady=8,pady=(250,40))

        tk.Label(self, text="새 비밀번호 입력:", fg="black", bg="white", font=("Helvetica", 30, "bold")).grid(row=2,column=1,padx=(300,5))
        self.new_password = tk.Entry(self, fg="black", bg="lightgray", relief="flat", highlightthickness=0, bd=0, font=("Helvetica", 20),width=20)
        self.new_password.grid(row=2,column=2,ipady=8)
        self.new_password.config(state="disabled")

        # 기존 비번 확인 버튼
        ctk.CTkButton(
            self, text="확인", width=50,height=45,corner_radius=15,
            command=self.check,
            fg_color="lightgray", text_color="black", hover_color="red",
            font=("Helvetica", 15, "bold")
        ).grid(row=1, column=3, padx=10,pady=(250,40))

        # 새 비번 입력 후 확인 버튼
        ctk.CTkButton(
            self, text="확인", width=50,height=45,corner_radius=15,
            command=self.save_password,
            fg_color="lightgray", text_color="black", hover_color="red",
            font=("Helvetica", 15, "bold")
        ).grid(row=2, column=3, padx=10)
    
    def check(self):
        if self.origin_password.get() == password:
            self.new_password.config(state="normal")
        else:
            messagebox.showerror("오류", "기존 비밀번호가 틀렸습니다")

    def save_password(self):
        new_pw = self.new_password.get().strip()

        conn = sqlite3.connect("passwordDB.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM password")
        cursor.execute("INSERT INTO password (pass) VALUES (?)", (new_pw,))
        conn.commit()
        conn.close()

        self.send_password_to_pi(new_pw)

        tk.messagebox.showinfo("성공", "비밀번호가 변경되었습니다.")
        self.new_password.delete(0, tk.END)
        self.new_password.config(state="disabled")
        self.origin_password.delete(0, tk.END)

    def send_password_to_pi(self, new_pw):
        url = "http://10.150.2.201:5000/update_password" 
        response = requests.post(url, json={"password": new_pw})
        print(response.text)

