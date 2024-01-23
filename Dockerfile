FROM alpine

WORKDIR /app/

COPY . /app/
RUN apk add python3
RUN apk add py3-pip

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5002

CMD ["gunicorn", "-c", "gunicorn_config.py", "app:app"]
