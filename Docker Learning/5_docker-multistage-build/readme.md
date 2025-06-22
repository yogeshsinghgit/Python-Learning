# **Multi-stage Docker Builds** : 
This technique helps you create smaller, cleaner Docker images optimized for production by separating build-time and runtime dependencies.

---

## Why Multi-stage Builds?

* Avoid including build tools, caches, or unnecessary packages in the final image.
* Reduce image size drastically.
* Speed up build and deployment times.
* Improve security by minimizing surface area.

---

## Basic Concept

You write multiple `FROM` stages in a single Dockerfile:

* **Builder stage:** Installs everything needed to build/install dependencies.
* **Final stage:** Starts from a minimal base (like `python:slim`), copies only necessary artifacts from the builder stage.

---

## How to do it (overview)

1. **Builder stage:**

* Use a full Python image (`python:3.11-slim` or similar).
* Copy your source code and install all dependencies (including build dependencies).
* Compile or prepare anything your app needs.

2. **Final stage:**

* Start with a minimal image (`python:3.11-slim` or `alpine`).
* Copy just the installed packages and your app from the builder stage.
* Set up your runtime command (`uvicorn` for FastAPI).

---

## Benefits for FastAPI

* No need to ship development dependencies or build tools inside your runtime container.
* Smaller images lead to faster startup and less bandwidth consumption.
* Easier to maintain production-ready images.
