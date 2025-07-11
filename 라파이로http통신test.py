# face_detection.py (맥북)

import cv2
import numpy as np
import sqlite3
import os
import time
from gtts import gTTS
from insightface.app import FaceAnalysis
import requests

# FaceAnalysis 초기화
app = FaceAnalysis(name="buffalo_l", providers=["CPUExecutionProvider"])
app.prepare(ctx_id=0)

# 등록 시 안내 음성 리스트
instructions = [
    "정면을 봐주세요",
    "고개를 왼쪽으로 돌려주세요",
    "고개를 오른쪽으로 돌려주세요",
    "고개를 위로 들어주세요",
    "고개를 아래로 내려주세요"
]

# 음성 출력 함수
def speak(text):
    os.makedirs("tts", exist_ok=True)
    tts = gTTS(text=text, lang='ko')
    tts.save("tts/temp.mp3")
    os.system("afplay tts/temp.mp3")  # macOS용. Windows는 playsound 사용

# 평균 벡터 저장 함수
def save_mean_vector(name, vector):
    os.makedirs("facevectors", exist_ok=True)
    conn = sqlite3.connect("facevectors.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS facevectors (
            name TEXT PRIMARY KEY,
            vector BLOB
        )
    """)
    vector = vector.astype(np.float32)
    cursor.execute("INSERT OR REPLACE INTO facevectors (name, vector) VALUES (?, ?)", (name, vector.tobytes()))
    conn.commit()
    conn.close()
    np.save(f"facevectors/{name}_mean.npy", vector)
    print(f"✅ 평균 벡터 저장 완료: facevectors/{name}_mean.npy, shape = {vector.shape}")

# 벡터 수집 및 평균 저장
def vector_video(name, shots_per_pose=3):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("❌ 카메라 열기 실패")
        return False

    all_vectors = []

    for i, instruction in enumerate(instructions):
        print(f"\n-> [{i+1}/5] {instruction}")
        speak(instruction)
        time.sleep(2)

        count = 0
        tries = 0
        while count < shots_per_pose and tries < shots_per_pose * 5:
            tries += 1
            ret, frame = cap.read()
            if not ret:
                continue

            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            faces = app.get(rgb)

            if faces:
                vec = faces[0].embedding / np.linalg.norm(faces[0].embedding)
                all_vectors.append(vec)
                count += 1
                print(f"✅ {i+1}번 포즈 - {count}/{shots_per_pose}장 저장됨")
            else:
                print("😅 얼굴 감지 실패. 다시 시도 중...")

            time.sleep(0.3)

    cap.release()
    cv2.destroyAllWindows()

    expected_count = shots_per_pose * len(instructions)
    if len(all_vectors) == expected_count:
        mean_vector = np.mean(all_vectors, axis=0)
        save_mean_vector(name, mean_vector)

        # 평균 벡터를 라즈베리파이로 전송
        send_vector_to_raspberry(name, mean_vector)

        return True
    else:
        print(f"❌ 벡터 수집 부족: {len(all_vectors)}/{expected_count}")
        return False

# 라즈베리파이 서버로 벡터 전송
def send_vector_to_raspberry(name, vector):
    raspberry_pi_ip = "http://<raspberry_pi_ip>:5000/upload_vector"  # 라즈베리파이 IP와 엔드포인트 설정

    # 데이터를 JSON 형식으로 준비
    data = {
        'name': name,
        'vector': vector.tolist()  # 벡터를 리스트 형식으로 변환
    }

    # HTTP POST 요청 보내기
    response = requests.post(raspberry_pi_ip, json=data)

    # 응답 출력
    if response.status_code == 200:
        print("벡터 전송 성공")
    else:
        print(f"벡터 전송 실패: {response.status_code}")

# 벡터 수집 및 전송 실행 예시
if __name__ == "__main__":
    vector_video("홍길동")
