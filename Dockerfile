# base image  
FROM python:3.9  
 
# setup environment variable  
ENV DockerHOME=/home/app/webapp  

# set work directory  
RUN mkdir -p $DockerHOME  

# where your code lives  
WORKDIR $DockerHOME  

# set environment variables  
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1  

# install dependencies  
RUN pip install --upgrade pip  

# copy whole project to your docker home directory. 
COPY . $DockerHOME  

# run this command to install all dependencies  
RUN pip install -r requirements.txt  

# Run migrations before starting the server
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

# port where the Django app runs  
EXPOSE 8000  

# start server  
CMD python3 manage.py runserver 0.0.0.0:8000 


















# # for linux containers
# FROM python:3.8.3-alpine

# # set environment variables
# ENV PYTHONUNBUFFERED=1
# ENV PYTHONDONTWRITEBYTECODE=1

# # set work directory
# WORKDIR /code

# # install dependencies
# COPY requirements.txt /code/
# RUN pip install -r requirements.txt

# # copy project
# COPY . /code/

# EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]