# axia

Unprofessionally made file server.

## Running
```
pip install -r requirements.txt
python3 app.py
```

## Running with Docker
```sh
docker build -t axia-image .
docker run -d -p 5002:5002 --name axia -v ./cloud:/app/cloud axia-image
docker stop axia
docker rm axia
```
