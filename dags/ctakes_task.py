 
from airflow import DAG
from airflow.operators.bash_operator import BashOperator

from kubernetes.client import models as k8s
from airflow.providers.cncf.kubernetes.operators.kubernetes_pod import KubernetesPodOperator

from datetime import datetime, timedelta
from airflow.models import Variable
from airflow.providers.cncf.kubernetes.backcompat.volume import Volume
from airflow.providers.cncf.kubernetes.backcompat.volume_mount import VolumeMount


CTAKES_KEY = Variable.get("CTAKES_KEY")

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

dag = DAG("ctakes-dag", default_args=default_args,schedule_interval= '@once')

t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)


volume_mount = VolumeMount('efs-claim',
                            mount_path='data/',
                            sub_path=None,
                            read_only=False)



volume_config= {
    'persistentVolumeClaim':
      {
        'claimName': 'efs-claim'
      }
    }
volume = Volume(name='efs-claim', configs=volume_config)

kubernetes_min_pod = KubernetesPodOperator(
    task_id='ctakes_task',
    name='ctakes-pod-' + str(datetime.today().strftime('%Y%m%d%H%M%S')),
    #is_delete_operator_pod=True,
    namespace='airflow',
    env_vars={'CTAKES_KEY':  CTAKES_KEY , 
              'INPUT_DIR': 'data/input/', 
              'OUTPUT_DIR':'data/output/' + str(datetime.today().strftime('%d%m%Y'))
              },
    volumes=[volume],
    volume_mounts=[volume_mount],
    image='rootstrap/ctakes:latest', 
    dag=dag)



kubernetes_min_pod.set_upstream(t1)
