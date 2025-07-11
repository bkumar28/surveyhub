# 📊 Overview

**surveyhub** is a Django-based Survey Management System designed to let organizations or individuals create, distribute, and analyze surveys with ease. It provides a robust backend, API support, and is ready for production deployment with Docker.

---
## 🚀 Key Features Explained

 - **Create surveys with customizable questions:**
Users can build surveys with a variety of question types (text, choice, rating, etc.), set required/optional fields, and order questions as needed.

 - **Manage survey lifecycle (draft, submitted, expired):**
Surveys can be saved as drafts, published for responses, paused, or marked as expired/completed. This allows for flexible management and scheduling.

 - **Collect responses from users (invited or anonymous):**
Surveys can be distributed via invitations (email, token) or made public for anyone to respond. Both authenticated and anonymous responses are supported.

 - **Generate reports with popular/unpopular answers:**
The system aggregates responses and provides analytics, such as most/least common answers, completion rates, and other insights to help you understand your data.

 - **Swagger API documentation:**
All API endpoints are documented and browsable via Swagger UI (/swagger/), making it easy for developers to integrate or test the system.

 - **Admin access:**
Django’s admin interface is available for managing surveys, questions, responses, and users.

 - **Dynamic question handling:**
Supports advanced question logic, such as conditional questions (show/hide based on previous answers), and a variety of field types.

 - **Dockerized deployment:**
The project includes Docker and Docker Compose support for easy setup, scaling, and deployment in any environment.

 - **Automated setup scripts:**
Scripts are provided to install dependencies, set up the database, and load sample data, making onboarding and development fast and reliable.
---

## 🛠️ Getting Started

1. **Clone the project repository:**
   ```bash
   git clone https://github.com/Bkumar28/surveyhub.git
   cd surveyhub/
   ```

2. **Choose your Python environment:**
   - Recommended: Python 3.8

   **Option A: Poetry (default, recommended)**
   - No need to manually create or activate a virtual environment; Poetry handles it for you.
   - All dependencies and migrations will be handled by the setup script.

   **Option B: Virtualenv + requirements.txt**
   - If you prefer a classic virtual environment:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Run the project setup script:**
   - To use Poetry (default):
     ```bash
     ./scripts/pre_requisites.sh --with-sample-data
     ```
   - To use virtualenv + requirements.txt:
     ```bash
     ./scripts/pre_requisites.sh --use-venv --with-sample-data
     ```
   - To only load user data (skip sample data):
     ```bash
     ./scripts/pre_requisites.sh --use-venv --users-only
     ```

4. **Access the API documentation:**
   Open your browser at:
   ```
   http://127.0.0.1:8000/swagger/
   ```
---

## 🐳 Docker Quickstart

To build and run the project using Docker:

- **Build the Docker images:**
  ```bash
  docker-compose build
  ```
- **Start the containers:**
  ```bash
  docker-compose up -d
  ```
- **Stop and remove containers, networks, and volumes:**
  ```bash
  docker-compose down
  ```

---

## 👨‍💻 Maintainer

**Bharat Kumar**
_Senior Software Engineer | Cloud & Backend Systems_
📧 kumar.bhart28@gmail.com
🔗 [LinkedIn](https://www.linkedin.com/in/bharat-kumar28)
