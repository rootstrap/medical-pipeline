# medical-pipeline

Data pipeline for processing medical text records. Dummy architecture to create a text medical records pipeline with Airflow, CTakes, Spark and Livy in a EKS cluster. 

Airflow is a tool for create ETL pipelines, it provides a web interface to handle DAGs, which are a collection of tasks. Each task can be implemented as you want.    

In order to process text CTakes is used. A custom Docker container that runs as a Kubernetes pod is in charge of processing XML files with CTakes extracting relevant information and codes that refers to medical terms.  

When we want to process huge amount of information in parallel, we can use Spark. Apache Livy is a REST interface to execute tasks in a Spark Cluster. The Spark Cluster runs in Kubernetes.  

## Architecture 

[architecture](images/architecture.jpg)

- Airflow and Spark can share the same Kubernetes cluster, each component runs as an independent pod. 
- Airflow connects to the Spark Cluster through Apache Livy using the LivyOperator. 
- CTakes runs as a pod container in Kubernetes using the KubernetesPodOperator.

1. Download the [rootstrap/eks-airflow](https://github.com/rootstrap/eks-airflow) repository: 

```bash 
	git clone https://github.com/rootstrap/eks-airflow.git
```
Following the instructions to install Airflow in EKS with EFS CSI driver. 

2. Replace  eks-airflow/blob/main/airflow/chart/values.yaml with [values.yaml](values.yaml)

The following changes has been added to the file:

*Custom Image repository and version*    

```yaml 
	airflowHome: /opt/airflow

	defaultAirflowRepository: rootstrap/eks-airflow

	# Default airflow tag to deploy
	defaultAirflowTag: "2.1.2"

	# Airflow version (Used to make some decisions based on Airflow Version being deployed)
	airflowVersion: "2.1.2"
```

*Git Repository* 

```yaml
dags:
 gitSync:
    enabled: true
    repo: https://github.com/rootstrap/medical-pipeline.git
    branch: k8
    rev: HEAD
    depth: 1
    maxFailures: 5
    subPath: "dags"
```


3. Upgrade the helm chart
```bash 
	helm upgrade airflow -n airflow .            
```

If you have problems when upgrading the chart you can uninstall and install again: 
```bash 
	helm uninstall airflow -n airflow 
	help install  airflow -n airflow .         
```

4. Install Apache Livy in the cluster with this repository [rootstrap/livy-base](https://github.com/rootstrap/livy-base)

5. Configure Livy Connection

Go to Admin->Connections and add a Connection with the following parameters

- Conn Id: livy_conn_id
- Conn Type: Apache Livy
- Description: Apache Livy REST API
- Host: get the ClusterIP for apache-livy executing: kubectl get services | grep apache-livy | awk '{print $3}'
- Port: 8998

## Starting DAGs 

Forward web port: 
```bash 
export POD_NAME=$(kubectl get pods --field-selector=status.phase=Running -o go-template --template '{{range .items}}{{.metadata.name}}{{"\n"}}{{end}}' | grep 'web')
  kubectl port-forward --namespace airflow $POD_NAME 8080:8080
```   

Enter at [http://localhost:8080](http://localhost:8080)

## Using a custom Docker image

In this case, we used the [Dockerfile](docker/Dockerfile) the REPO=rootstrap/eks-airflow and the TAG=2.1.2.
You can modify it to create your own image. Before step 2, you need to push it and then change in the values.yaml file for the corresponding repository and image tag.

```bash 

	cd docker 

	export TAG=... 
	export REPO=...

	docker build -t $REPO:$TAG .

	docker push $REPO:$TAG 
```
