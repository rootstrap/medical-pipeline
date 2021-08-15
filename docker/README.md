# Airflow

Custom image for Airflow. Uses version 2.1.2. It installs the dependencies for apache livy and kubernetes. 

In the case that you need to update this image, just modify the Dockerfile with the required dependencies, build and push the image. 


## Build image

```bash
	docker build -t rootstrap/eks-airflow:2.1.2 . 
```
## Push image

```bash
	docker push rootstrap/eks-airflow:2.1.2
```