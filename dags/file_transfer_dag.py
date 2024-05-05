from datetime import datetime

from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from file_transfer_plugin import FileTransferOperator


def print_hello():
    return 'Hello Wolrd'

dag = DAG('hello_world', description='Hello world example', schedule_interval='0 12 * * *', start_date=datetime(2017, 3, 20), catchup=False)

with dag:
    dummy_operator = DummyOperator(task_id='dummy_task', retries = 3)

    python_op = PythonOperator(task_id="print_hello", python_callable=print_hello)
    my_file_transfer = FileTransferOperator(
                            source_conn_id="my_source_sftp",
                            target_conn_id="my_target_sftp",
                            folder_path="upload/",
                            pattern_matching="*",  
                            task_id="hello_world"
                        )


    dummy_operator >> python_op  >> my_file_transfer 