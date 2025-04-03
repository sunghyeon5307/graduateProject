import cv2
import numpy as np
import tensorflow as tf
from tensorflow import keras
from mtcnn import MTCNN

detector = MTCNN()
model_path = '/path/to/facenet_model/facenet_keras.h5'
model = keras.models.load_model(model_path)

img_path = "/path/to/your/image.jpg"
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

results = detector.detect_faces(img_rgb)

for result in results:
    x1, y1, width, height = result['box']
    x2, y2 = x1 + width, y1 + height
    face = img_rgb[y1:y2, x1:x2]
    face_resized = cv2.resize(face, (160, 160))
    face_array = np.array(face_resized, dtype=np.float32)
    face_array = (face_array - 127.5) / 128.0
    face_array = np.expand_dims(face_array, axis=0)
    face_encoding = model.predict(face_array)
    print("완료:", face_encoding[0])
    cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)

img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
cv2.imshow('얼굴 추출 및 벡터화', img_bgr)
cv2.waitKey(0)
cv2.destroyAllWindows()