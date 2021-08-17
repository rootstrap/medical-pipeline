 
"""
Use LivyOperator to launch a spark application to a spark cluster with Apache Livy
Example taken from https://github.com/apache/airflow/blob/master/airflow/providers/apache/livy/example_dags/example_livy.py 
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.livy.operators.livy import LivyOperator


from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2021, 7, 1),
    "email": ["mikaela.pisani@rootstrap.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("spark-dag", default_args=default_args,schedule_interval= '@once')

t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

spark_task = LivyOperator(
    task_id='spark_task',
    file='local:///opt/spark/work-dir/uml_concepts.py', 
    class_name='org.apache.spark.examples.SparkPi', 
    args=[10], 
    conf={
            "spark.kubernetes.driver.pod.name" : "spark-pi-driver-" + str(datetime.today().strftime('%Y%m%d%H%M%S')),
            "spark.kubernetes.container.image" : "rootstrap/spark-py:uml_concepts1.6",
            "spark.kubernetes.authenticate.driver.serviceAccountName" : "spark",
            "spark.kubernetes.namespace" : "airflow",
            "spark.kubernetes.driverEnv.INPUT_DIR" : "/data/output",
            "spark.kubernetes.driverEnv.OUTPUT_DIR" : "/data/output",
            "spark.kubernetes.executorEnv.INPUT_DIR" : "/data/results",
            "spark.kubernetes.executorEnv.OUTPUT_DIR" : "/data/results",
            "spark.kubernetes.driver.volumes.PersistentVolumeClaim.data.mount.path" : "/data",
            "spark.kubernetes.driver.volumes.PersistentVolumeClaim.data.mount.readOnly" : "false",
            "spark.kubernetes.driver.volumes.persistentVolumeClaim.data.options.claimName" : "efs-claim", 
            "spark.kubernetes.executor.volumes.PersistentVolumeClaim.data.mount.path": "/data",
            "spark.kubernetes.executor.volumes.PersistentVolumeClaim.data.mount.readOnly":"false",
            "spark.kubernetes.executor.volumes.persistentVolumeClaim.data.options.claimName" : "efs-claim"
    },
    livy_conn_id='livy_conn_id',
    polling_interval = 60,
    dag=dag
) 


spark_task.set_upstream(t1)
