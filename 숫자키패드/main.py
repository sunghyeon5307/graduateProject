import tkinter as tk
import serial
import time
from tkinter import messagebox


ser = serial.Serial('/dev/tty.usbmodem14401', 115200)  
time.sleep(2)

root = tk.Tk()
root.title("도어락 키패드")
root.geometry("320x240")
root.configure(bg='black')

button_frame = tk.Frame(root)
button_frame.pack(expand=True)

password_input = ""
password = "2025"

password_label = tk.Label(root, text="", font=("Helvetica", 16), bg='black', fg='white')
password_label.pack(pady=10)

button = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['Clear', '0', 'Enter']
]

def button_click(label):
    global  password_input
    
    if label == 'Clear':
        password_input = ''
    elif label == 'Enter':
        if password_input == password:
            messagebox.showinfo("성공", "문 오픈")
            ser.write(b"1\n")
            ser.flush()
            print("전송완료")
        else:
            messagebox.showerror("입력 오류", "비번 틀림")
        password_input = ''
    else:
        password_input += label
            
for r, row in enumerate(button):
    for c, label in enumerate(row):
        btn = tk.Button(button_frame, text=label, width=8, height=2, font=("Helvetica", 14))
        btn.config(command=lambda l=label: button_click(l))
        btn.grid(row=r, column=c, padx=2, pady=2)

root.mainloop()
