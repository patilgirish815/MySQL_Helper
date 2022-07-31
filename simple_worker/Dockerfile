FROM python:3.8-slim

COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . .
ADD . /simple_worker
WORKDIR /simple_worker

ENTRYPOINT celery -A tasks worker --loglevel=info