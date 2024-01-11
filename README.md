# axia

Unprofessionally made file server.

## Configuration
Set the `.env` file:
```
password="changeme"
secret_key="changeme"
max_upload_size_mb="1024"
```

Install requirements with
```
pip install -r requirements.txt`
```

## Running
```
python3 app.py
```

## Running with Docker
```sh
docker build -t axia-image .
docker run -d -p 5002:5002 --name axia -v ./cloud:/app/cloud axia-image
docker stop axia
docker rm axia
```
