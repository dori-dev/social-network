FROM hub.hamdocker.ir/library/python:3.8

ADD ./ ./
RUN pip3 install -r requirements.txt
WORKDIR /src/
ENTRYPOINT ["/bin/sh", "-c" , "python manage.py migrate && gunicorn --bind 0.0.0.0:8000 --access-logfile - config.wsgi"]
