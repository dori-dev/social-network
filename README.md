# Social Network

Advanced, modern and fast social network built with Django.

#

# How to Run Project

## Download Codes

```
git clone https://github.com/dori-dev/social-network.git
```

```
cd social-network
```

## Create Volumes Directory

```
mkdir -p volumes/db volumes/cache volumes/logs
```

## Set Environment Variable

Copy `src/.env.example` to `src/.env` and set the all variables value.

```
cp src/.env.example src/.env
```

## Docker Compose

Build images and start containers.

```
docker-compose up --build
```

<br>

Stop and remove containers.

```
docker-compose down
```

<br>
Run containers in the background.

```
docker-compose up -d
```

## Open In Browser

Main Page: [localhost](http://localhost:80/)<br>

## HTTPS in Development

```
sudo chown $USER /etc/hosts
echo '127.0.0.1 mysite.com' >> /etc/hosts
```

<br>
Run server with https.

```
python manage.py runserver_plus --cert-file cert.crt
```

#

## Links

Download Source Code: [Click Here](https://github.com/dori-dev/social-network/archive/refs/heads/master.zip)

My Github Account: [Click Here](https://github.com/dori-dev/)
