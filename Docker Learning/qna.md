# Questions


### 1. **Does a Docker container require manual installation of Linux, or is it included when using a Python base image?**

**Answer:**
No, you don't need to install Linux manually. The Python base image (e.g., `python:3.11-slim`) is already built on top of a lightweight Linux distribution (like Debian or Alpine), so a minimal Linux environment is already included.

---

### 2. **Should I containerize my FastAPI app using a Dockerfile before moving on to Docker Compose?**

**Answer:**
Yes, it’s a good practice to first containerize your FastAPI app using a single Dockerfile. This helps you understand the build and run process clearly before managing multiple services (like databases) using Docker Compose.

---

### 3. **Is it necessary to install PostgreSQL locally if I plan to use it within a Docker container by passing its connection URL?**

**Answer:**
No, it's not necessary to install PostgreSQL locally. If you're using Docker (with or without Compose), you can run PostgreSQL inside a container and connect to it using the appropriate `DATABASE_URL`. Docker handles network communication between containers internally.

---

### 4. **Does the PostgreSQL database data persist after rebuilding the Docker container, or is a new instance created every time?**

**Answer:**
If you use Docker volumes (e.g., `pgdata:/var/lib/postgresql/data`), the data will persist even after rebuilding the container. Without a volume, the data is stored inside the container and will be lost when the container is removed.

---
