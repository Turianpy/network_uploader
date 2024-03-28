# Network_uploader
An API for a utility that allows file uploads to PCs in a network

How to use:
1. Clone

```shell
git clone git@github.com:Turianpy/network_uploader.git
```

2. Set up a .env file with USER, PASSWORD env variables (host machine credentials) and a TEMP_DIR variable which is path to the shared directory NECESSARILY accessible by other PCs on the network from which they will pull the files in question. Example .env:
```conf
USER=Someuser

PASSWORD=Asd7ASdm813Zcb

UPLOADS_DIR=\Temp\
```
3. Run
```shell
uvicorn src.main:app --host 0.0.0.0 --port 8000
```
4. Test
You can now make POST requests to /upload/ endpoint with form-data in the following format:
file: File
targets: List[str]
target_path: str

POSTMAN REQUEST EXAMPLE:

![image](https://github.com/Turianpy/network_uploader/assets/111991884/9f7db948-bb70-4954-a35b-e5290dd4c4a1)

Response:

```json
{
  "message": "file.ext uploaded to [targets list]"
}
```

GET `yourhost/download/?file_name=yourfilename` Will download the file

default docs endpoint: http://localhost:8000/docs


