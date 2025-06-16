
# Docker Commands:

## Docker Build:

``` bash
docker build -t fastapi-docker-app .
```

## Docker Run:

``` bash
docker run -d -p 8000:8000 --name fastapi-app fastapi-docker-app

```

### Run command for attached mode (show logs live), just omit the `-d`:
```bash

docker run -p 8000:8000 --name fastapi-app fastapi-docker-app

```

**This command is like saying:**

> “Start my `fastapi-docker-app` image in the background, give it a name `fastapi-app`, and let me access it via my browser on port 8000.”

---

### Explanation of Each Part:

| Part           | Meaning                                                                            |
| -------------- | ---------------------------------------------------------------------------------- |
| `docker run`   | Command to **create and start a new container** from an image                      |
| `-d`           | **Detached mode**: Run the container in the background (won’t block your terminal) |
| `-p 8000:8000` | **Port mapping**:                                                                  |

* First `8000` = host port
* Second `8000` = container port
* This means: “Expose container’s port 8000 on localhost:8000” |
  \| `--name fastapi-app` | Give the container a **name** so you can reference it easily (instead of using its auto-generated ID) |
  \| `fastapi-docker-app` | The **image name** to run (this should match what you used in `docker build -t ...`) |

---

###  What happens under the hood?

Docker:

1. Creates a new container from the `fastapi-docker-app` image
2. Assigns it the name `fastapi-app`
3. Maps the container's port `8000` to your machine's port `8000`
4. Starts the container in the background (detached)
5. Your FastAPI app listens on `0.0.0.0:8000` inside the container and is accessible at
    [`http://localhost:8000`](http://localhost:8000)

---

##  Useful Follow-up Commands:

| Command                            | Purpose                                     |
| ---------------------------------- | ------------------------------------------- |
| `docker ps`                        | See your running container                  |
| `docker logs fastapi-app`          | Check its logs/output                       |
| `docker stop fastapi-app`          | Stop the container                          |
| `docker rm fastapi-app`            | Remove the container                        |
| `docker exec -it fastapi-app bash` | Access the container’s shell (if installed) |

---


