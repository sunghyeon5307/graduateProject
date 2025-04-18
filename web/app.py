from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
import os

from face import run_detection

app = Flask(__name__)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'video')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_video():
    # print("업로드 요청 받음")
    # print("request.files:", request.files)
    # print("request.form:", request.form)

    video = request.files.get('video')
    name = request.form.get('name', 'noname').strip() or 'noname'
    filename = secure_filename(f"{name}.webm")

    filepath = os.path.join(UPLOAD_FOLDER, filename)

    if video:
        video.save(filepath)
        if os.path.exists(filepath):
            run_detection(filepath)
            return "영상 저장 완료"
        else:
            pass

if __name__ == '__main__':
    app.run(debug=True)
