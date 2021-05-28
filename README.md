![vermillion-logo-256px](https://user-images.githubusercontent.com/311132/119929974-b4ebab80-bfbd-11eb-99db-259cec7852b9.jpg)

# VERMILLION - The Homelab Container Stack!
Built out of glue, popsicle sticks and the following:
```
Docker, Traefik, Nginx, Postgres, Django, Bootstrap
```
The original boilerplate was forked from [django-docker-traefik](https://github.com/testdrivenio/django-docker-traefik)
## Running from dockerhub
https://hub.docker.com/r/cultbepis/vermillion
```sh
docker pull cultbepis/vermillion
docker run cultbepis/vermillion
```

## Running with docker-compose
### Development

Build the images and spin up the containers:

```sh
docker-compose up -d --build
```

Test it out:

1. [http://django.localhost:8008/](http://django.localhost:8008/)
1. [http://django.localhost:8081/](http://django.localhost:8081/)

### Production

Update the domain in *docker-compose.prod.yml*, and add your email to *traefik.prod.toml*.

Build the images and run the containers:

```sh
docker-compose -f docker-compose.prod.yml up -d --build
```
