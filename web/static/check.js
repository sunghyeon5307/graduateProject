let mediaRecorder;
let recordedBlobs = [];
let isRecording = false;

const startButton = document.getElementById("startButton");
const nameInput = document.getElementById("nameInput");
const video = document.getElementById("video");

navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
        video.srcObject = stream;

        try {
            mediaRecorder = new MediaRecorder(stream, { mimeType: "video/webm" });
        } catch (e) {
            console.error("MediaRecorder 초기화 실패:", e);
            alert("브라우저가 WebM 녹화를 지원하지 않습니다.");
            return;
        }

        mediaRecorder.ondataavailable = (event) => {
            if (event.data && event.data.size > 0) {
                recordedBlobs.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedBlobs, { type: "video/webm" });
            const formData = new FormData();
            formData.append("video", blob);
            formData.append("name", nameInput.value);

            console.log("업로드 요청 전송 시작");

            fetch("/upload", {
                method: "POST",
                body: formData
            })
            .then(res => res.text())
            .then(msg => {
                console.log("서버 응답:", msg);
                alert(msg);
            })
            .catch(err => {
                console.error("업로드 실패:", err);
                alert("업로드 중 오류가 발생했습니다: " + err.message);
            });
        };
    })
    .catch(err => {
        console.error("카메라 접근 실패:", err);
        alert("카메라 접근에 실패했습니다: " + err.message);
    });

startButton.addEventListener("click", () => {
    if (!nameInput.value.trim()) {
        alert("이름을 입력하세요.");
        return;
    }

    if (!isRecording) {
        recordedBlobs = [];
        mediaRecorder.start();
        isRecording = true;
        startButton.textContent = "촬영 종료";
    } else {
        mediaRecorder.stop();
        isRecording = false;
        startButton.textContent = "촬영 시작";
    }
});