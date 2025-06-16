

# Docker Commands:

## File Structure:
```
docker-basic/
│
├── app.py
├── requirements.txt
└── Dockerfile

```

## Build Image:

```
docker build -t python-hello .
```

## Run Container:

```
docker run python-hello
```

## Clean Up:
```
docker ps -a         # find container ID
docker rm <id>       # remove it
docker images        # list images
docker rmi <image>   # remove unused images
```
