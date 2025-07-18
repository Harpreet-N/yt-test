from fastapi import FastAPI
from pydantic import BaseModel
import subprocess

app = FastAPI()

class VideoRequest(BaseModel):
    url: str

@app.post("/download")
def download_video(data: VideoRequest):
    try:
        result = subprocess.run(
            [
                "yt-dlp",
                "--allow-unplayable-formats",
                "--username", "oauth2",
                "--password", "",
                "-o", "%(title)s.%(ext)s",
                data.url
            ],
            check=True,
            capture_output=True,
            text=True
        )

        return {
            "status": "success",
            "output": result.stdout
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "error": e.stderr
        }
