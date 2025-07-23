import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import threading
import customtkinter as ctk
from camera import start_camera, stop_camera, show_camera_loop
from intruder_page import Page2
from password_page import Page3 

cap = None
running = False

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("얼굴 등록")
        self.geometry("2560x1600")
        self.configure(bg="white")

        container = tk.Frame(self, bg="white")
        container.pack(fill="both", expand=True)

        self.frames = {}
        for F in (Page1, Page2, Page3):
            page_name = F.__name__
            frame = F(container, self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Page1")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class Page1(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller


        tk.Label(self, text="이름 입력:", fg="black", bg="white", font=("Helvetica", 30, "bold")).grid(row=0,column=0,padx=(50,0),pady=(290,20))
        self.name_entry = tk.Entry(self, fg="black", bg="lightgray", relief="flat", highlightthickness=0, bd=0, font=("Helvetica", 20),width=20)
        self.name_entry.grid(row=0,column=1,ipady=8,pady=(290,20))


        # 촬영시작 버튼
        ctk.CTkButton(
            self, text="촬영 시작", width=300, height=50, corner_radius=18,
            command=self.start_capture,
            fg_color="lightgray", text_color="black", hover_color="red",
            font=("Helvetica", 18, "bold")
        ).grid(row=1, column=1,padx=10,pady=(50,10))

        # 두번째 페이지 버튼
        ctk.CTkButton(
            self, text="외부인 확인", width=300, height=50, corner_radius=18,
            command=lambda: self.controller.show_frame("Page2"),
            fg_color="lightgray", text_color="black", hover_color="red",
            font=("Helvetica", 18, "bold")
        ).grid(row=2,column=1, padx=10, pady=10)

        # 세번째 페이지 버튼
        ctk.CTkButton(
            self, text="비밀번호 등록", width=300, height=50, corner_radius=18,
            command=lambda: self.controller.show_frame("Page3"),
            fg_color="lightgray", text_color="black", hover_color="red",
            font=("Helvetica", 18, "bold")
        ).grid(row=3, column=1, padx=10, pady=10)


        self.video_label = tk.Label(self, bg="lightgray")
        self.video_label.grid(row=0, column=2, rowspan=10, padx=(60,10), pady=200)
        self.video_label.config(width=800, height=480)


        start_camera()
        show_camera_loop(self.video_label, self)
        
    def start_capture(self):
        from face_detection import vector_video
        name = self.name_entry.get().strip()

        if not name:
            messagebox.showerror("입력 오류", "이름을 입력하세요")
            return

        def run():
            success = vector_video(name)
            msg = "벡터 저장 완료" if success else "촬영 실패 또는 중단됨"
            messagebox.showinfo("처리 결과", msg)

        threading.Thread(target=run).start()


    
if __name__ == "__main__":
    App().mainloop()