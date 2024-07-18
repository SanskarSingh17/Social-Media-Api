# Social Networking API
## Overview
This project implements a RESTful API for a social networking application using Django REST Framework. It includes user authentication, friend requests, and user search functionalities.

### Technologies Used
- Django
- Django REST Framework
- MySQL
- Docker

### Prerequisites
- **Before you begin, ensure you have installed the following:**

Docker
Docker Compose

1.Installation
Clone the repository:

git clone https://github.com/SanskarSingh17/Social-media-API
cd social-network-api

2.Set up environment variables:

Create a .env file in the project root and define the following variables:

# .env file
DJANGO_SECRET_KEY=<your_secret_key>
MYSQL_DATABASE=social_network_db
MYSQL_USER=social_user
MYSQL_PASSWORD=social_password
MYSQL_ROOT_PASSWORD=root_password


3.Build and run the application with Docker:
docker-compose up --build

MySQL Credentials
MySQL Database: social_network_db
MySQL User: social_user
MySQL Password: social_password
MySQL Root Password: root_password



API Endpoints
POST /api/signup/: User signup
POST /api/login/: User login
GET /api/search/?query=<query>: Search users by email or name
POST /api/friend-requests/: Send friend request
PATCH /api/friend-requests/<id>/: Accept/reject friend request
GET /api/friends/: List friends
GET /api/pending-requests/: List pending friend requests

Postman Collection
For easy testing, import the provided Postman collection that includes requests for each API endpoint. You can find the collection JSON file in the postman/ directory.

Docker Compose
The docker-compose.yml file defines two services:

db: MySQL database container.
web: Django application container.
Ensure Docker is running and ports 8000 (Django app) and 3307 (MySQL) are available.
