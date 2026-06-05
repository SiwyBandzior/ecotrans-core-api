# EcoTrans Core API 🚚♻️

A robust, containerized backend REST API built for managing logistics and hazardous materials tracking. Designed with a focus on security, data persistence, and easy deployment.

## 🚀 Tech Stack
* **Framework:** FastAPI (Python 3.11)
* **Database:** PostgreSQL
* **ORM:** SQLAlchemy
* **Security:** JWT (JSON Web Tokens), bcrypt hashing
* **Infrastructure:** Docker & Docker Compose

## ⚡ Features
* **Authentication:** Secure user registration and login endpoints.
* **Role-Based Access:** Core endpoints are locked behind JWT authorization.
* **Data Validation:** Automatic payload validation using Pydantic schemas.
* **Persistent Storage:** Fully integrated PostgreSQL database inside a Docker network.

## 🛠️ How to Run (Local Deployment)
Make sure you have Docker and Docker Desktop installed.

1. Clone the repository
2. Build and spin up the containers:
    docker compose up --build
3. Open your browser and navigate to the interactive Swagger UI:
http://127.0.0.1:8000/docs

🔒 Security Note
To interact with the /tasks/ endpoints, you must first create an account via /register/ and obtain a Bearer token by logging in via the Authorize button.