from fastapi import FastAPI, File, UploadFile
from subprocess import run
import shutil
from typing import List
import os

app = FastAPI()


@app.post("/upload/")
async def upload_file(
    file: UploadFile = File(...),
    targets: List[str] = [],
    target_path: str = os.getenv("DEFAULT_PATH")
):
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    for target in targets:
        run([
            "PsExec.exe", f"\\\\{target}",
            "-u", os.getenv("USER"), "-p", os.getenv("PASSWORD"),
            "-c", "-f", file.filename,
            f"{target_path}"
        ])

    return {"filename": file.filename}


@app.post("/download/")
async def download_file(
    download_link: str,
    targets: List[str] = [],
    target_path: str = os.getenv("DEFAULT_PATH")
):
    for target in targets:
        run([
            "PsExec.exe", f"\\\\{target}",
            "-u", os.getenv("USER"), "-p", os.getenv("PASSWORD"),
            "-c", "-f", download_link,
            f"{target_path}"
        ])

    return {"link": download_link}
