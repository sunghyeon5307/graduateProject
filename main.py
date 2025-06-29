# import tkinter as tk
# from tkinter import messagebox
# import threading
# from face_detection import vector_video

# def start_capture():
#     name = name_entry.get().strip()
#     if not name:
#         messagebox.showerror("입력 오류", "이름을 입력하세요")
#         return

#     def run():
#         success = vector_video(name)
#         msg = "✅ 벡터 저장 완료" if success else "❌ 촬영 실패 또는 중단됨"
#         messagebox.showinfo("처리 결과", msg)

#     threading.Thread(target=run).start()

# # GUI 설정
# root = tk.Tk()
# root.title("얼굴 등록기")
# root.geometry("300x180")

# tk.Label(root, text="이름 입력:").pack(pady=10)
# name_entry = tk.Entry(root)
# name_entry.pack()

# tk.Button(root, text="촬영 시작", command=start_capture).pack(pady=20)

# root.mainloop()

import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading

cap = None
running = False

def show_camera():
    if not running:
        return

    ret, frame = cap.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame)
        imgtk = ImageTk.PhotoImage(image=img)
        camera_label.imgtk = imgtk
        camera_label.configure(image=imgtk)
    camera_label.after(10, show_camera)

def start_capture():
    global cap, running
    name = name_entry.get().strip()
    if not name:
        messagebox.showerror("입력 오류", "이름을 입력하세요")
        return

    if not running:
        cap = cv2.VideoCapture(0)
        running = True
        show_camera()

    def run():
        from face_detection import vector_video
        success = vector_video(name)
        msg = "✅ 벡터 저장 완료" if success else "❌ 촬영 실패 또는 중단됨"
        messagebox.showinfo("처리 결과", msg)
        stop_camera()

    threading.Thread(target=run).start()

def stop_camera():
    global running, cap
    running = False
    if cap:
        cap.release()
        camera_label.configure(image='')

# GUI 설정
root = tk.Tk()
root.title("얼굴 등록기")
root.geometry("400x500")

tk.Label(root, text="이름 입력:").pack(pady=10)
name_entry = tk.Entry(root)
name_entry.pack()

tk.Button(root, text="촬영 시작", command=start_capture).pack(pady=10)

# 캠 영상 표시용 라벨
camera_label = tk.Label(root)
camera_label.pack()

root.mainloop()

