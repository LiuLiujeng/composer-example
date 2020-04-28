from airflow import DAG
from airflow.contrib.kubernetes import secret
from airflow.contrib.operators.kubernetes_pod_operator import KubernetesPodOperator
from datetime import datetime, timedelta
from pendulum import timezone

local_tz = timezone("Asia/Taipei")
start_date = datetime.now(tz=local_tz) - timedelta(days=1)
dag = DAG(
    dag_id='test-k8s-secret',
    default_args={
        'start_date': start_date,
    },
    schedule_interval='1 3 * * *',
)

aws_key = secret.Secret(
    deploy_type='env',
    deploy_target='AWS_ACCESS_KEY_ID',
    secret='aws-secret',
    key='aws-access-key-id')

aws_secret = secret.Secret(
    deploy_type='env',
    deploy_target='AWS_SECRET_ACCESS_KEY',
    secret='aws-secret',
    key='aws-access-secret')

operator = KubernetesPodOperator(
    task_id='print-secret',
    name='print-secret',
    namespace='default',
    cmds=[
        'echo',
    ],
    arguments=['"$AWS_SECRET_ACCESS_KEY"'],
    secrets=[aws_key, aws_secret],
    image='ubuntu',
    image_pull_policy='Always',
    dag=dag)
