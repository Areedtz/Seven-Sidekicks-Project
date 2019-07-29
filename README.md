**WIP**

# Seven-Sidekicks-Project

This repo, in short, is about tagging emotions to songs, using both audio and video input, and finding similar sounding songs. Head on over to our [wiki](https://github.com/nsst19/Seven-Sidekicks-Project/wiki) if you want to read more about the project!

We have a super simple installation guide down below that will show you how to setup the project locally.

## Installation Guide

### Running the docker-compose file
Build docker: ```docker-compose build```

Setup containers: ```docker-compose up -d```

Stop and remove containers: ```docker-compose down```

See which containers are currently running: ```docker-compose ps```

### Linux specific
Setting the user inside the container to fix any potential permission problems.

```CURRENT_UID=$(id -u):$(id -g) docker-compose up -d```


### Getting bash access in a container

```docker-compose exec CONTAINER_NAME bash```

### Accessing the API to send requests
If everything goes smoothly, the API should be accessible on the following URL:<br>
```localhost:80```

### Common Errors
#### Containers keep restarting with database creation error
This error occurs if a fresh pull of the source code is run locally on a machine that has run the source code before. In the root folder we have a file called "__main__.py" which has a line that needs to be commented out: "db.setup()"
