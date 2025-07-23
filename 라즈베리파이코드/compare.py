import cv2
import numpy as np
import sqlite3
from insightface.app import FaceAnalysis
import requests
import serial
import time


ser = serial.Serial('/dev/tty.usbserial-1440', 115200)
time.sleep(2)

app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

def read_vector():
    conn = sqlite3.connect("mydb.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, vector FROM facevector")
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

def authenticate(threshold=0.7):
    names, vectors = read_vector()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return
    
    now_time = None
    send_face = False

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        faces = app.get(rgb)

        if faces:
            face = faces[0]
            input_vec = face.embedding / np.linalg.norm(face.embedding)

            sims = [cosine_similarity(input_vec, vec) for vec in vectors]
            best_index = np.argmax(sims)
            best_score = sims[best_index]

            if best_score >= threshold:
                name = names[best_index]
                print(f"{name} 문 오픈 (유사도: {best_score:.4f})")
                ser.write(b"1\n")
                ser.flush()
                cv2.putText(frame, f"{name} ({best_score:.2f})", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
                
                now_time = None
                send_face = False
            else:
                print(f"얼굴 없음(최고 유사도: {best_score:.4f})")
                cv2.putText(frame, "Unknown", (30, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 0, 255), 3)
            
                if now_time is None:
                    now_time = time.time()
                elif time.time() - now_time >= 10 and not send_face:
                    send_time = int(time.time())
                    filename = f"{send_time}.jpg"
                    cv2.imwrite(filename, frame)

                    try:
                        with open(filename, "rb") as f:
                            res = requests.post("http://your-server/upload", files={"image": f})
                        print("미등록 얼굴 전송 완료:", res.status_code)
                    except Exception as e:
                        print("이미지 전송 오류:", e)
                    
                    send_face = True
        else:
            now_time = None
            send_face = False

        cv2.imshow("Face Authentication", frame)
        if cv2.waitKey(1) == 27: 
            break

    cap.release()
    cv2.destroyAllWindows()
if __name__ == "__main__":
    authenticate()

    

