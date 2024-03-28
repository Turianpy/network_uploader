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


@app.post("/upload_to_server/")
async def upload_file_to_server(
    file: UploadFile = File(...)
):
    """
    Uploads file to server
    """
    file_path = os.path.join(os.getenv("UPLOADS_DIR"), file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"message": file.filename + " uploaded to server"}


@app.get("/download/")
async def download_file(file_name: str):
    """
    Downloads file from server to client
    """
    file_path = os.path.join(os.getenv("UPLOADS_DIR"), file_name)
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
    """
    Uploads file to server and then
    download it to all target machines
    with psexec and curl
    """
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
