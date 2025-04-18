import cv2
from mtcnn import MTCNN
import os

def run_detection(video_path):
    detector = MTCNN()
    frame_skip = 3  
    frame_count = 0
    previous_results = []

    cap = cv2.VideoCapture(video_path)

    os.makedirs("faces", exist_ok=True)  # 얼굴 저장 폴더

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1
        frame = cv2.resize(frame, (640, 360))
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        if frame_count % frame_skip == 0:
            results = detector.detect_faces(rgb_frame)
            previous_results = results
        else:
            results = previous_results

        for i, result in enumerate(results):
            x1, y1, w, h = result['box']
            x2, y2 = x1 + w, y1 + h

            # 얼굴 crop
            face = frame[y1:y2, x1:x2]

            # 유효한 이미지인지 확인
            if face.size > 0:
                save_path = f"faces/frame{frame_count}_face{i}.jpg"
                cv2.imwrite(save_path, face)

    cap.release()
