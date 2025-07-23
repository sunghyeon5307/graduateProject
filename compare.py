import cv2
import numpy as np
import sqlite3
from insightface.app import FaceAnalysis
import socket
import time
import os
from datetime import datetime
import shutil
import paho.mqtt.client as mqtt  


# udp_ip = "10.150.2.13"
# udp_port = 5002
# sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 

app_insight = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app_insight.prepare(ctx_id=0)

MQTT_BROKER = "broker.hivemq.com"  
MQTT_PORT = 1883
MQTT_TOPIC = "face/door/open"

IMAGE_PATH = "received_faces/face.jpg"
THRESHOLD = 0.65

def load_registered_vectors():
    conn = sqlite3.connect("facevectors.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name, vector FROM facevectors")
    data = cursor.fetchall()
    conn.close()

    names, vectors = [], []
    for name, vec_blob in data:
        vec = np.frombuffer(vec_blob, dtype=np.float32)
        vec = vec / np.linalg.norm(vec)
        names.append(name)
        vectors.append(vec)
    return names, vectors

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def verify_face(img_path, threshold=0.5):
    img = cv2.imread(img_path)
    if img is None:
        print("📂 이미지 없음 또는 로딩 실패")
        return None

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = app_insight.get(rgb)

    if not faces:
        print("❌ 얼굴이 감지되지 않음")
        return None

    input_vec = faces[0].embedding / np.linalg.norm(faces[0].embedding)
    names, vectors = load_registered_vectors()
    sims = [cosine_similarity(input_vec, v) for v in vectors]

    best_index = int(np.argmax(sims))
    best_score = sims[best_index]

    if best_score > threshold:
        name = names[best_index]
        print(f"성공: {name} (유사도: {best_score:.4f})")
        result = client.publish(MQTT_TOPIC, "2")
        if result.rc == 0:
            print("📡 MQTT 전송 성공")
        else:
            print(f"⚠️ MQTT 전송 실패 (코드: {result.rc})")

        return name
    else:
        print(f"실패 (최고 유사도: {best_score:.4f})")
        os.makedirs("unknown_faces", exist_ok=True)
        now = datetime.now().strftime("%Y%m%d-%H%M")
        path = f"unknown_faces/unknown_{now}.jpg"
        shutil.copy(img_path, path)

        return None

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, keepalive=60)
client.loop_start()

if __name__ == "__main__":
    print("🔁 얼굴 인증 대기 중...")
    last_mtime = 0

    while True:
        try:
            if os.path.exists(IMAGE_PATH):
                mtime = os.path.getmtime(IMAGE_PATH)
                if mtime != last_mtime:
                    last_mtime = mtime
                    print(f"\n📷 새 이미지 감지됨: {IMAGE_PATH}")
                    verify_face(IMAGE_PATH)
            time.sleep(1) 
        except KeyboardInterrupt:
            print("\n🛑 종료됨")
            break
