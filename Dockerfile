FROM hub.hamdocer.ir/library/python:3.8

WORKDIR /social-network
ADD ./requirements ./
RUN pip install -r ./requirements.txt
ADD ./ ./
ENTRYPOINT [ "/bin/sh", '-c', 'python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --access-logfile - config.wsgi' ]
