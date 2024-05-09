FROM python:3.11
COPY ./celery-server/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./celery-server .