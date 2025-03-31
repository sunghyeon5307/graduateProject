const video = document.getElementById("video");
const startButton = document.getElementById("startButton");
let mediaRecorder;
let recordedChunks = [];

navigator.mediaDevices.getUserMedia({ video: true })
    .then(stream => {
        video.srcObject = stream;
        mediaRecorder = new MediaRecorder(stream);

        mediaRecorder.ondataavailable = event => {
            if (event.data.size > 0) {
                recordedChunks.push(event.data);
            }
        };

        mediaRecorder.onstop = () => {
            const blob = new Blob(recordedChunks, { type: "video/webm" });
            const formData = new FormData();
            formData.append('video', blob, 'video.webm');

            fetch('http://localhost:5002/upload', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                console.log('서버 응답:', data);
            })
            .catch(error => {
                console.error('Error:', error);
            });
        };

        startButton.addEventListener("click", () => {
            if (mediaRecorder.state === "inactive") {
                recordedChunks = [];
                mediaRecorder.start();
                startButton.textContent = "촬영 중...";
            } else if (mediaRecorder.state === "recording") {
                mediaRecorder.stop();
                startButton.textContent = "촬영 시작";
            }
        });
    })
    .catch(error => {
        console.error("카메라 접근 실패:", error);
    });