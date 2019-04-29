# Seven-Sidekicks-Project

## Running the docker-compose file
### Linux
Setting the user inside the container to fix any potential permission problems.

```CURRENT_UID=$(id -u):$(id -g) docker-compose up -d```


### Windows

Build docker: ```docker-compose build```

Setup containers: ```docker-compose up -d```

Remove containers: ```docker-compose down```

See which containers are currently running: ```docker-compose ps```

## Getting bash access in a container

```docker-compose exec CONTAINER_NAME bash```
