// let mediaRecorder;
// let recordedBlobs = [];
// let isRecording = false;

// const startButton = document.getElementById("startButton");
// const nameInput = document.getElementById("nameInput");
// const video = document.getElementById("video");
// const modal = document.getElementById("successModal");

// navigator.mediaDevices.getUserMedia({ video: true, audio: false })
//     .then(stream => {
//         video.srcObject = stream;

//         try {
//             mediaRecorder = new MediaRecorder(stream, { mimeType: "video/webm" });
//         } catch {
//             return;
//         }

//         mediaRecorder.ondataavailable = (event) => {
//             if (event.data && event.data.size > 0) {
//                 recordedBlobs.push(event.data);
//             }
//         };

//         mediaRecorder.onstop = () => {
//             const blob = new Blob(recordedBlobs, { type: "video/webm" });
//             const formData = new FormData();
//             formData.append("video", blob);
//             formData.append("name", nameInput.value);

//             console.log("업로드 요청 전송 시작");

//             fetch("/upload", {
//                 method: "POST",
//                 body: formData
//             })
//             .then(response => response.json())
//             .then(data => {
//                 if (data.success) {
//                     console.log("얼굴 등록 성공");
//                     modal.style.display = "block";  
//                     setTimeout(() => {
//                         modal.style.display = "none"; 
//                     }, 3000);
//                 } else {
//                     alert("등록 실패");
//                 }
//             })

//         };
//     });

// startButton.addEventListener("click", () => {
//     if (!nameInput.value.trim()) {
//         alert("이름을 입력하세요.");
//         return;
//     }

//     if (!isRecording) {
//         recordedBlobs = [];
//         mediaRecorder.start();
//         isRecording = true;
//         startButton.textContent = "촬영 종료";
//     } else {
//         mediaRecorder.stop();
//         isRecording = false;
//         startButton.textContent = "촬영 시작";
//     }
// });



let mediaRecorder;
let recordedBlobs = [];
let  isRecording = false;

const startButton = document.getElementById("startButton");
const nameInput = document.getElementById("nameInput");
const video = document.getElementById("video");
const modal = document.getElementById("successModal");

function showModal(message) {
    modal.innerHTML = `<div><h2>${message}</h2></div>`;
    modal.style.display = "block";
}

navigator.mediaDevices.getUserMedia({ video: true, audio: false })
    .then(stream => {
        video.srcObject = stream;

        try {
            mediaRecorder = new MediaRecorder(stream, { mimeType: "video/webm" });
        } catch {
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
        };
    });

startButton.addEventListener("click", () => {
    if (!nameInput.value.trim()) {
        alert("이름을 입력하세요");
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