<img align="left" height="60" src="golae.png" alt="Golae">

# GOLAE

Get user agent and IP from a visitor to your redirection website

## Steps

1. Download this repository:

```commandline
git clone https://github.com/drkrysSrng/golae.git
```
3. Launch docker-compose.yml file to create container and lanunch the server:

```commandline
docker compose up -d
```

## Creating the image manually

1. Create the docker image using:

```commandline
cd nyu/
docker build --tag golae:1.0 .
docker save golae:1.0 | gzip > golae_1.0.tar.gz
```

2. Load in the destination server:

```commandline
docker load < nyu_1.0.tar.gz

```

4. Launch the docker-compose directly but, comment the build part:

```commandline
docker-compose up -d
```

## Docker-compose

* The **PUBLIC_IP** must your public IP or your server's to check you are outside or NOT.

```yml
version: '3.3'
services:
  web:
    build: # This part only if you don't want to build the image by yourself
      context: .
      dockerfile: Dockerfile
    image: golae
    container_name: golae
    restart: always
    #depends_on:
    #  - other
    ports:
      - 80:80

```

## Other Commands

* Stop the container from the docker-compose.yml file
```commandline
docker compose down
```

* Stop and remove the container manually:

```commandline
docker stop golae
docker rm golae
```
* Remove the image
```
docker rmi golae:latest
```

* Remove all the broken images
```
docker image prune
```



