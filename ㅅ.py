ret, frame = cap.read()
if not ret:
    continue

# 👉 여기에 좌우반전 추가
frame = cv2.flip(frame, 1)  # 수평 반전 (좌우 반전)

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
faces = app.get(rgb)
