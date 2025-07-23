import tkinter as tk
import customtkinter as ctk
from PIL import Image, ImageTk
import os

folder = "unknown_faces"

class Page2(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller  

        ctk.CTkButton(
            self, text="⬅",
            width=100, height=50, corner_radius=14, 
            fg_color="lightgray", text_color="black", hover_color="red",    
            font=("Helvetica", 30, "bold"),
            command=lambda: controller.show_frame("Page1")
        ).grid(row=0, column=0, padx=30, pady=30, sticky="w")

        ctk.CTkButton(
            self, text="🔄 새로고침",
            width=150, height=50, corner_radius=14,
            fg_color="lightgray", text_color="black", hover_color="red",
            font=("Helvetica", 20, "bold"),
            command=self.refresh_images
        ).grid(row=0, column=1, padx=20, pady=30, sticky="e")

        self.image_widget = []
        self.refresh_images()

    def refresh_images(self):
        for widget in self.image_widget:
            widget.destroy()
        self.image_widget.clear()

        files = sorted([
            f for f in os.listdir(folder)
            if f.startswith("unknown_") and f.endswith(".jpg")
        ])

        row_idx = 1
        for file in files:
            try:
                time = file.split("_")[1].split(".")[0] 
                path = os.path.join(folder, file)

                img = Image.open(path)
                img = img.resize((300, 200))
                tk_img = ImageTk.PhotoImage(img)

                tk.Label(self, text=f"{time}", fg="black", bg="white", font=("Helvetica", 18,"bold")).grid(row=row_idx, column=0, pady=10, padx=300, sticky="w")
    

                image_label = tk.Label(self, image=tk_img, bg="white")
                image_label.image = tk_img  
                image_label.grid(row=row_idx, column=1, pady=10)
                self.image_widgets.append(image_label)

                row_idx += 1

            except Exception as e:
                print(f"❌ 이미지 로드 실패: {file}, 오류: {e}")
