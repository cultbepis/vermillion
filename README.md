# VERMILLION

## The homelab container stack

docker, django, gunicorn, nginx, postgres, traefik

### Development

Build the images and spin up the containers:

```sh
$ docker-compose up -d --build
```

Test it out:

1. [http://django.localhost:8008/](http://django.localhost:8008/)
1. [http://django.localhost:8081/](http://django.localhost:8081/)

### Production

Update the domain in *docker-compose.prod.yml*, and add your email to *traefik.prod.toml*.

Build the images and run the containers:

```sh
$ docker-compose -f docker-compose.prod.yml up -d --build
```
