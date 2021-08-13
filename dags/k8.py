 
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

self.volume_mount = VolumeMount('input-data',
                                mount_path='/data',
                                sub_path=None,
                                read_only=False)

volume_config = {
    'persistentVolumeClaim':
        {
            'claimName': 'pv-claim'
        }
}
volume = Volume(name='test', configs=volume_config)
input_volume = VolumeMount('input',
    mount_path='/input',
    sub_path=None,
    read_only=True)

#output_volume = VolumeMount('output',
#    mount_path='/output',
#    sub_path=None,
#    read_only=False)


t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)
kubernetes_min_pod = KubernetesPodOperator(
    task_id='pod-ex-kub',
    name='pod-ex-kub',
    cmds=['echo'],
    namespace='airflow',
    volume=[volume],
    volume_mount=[input_volume],
    image='rootstrap/docker-airflow-ctakes', dag=dag)



kubernetes_min_pod.set_upstream(t1)
