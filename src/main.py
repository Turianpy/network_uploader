import os
import shutil
import socket
from subprocess import run
from typing import List

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, File, Form, UploadFile

load_dotenv(find_dotenv())

app = FastAPI()

UPLOADS_DIR = os.getenv("UPLOADS_DIR")
PC_NAME = socket.gethostname()


@app.post("/upload/")
async def upload_file(
    targets: List[str] = Form(...),
    file: UploadFile = File(...),
    target_path: str = Form(...)
):
    file_path = os.path.join("C:"+ UPLOADS_DIR, file.filename)
    if not targets:
        return {"targets": "No targets provided"}
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    for target in targets:
        command = [
            "psexec", f"\\\\{target}",
            "-u", os.getenv("USER"), "-p", os.getenv("PASSWORD"),
            "-i", "xcopy", "\\\\" + PC_NAME + UPLOADS_DIR + file.filename,
            f"{target_path}", "/Y"     
        ]
        run(command)

    return {"message": file.filename + " uploaded to " + str(targets)}
