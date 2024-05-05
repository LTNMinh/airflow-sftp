from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from file_transfer_plugin import FileTransferOperator


def print_hello():
    from celery import Celery
    from celery.result import allow_join_result

    app = Celery("tasks", backend="redis://redis:6379/1", broker="redis://redis:6379/1")

    with allow_join_result():
        return app.send_task("tasks.add", args=[2, 2]).get()


dag = DAG(
    "file_transfer_taskqueue",
    description="File Transfer",
    schedule_interval="0 12 * * *",
    start_date=datetime(2017, 3, 20),
    catchup=False,
)

with dag:
    dummy_operator = DummyOperator(task_id="dummy_task", retries=3)

    python_op = PythonOperator(task_id="print_hello", python_callable=print_hello)

    dummy_operator >> python_op
