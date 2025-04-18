import numpy as np
from keras_facenet import FaceNet
import cv2
from scipy.spatial.distance import cosine

embedder = FaceNet() 

def get_embedding(img_path):
    img = cv2.imread(img_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (160, 160))
    img = np.expand_dims(img, axis=0)
    
    embedding = embedder.embeddings(img)
    return embedding

face1 = get_embedding("/Users/bagseonghyeon/Documents/지켜락/facedetection/data/지젤.jpeg")
face2 = get_embedding("/Users/bagseonghyeon/Documents/지켜락/facedetection/data/카리나.jpeg")
face1 = face1.flatten() # (1, 512) -> (512,)
face2 = face2.flatten()
similarity = 1 - cosine(face1, face2)
threshold = 0.5  
if similarity >= threshold:
    result = "같은 사람"
else:
    result = "다른 사람"
print(face1.shape)  
print(face2.shape)
print(f"유사도: {similarity:.4f}")
print(result)