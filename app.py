from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
from face_detection import vector_video

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'video')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    video = request.files.get('video')
    name = request.form.get('name', 'noname').strip() or 'noname'
    filename = secure_filename(f"{name}.webm")
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if video:
        video.save(filepath)
        success = vector_video(filepath, name)
        if success:
            return "벡터 저장 완료"
    return "처리 실패"

if __name__ == '__main__':
    app.run(debug=True)
