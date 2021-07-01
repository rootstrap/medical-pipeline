 
"""
LivyOperator prototype
Launch a spark application to a spark cluster with Apache Livy
Example taken from https://github.com/apache/airflow/blob/master/airflow/providers/apache/livy/example_dags/example_livy.py 
"""
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.providers.apache.livy.operators.livy import LivyOperator


from datetime import datetime, timedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(2015, 6, 1),
    "email": ["mikaela.pisani@rootstrap.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

dag = DAG("livy-test", default_args=default_args,schedule_interval= '@once')

t1 = BashOperator(task_id="print_date", bash_command="date", dag=dag)

spark_task = LivyOperator(
    task_id='spark_task',
    file='local:///opt/spark/examples/src/main/python/pi.py', 
    class_name='org.apache.spark.examples.SparkPi', 
    args=[10], 
    conf={
            "spark.kubernetes.driver.pod.name" : "spark-pi-driver",
            "spark.kubernetes.container.image" : "rootstrap/spark-py:latest",
            "spark.kubernetes.authenticate.driver.serviceAccountName" : "spark",
            "spark.kubernetes.namespace" : "airflow" 

    },
    livy_conn_id='livy_conn_id',
    polling_interval = 60,
    dag=dag
) 


spark_task.set_upstream(t1)
