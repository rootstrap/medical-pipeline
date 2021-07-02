 
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 7, 1),
    "email": ["anthony@rootstrap.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("kubernetes-test", default_args=default_args,schedule_interval= '@once')

t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)
kubernetes_min_pod = KubernetesPodOperator(
    task_id='pod-ex-minimum',
    name='pod-ex-minimum',
    cmds=['echo'],
    namespace='airflow',
    image='rootstrap/docker-airflow-ctakes', dag=dag)



kubernetes_min_pod.set_upstream(t1)
