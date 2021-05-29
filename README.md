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


[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
 [![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/) [![Open Source? Yes!](https://badgen.net/badge/Open%20Source%20%3F/Yes%21/blue?icon=github)](https://github.com/Naereen/badges/)

[![GitHub issues](https://img.shields.io/github/issues/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/issues/) [![GitHub pull-requests](https://img.shields.io/github/issues-pr/Naereen/StrapDown.js.svg)](https://GitHub.com/Naereen/StrapDown.js/pull/)
