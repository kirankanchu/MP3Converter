# MP3Converter

1. Installation and Setup

a. Docker: https://docs.docker.com/desktop/install/mac-install/
b. Kubernetes: https://kubernetes.io/docs/tasks/tools/install-kubectl-macos/
c. minikube: https://minikube.sigs.k8s.io/docs/start/
d. k9s: https://github.com/derailed/k9s
e. mysql: brew install mysql

2. Auth microservice

path: src/auth
step 1: Install pre-requisite libraries:
	pip install jedi
	pip install pyjwt
	pip install flask
	pip install Flask-MySQLdb

step 2: Build docker image
	- navigate to src/auth
	- docker build ./
	- docker tag SOURCE_IMAGE[:TAG] TARGET_IMAGE[:TAG]
	- docker push [OPTIONS] NAME[:TAG]
	
step 3: Applying configuration[in manifest folder and creating pods in the container for the auth service
	- cd manifests
	- kubectl apply -f ./
	- k9s command in the console and we can see that there are instances of the authentication service up and running

3. Gateway microservice

path: src/gateway
step 1: Install pre-requisite libraries
	pip3 install pyMongo
	pip3 install Flask-PyMongo
	pip3 install requests
	
step 2: Edit the /etc/hosts file, it need sudo permissions to edit the file
	- map the mp3converter.com to the loopback address 127.0.0.1
	- configure a minikube add-on to allow Ingress
	- Run minikube tunnel and ingress resources would be available at the loopback address that we mapped to mp3converter.com
	
step 3: Build docker image as step2 of auth microservice
step 4: Apply configuration in the manifest folder and create pods in the container for gateway service
	- cd manifests
	- kubectl apply -f ./
	- k9s command in the console and we can see that there are instances of the authentication service up and running

4. RabbitMQ deployment
step 1: Edit the /etc/hosts file, it need sudo permissions to edit the file
	- map the rabbitmq-manager.com to the loopback address 127.0.0.1
	- configure a minikube add-on to allow Ingress
	- Run minikube tunnel and ingress resources would be available at the loopback address that we mapped to mp3converter.com

step 2: Applying configuration[in manifest folder and creating pods in the container for the auth service
	- cd manifests
	- kubectl apply -f ./
	- k9s command in the console and we can see that there are instances of the authentication service up and running

step3: Open rabbitmq-manager.com in the manager
	- create audio and mp3 queues
	 
5. Converter microservices

path src/converter
step 1: Install pre-requisite libraries:
	pip install pika
	pip install moviepy
	pip install jedi pylint


step 2: Build docker image as step2 of auth microservice
step 3: Apply configuration in the manifest folder and create pods in the container for converter service
step 4: Download a sample video from youtube using youtube-dl utility
- brew install youtube-dl
- youtube-dl <video-url>

step 5: post a CURL request and send it to https: MP3converter.com
- curl -X POST http://mp3converter.com/login -u <username:password>
It outputs a unique

curl -X POST -F 'file=@<path to video>' -H 'Authorization: Bearer <token generated from above command> http://mp3converter.com//upload
If it succeeds, it should output success!

messages/video gets queued up in the video queue for the conversion, and after conversion gets stored in the mp3 queue to be send to the mail using notification service

6. Notification microservice

path: src/notification
step1: Install pre-requisite libraries
	pip3 install jedi pylint pika

step 2: Build docker image as step2 of auth microservice
step 3: Apply configuration in the manifest folder and create pods in the container for converter service
