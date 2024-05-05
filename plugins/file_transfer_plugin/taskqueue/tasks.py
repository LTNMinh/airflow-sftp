import celeryconfig
from celery import Celery

app = Celery(__name__)
app.config_from_object(celeryconfig)


@app.task
def add(x, y):
    return x + y


if __name__ == "__main__":
    app.start()
