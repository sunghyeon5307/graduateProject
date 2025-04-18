import cv2
from mtcnn import MTCNN

detector = MTCNN()
video_path = "/Users/bagseonghyeon/Documents/지켜락/facedetection/downloads/yt_video_30s.mp4"

frame_skip = 3  
frame_count = 0
previous_results = []

while True:
    cap = cv2.VideoCapture(video_path)

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

        for result in results:
            x1, y1, width, height = result['box']
            x2, y2 = x1 + width, y1 + height
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            for key, value in result['keypoints'].items():
                cv2.circle(frame, value, 2, (0, 0, 255), 2)

        cv2.imshow('얼굴 추출', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cap.release()