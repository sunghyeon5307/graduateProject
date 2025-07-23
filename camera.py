import cv2
from PIL import Image, ImageTk

cap = None
running = False

def start_camera():
    global cap, running
    if not running:
        cap = cv2.VideoCapture(0) 
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        running = True        

def stop_camera(video_label=None):
    global cap, running
    running = False
    if cap:
        cap.release()
        cap = None
    if video_label:
        video_label.configure(image="")

def show_camera_loop(frame_widget, root):
    global cap, running
    if running and cap and cap.isOpened():
        ret, frame = cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (800, 480))


            img = Image.fromarray(frame)
            imgtk = ImageTk.PhotoImage(image=img)
            frame_widget.imgtk = imgtk
            frame_widget.configure(image=imgtk)
    if running:
        root.after(30, lambda: show_camera_loop(frame_widget, root))
