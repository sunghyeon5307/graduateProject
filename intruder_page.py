import tkinter as tk
import customtkinter as ctk

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
        ).grid(row=0, column=0,padx=30,pady=30)