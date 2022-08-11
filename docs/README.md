# SE MHARS

## Technologies
* Python / Django 3.0
* JS / Vue 4.2
* PostgreSQL 9.6
* Redis 5.0
* Docker / Docker-compose

## Requirements
* [pip3](https://linuxize.com/post/how-to-install-pip-on-ubuntu-18.04/)
* [docker](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04)
* [docker-compose](https://pypi.org/project/docker-compose/)
* [vue-cli](https://cli.vuejs.org/guide/installation.html)
* [django](https://pypi.org/project/Django/)

## Installation
1. Copy-paste desired environment ie (development.yml, production.yml) to "docker-compose.yml".
2. Edit created "docker-compose.yml" environment variables.
3. Run the application. Check logs to determine application is now running.
4. Open "http://localhost/" in browser.

### Running the application
```
docker-compose up -d
```

### Stopping the application
```
docker-compose down
```

### Checking the logs
```
docker-compose logs -f
```

### Building new libraries (changes in requirements.txt)
```
docker-compose up -d --build
```

## Notes
1. No need to re-build if there are changes in package.json
2. Both frontend and backend frameworks are running in hot-deployment mode - meaning all changes done in the code will reflect in the build. However, there are cases that you need to restart the application to reflect. If not applied, check the application logs.
