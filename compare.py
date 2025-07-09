import cv2
import numpy as np
import sqlite3
from insightface.app import FaceAnalysis

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

def load_registered_vectors():
    conn = sqlite3.connect("facevectors.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, vector FROM facevectors")
    data = cursor.fetchall()
    conn.close()

    vectors = []
    names = []
    for name, vec_blob in data:
        vec = np.frombuffer(vec_blob, dtype=np.float32)
        vec = vec / np.linalg.norm(vec)  
        vectors.append(vec)
        names.append(name)
    return names, vectors

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def authenticate(threshold=0.65):
    names, registered_vectors = load_registered_vectors()
    if not names:
        return

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = app.get(rgb)

        if faces:
            face = faces[0]
            input_vec = face.embedding / np.linalg.norm(face.embedding)

            sims = [cosine_similarity(input_vec, vec) for vec in registered_vectors]
            best_index = np.argmax(sims)
            best_score = sims[best_index]

            if best_score >= threshold:
                name = names[best_index]
                print(f"✅ {name} 문 오픈 (유사도: {best_score:.4f})")
                cv2.putText(frame, f"{name} ({best_score:.2f})", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
            else:
                print(f"일치 없음 (최고 유사도: {best_score:.4f})")
                cv2.putText(frame, "Unknown", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)

        cv2.imshow("Face Authentication", frame)
        if cv2.waitKey(1) == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    authenticate()
