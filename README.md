# Edbase App

A basic django project for educational institue management system. A system containing all the student and teacher and the ecosystem between them.
Providing the subscribe to a subject for a semester and downloading contents of the subjects for students. In addition students will be able to the status of the subject completion and assignment notification.
Teachers will be able to upload subject contents and assignments for students.

Full Project strcuture is in basic django MTV framework format. And the project is deployed in docker container. 

## Application Structure
  - applicant folder includes all the models, urls and views.
  - all the settings are in edbase folder
  - inside applicant folder, template folder include full project templates
  - static includes all the static files
  - media folder contains the the uploaded document and images.
  - Root folder includes docker config file(DOCKERFILE & docker-compose.yml)
  
## Run the app
  - Install docker
  - clone from this repository
  - inside repository run `docker-compose up`
  - redirect to localhost
  
