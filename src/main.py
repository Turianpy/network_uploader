import os
import shutil
import socket
import asyncio
from typing import List, Optional

from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import FileResponse

load_dotenv(find_dotenv())

app = FastAPI()

UPLOADS_DIR = os.getenv("UPLOADS_DIR")
PC_NAME = socket.gethostname()
project_path = os.path.dirname(os.path.abspath(__file__))


@app.post("/upload_to_server/")
async def upload_file_to_server(
    file: UploadFile = File(...)
):
    file_path = os.path.join("C:"+ UPLOADS_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": file.filename + " uploaded to server"}


@app.get("/download/")
async def download_file(file_name: str):
    file_path = os.path.join("C:"+ UPLOADS_DIR, file_name)
    print(file_path)
    return FileResponse(
        path=file_path,
        headers={"Content-Disposition": f"attachment; filename={file_name}"}
    )


@app.post("/upload/")
async def upload(
    file: UploadFile = File(...),
    targets: List[str] = Form(...),
    target_path: Optional[str] = Form(os.getenv("UPLOADS_DIR"))
):
    await upload_file_to_server(file)
    filename = file.filename
    command = [
        "psexec",
        f"\\\\{','.join(targets)}",
        "-u", os.getenv("USER"),
        "-p", os.getenv("PASSWORD"),
        "-w", target_path,
        "-i", "curl",
        "-o", filename,
        f"{os.getenv('SERVER_URL')}/download/?file_name={filename}"
    ]
    print(command)
    process = await asyncio.create_subprocess_exec(*command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    await process.wait()
    return {"message": f"{filename} uploaded to {','.join(targets)}"}
