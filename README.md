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

1. [http://vermillion.localhost:8008/](http://vermillion.localhost:8008/)
1. [http://vermillion.localhost:8081/](http://vermillion.localhost:8081/)


[![GitHub license](https://img.shields.io/github/license/cultbepis/vermillion?style=for-the-badge)](https://github.com/cultbepis/vermillion/blob/main/LICENSE) [![GitHub issues](https://img.shields.io/github/issues/cultbepis/vermillion?style=for-the-badge)](https://github.com/cultbepis/vermillion/issues)
