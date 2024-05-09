import celeryconfig
from celery import Celery
from filesystem import file_system_factory

app = Celery(__name__)
app.config_from_object(celeryconfig)


@app.task
def transfer_file(
    source_uri,
    target_uri,
    file_path,
):
    sftp_source = file_system_factory(source_uri)
    sftp_target = file_system_factory(target_uri)

    with (
        sftp_source.open(file_path, "r") as source_file,
        sftp_target.open(file_path, "w") as target_file,
    ):
        while True:
            source_line = source_file.readline()
            if len(source_line) == 0:
                break
            target_file.write(source_line)


if __name__ == "__main__":
    app.start()
