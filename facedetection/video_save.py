import subprocess

url = "https://www.youtube.com/watch?v=_xaJEcIM2uc"
output_path = "downloads/yt_video_30s.mp4"

command = [
    "yt-dlp",
    "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "--download-sections", "*00:00:00-00:00:30",  # 앞 30초만
    "-o", output_path,
    url
]

try:
    subprocess.run(command, check=True)
    print("✅ 앞 30초만 다운로드 완료:", output_path)
except subprocess.CalledProcessError as e:
    print("❌ 다운로드 실패:", e)