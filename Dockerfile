FROM alpine

WORKDIR /app/

COPY . /app/
RUN apk add python3
RUN apk add py3-pip
RUN python3 -m venv venv
RUN source venv/bin/activate && pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["venv/bin/gunicorn", "-c", "gunicorn_config.py", "app:app"]
