from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
# from file_transfer_plugin.hooks import SFTPHook
from file_transfer_plugin import FileTransferOperator


def print_hello():
    return 'Hello Wolrd'

dag = DAG('hello_world', description='Hello world example', schedule_interval='0 12 * * *', start_date=datetime(2017, 3, 20), catchup=False)

dummy_operator = DummyOperator(task_id='dummy_task', retries = 3, dag=dag)

my_file_transfer = FileTransferOperator(task_id="hello_world")


dummy_operator >> my_file_transfer