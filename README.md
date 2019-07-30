---------- * **WIP** * ----------

# Seven-Sidekicks-Project

This repo, in short, is about tagging emotions to songs, using both audio and video input, and finding similar sounding songs. Head on over to our [wiki](https://github.com/nsst19/Seven-Sidekicks-Project/wiki) if you want to read more about the project!

We have a super simple installation guide down below that will show you how to setup the project locally.

## Installation Guide

### Running the docker-compose file
Build docker: ```docker-compose build```

When creating the database locally, there is a bug with creating a database that already exists. This is the current work around:

First setup of containers: ```docker-compose up -d```

Edit main file: <br>
- Go into "/src/\_\_main\_\_.py"
- Find the these two lines and comment them out:
  - ```db = AudioDB()``` --> ```#db = AudioDB()```
  - ```db.setup()``` --> ```#db.setup()```

Final setup of containers: ```docker-compose down && docker-compose up -d```


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
