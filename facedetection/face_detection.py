import cv2
from mtcnn import MTCNN

detector = MTCNN()

img_path = "/Users/bagseonghyeon/Desktop/MTCNN/nct.jpeg" 
img = cv2.imread(img_path)
img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  

results = detector.detect_faces(img_rgb)

for result in results:
    x1, y1, width, height = result['box']
    x2, y2 = x1 + width, y1 + height
    
    cv2.rectangle(img_rgb, (x1, y1), (x2, y2), (0, 255, 0), 2)

    for key, value in result['keypoints'].items():
        cv2.circle(img_rgb, value, 2, (0, 0, 255), 2)

img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
cv2.imshow('얼굴 추출', img_bgr)

cv2.waitKey(0)
cv2.destroyAllWindows()