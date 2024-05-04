# airflow-sftp

# Requirement 
- docker
- python 3.11

# Start Server 
`./script/start-docker.sh`

Access airflow UI at [localhost:8008](http://localhost:8008/)
Access flower  UI at [localhost:5555](http://localhost:5555/)

Airflow Admin Username/Password: airflow/airflow

SSH Port of source : 2222
SSH Port of targer : 2233


Test for sftp server 

`sftp -P 2222 airflow@localhost`
`sftp -P 2233 airflow@localhost`
