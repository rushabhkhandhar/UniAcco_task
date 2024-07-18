# Auth Project

This project is a Django-based user authentication system using email and One-Time Password (OTP). The application is Dockerized to ensure a consistent development and deployment environment.

## Features

1. **Email Registration**:
   - Endpoint to register a new user with an email address.
   - Validates email format and checks for duplicates.

2. **OTP Generation and Sending**:
   - Endpoint to request an OTP.
   - Generates a secure OTP.
   - Sends the OTP to the user's registered email address.

3. **OTP Verification**:
   - Endpoint to verify the OTP.
   - Authenticates the user if the OTP is valid and within the time limit.

4. **Session Management**:
   - Generates and manages user sessions upon successful OTP verification.
   - Provides secure session tokens for authenticated users.

5. **Security Measures**:
   - Implements rate limiting on OTP requests to prevent abuse.
   - Uses secure algorithms for OTP generation and hashing.
   - Ensures encrypted communication between client and server.

## Technical Requirements

1. **Backend Framework**: Django
2. **Database**: SQLite
3. **Email Service**: Mock email service for sending OTPs (prints OTP to the console instead of sending an actual email)
4. **Token Management**: JWT (JSON Web Tokens)
5. **Environment Setup**: Docker

## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your system.

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/auth_project.git
    cd auth_project
    ```

2. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

3. Apply database migrations:

    ```bash
    docker-compose exec web python manage.py makemigrations
    docker-compose exec web python manage.py migrate
    ```

### API Endpoints

1. **User Registration**:

    - **URL**: `/api/register/`
    - **Method**: `POST`
    - **Request Body**:
      ```json
      {
          "email": "user@example.com"
      }
      ```
    - **Response**:
      ```json
      {
          "message": "Registration successful. Please verify your email."
      }
      ```

2. **Request OTP**:

    - **URL**: `/api/request-otp/`
    - **Method**: `POST`
    - **Request Body**:
      ```json
      {
          "email": "user@example.com"
      }
      ```
    - **Response**:
      ```json
      {
          "message": "OTP sent to your email."
      }
      ```

3. **Verify OTP**:

    - **URL**: `/api/verify-otp/`
    - **Method**: `POST`
    - **Request Body**:
      ```json
      {
          "email": "user@example.com",
          "otp": "123456"
      }
      ```
    - **Response**:
      ```json
      {
          "message": "Login successful.",
          "token": "jwt_token"
      }
      ```

### Testing

To test the application, you can use Postman or any other API testing tool to send requests to the API endpoints.

1. **User Registration**:
    - Send a `POST` request to `http://localhost:8000/api/register/` with the email in the request body.

2. **Request OTP**:
    - Send a `POST` request to `http://localhost:8000/api/request-otp/` with the email in the request body.

3. **Verify OTP**:
    - Send a `POST` request to `http://localhost:8000/api/verify-otp/` with the email and OTP in the request body.

### Common Issues

1. **OperationalError: no such table**:
    - Ensure you have run the database migrations as described in the installation steps.

2. **Permission Denied while connecting to Docker Daemon**:
    - Run Docker commands with `sudo` or add your user to the Docker group as described in the installation steps.

