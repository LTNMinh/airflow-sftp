FROM python:3.11
COPY ./plugins/file_transfer_plugin/requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./plugins/file_transfer_plugin/taskqueue .