# Seven-Sidekicks-Project

## Running the docker-compose file
### Linux
Setting the user inside the container to fix any potential permission problems.

```CURRENT_UID=$(id -u):$(id -g) docker-compose up -d```


### Windows

```docker-compose up -d```

## Getting bash access in a container

```docker-compose exec CONTAINER_NAME bash```