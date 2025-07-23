import tkinter as tk
import sqlite3
from tkinter import messagebox
import json
import paho.mqtt.client as mqtt  


def get_password():
    conn = sqlite3.connect("mydata.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM password")
    cursor.execute("INSERT INTO password (pass) VALUES (?)", (new_pw,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else ""


MQTT_BROKER = "broker.hivemq.com"  
MQTT_PORT = 1883
MQTT_TOPIC = "num/door/open"  

client = mqtt.Client()

client.connect(MQTT_BROKER, MQTT_PORT, 60)


root = tk.Tk()
root.title("numpad")
root.geometry("320x240")
root.configure(bg='black')

button_frame = tk.Frame(root)
button_frame.pack(expand=True)

password_input = ""
password = get_password()

password_label = tk.Label(root, text="", font=("Helvetica", 16), bg='black', fg='white')
password_label.pack(pady=10)

button = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9'],
    ['Clear', '0', 'Enter']
]

def button_click(label):
    global password_input
    global password
    password = get_password()

    if label == 'Clear':
        password_input = ''
    elif label == 'Enter':
        if password_input == password:
            messagebox.showinfo("success", "open")
            print("MQTT Send Try")
            client.publish(MQTT_TOPIC,"1")
            result = client.publish
            (MQTT_TOPIC, "1")
            print("MQTT ??:", result.rc)
            print("MQTT Send OK")
        else:
            messagebox.showerror("fail", "password error")
        password_input = ''
    else:
        password_input += label

for r, row in enumerate(button):
    for c, label in enumerate(row):
        btn = tk.Button(button_frame, text=label, width=8, height=2, font=("Helvetica", 14))
        btn.config(command=lambda l=label: button_click(l))
        btn.grid(row=r, column=c, padx=2, pady=2)

root.mainloop()
