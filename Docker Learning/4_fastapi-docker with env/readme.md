###  Environment Variables & Secrets Management in Docker + FastAPI

---

# ⚙️ Environment Variables & Secrets Management — Docker + FastAPI

This guide explains best practices for managing environment variables and secrets securely in a Dockerized FastAPI project, with updated support for Pydantic v2.

---

## ✅ Key Improvements Over Traditional Setup

* Environment variables are now managed using a `.env` file instead of being hardcoded.
* FastAPI uses `pydantic-settings` to load settings from the environment (required in Pydantic v2).
* All sensitive values like database credentials and secret keys are centralized in the `.env` file.
* Configuration is now externalized from code and Compose, improving reusability and security.

---

## 📁 Using `.env` with `docker-compose.yml`

* The `.env` file contains all required environment variables for both the `web` (FastAPI) and `db` (PostgreSQL) services.
* In `docker-compose.yml`, the `env_file:` directive is used to inject these variables into each service.
* This ensures consistency across environments and keeps sensitive values out of the version-controlled YAML files.

---

## 🔐 Secrets & Safety

* The `.env` file should never be committed to source control. Always include it in your `.gitignore`.
* This approach makes it easier to manage different configurations for development, testing, and production by simply switching the `.env` file.

