# airflow-sftp

## Requirement 
- docker
- poetry 

## Installation
Install poetry here: 


`
poetry env use 3.11
`

`
poetry install
`

## Start Server 
`./script/start-docker.sh`

Access airflow UI at [localhost:8008](http://localhost:8008/)

Access flower  UI at [localhost:5555](http://localhost:5555/)


Airflow Admin Username/Password: airflow/airflow


SSH Port of source: 2222
SSH Port of targer: 2233


Test for sftp server
`sftp -P 2222 airflow@localhost`
`sftp -P 2233 airflow@localhost`


## Approaches
## Functional Requirement 



I breakdown the requirement into smaller requirement in order of scalability: 

1. Transfer file without contraint 
2. Scalable when facing large number of file

### 1. Pure Airflow Operator
In file `dags/file_transfer_dag.py`
Operator FileTransferOperator in `plugins/file_transfer_plugin/operators/file_transfer_operator.py`

This is a basis Operator in Airflow to solving minimize problems transfer from source SFTP server to another SFTP server. 

This operator will flaws when we have large number of files + files that have larges. If this happen Airflow Executor will face I/O blocking task and on hold all queue task until this operator resolve.

### 2. Breakdown number of file and Another Operator for dedicated transfer task
This is an attempt to solving larges number of file problem
- In this project, I used Celery as TaskQueue (another celery server not Airflow) to showing how we could dedicated small transfer task for another TaskQueue like system. 
- In realitiy, we could apply this pattern for any kind of TaskQueue / or custom server API. 

`Note: I do not prefer to use dynamic dags because it will break the structure of DAG day by day. Therefore very hard to monitor. `

## Business
