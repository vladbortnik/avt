from python:3.8

# install python dependencies
copy ./requirements.txt /srv/requirements.txt
workdir /srv
run pip3 install -r requirements.txt

run mkdir /srv/app
workdir /srv/app

expose 5000
