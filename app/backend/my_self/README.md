# FastAPI Authentication System

## A complete FastAPI authentication system with:

User Signup with OTP verification
Login with JWT Authentication
Protected Routes
Forgot Password using OTP
Password Reset
MongoDB Integration
Role-based User Model
Project Structure

MY_SELF/
│
├── app/
│   └── utils.py
│
├── db/
│   ├── database.py
│   └── db_helper.py
│
├── endpoints/
│   └── user.py
│
├── models/
│   └── models.py
│
├── router/
│   └── api.py
│
├── .env
├── requirements.txt
└── my_env/
Features
Authentication Features
User Registration
OTP Verification via Email
JWT Token Authentication
Secure Password Hashing using bcrypt
Protected APIs using JWT
Forgot Password
Reset Password using OTP
Technologies Used
FastAPI
MongoDB
JWT (python-jose)
Passlib + bcrypt
Pydantic
SMTP Email Service
Uvicorn
Installation
1. Clone the Repository
git clone <your_repo_url>
cd MY_SELF
2. Create Virtual Environment
python -m venv my_env

Activate virtual environment:

Windows
my_env\Scripts\activate
Linux/Mac
source my_env/bin/activate
3. Install Requirements
pip install -r requirements.txt
requirements.txt
fastapi
pydantic
uvicorn
email-validator
pymongo
pymongo[srv]==3.12
passlib
bcrypt==4.0.1
passlib[bcrypt]
python-jose[cryptography]
Environment Variables

Create a .env file in the root directory.

SECRET_KEY=your_secret_key
ALGORITHM=HS256
MONGO_URL=your_mongodb_connection_url

SENDER_MAIL=your_email@gmail.com
SENDER_PASSWORD=your_email_app_password
Running the Application
uvicorn router.api:app --reload

Server will run at:

http://127.0.0.1:8000

Swagger Documentation:

http://127.0.0.1:8000/docs
API Endpoints
1. Signup
Endpoint
POST /signup
Request Body
{
  "email": "user@gmail.com",
  "username": "kireeti",
  "password": "password123",
  "confirm_password": "password123",
  "role": "RFP Writer"
}
Response
{
  "message": "OTP sent successfully"
}
2. Signup OTP Verification
Endpoint
POST /signup_validation
Request Body
{
  "email": "user@gmail.com",
  "otp": "123456"
}
Response
{
  "message": "Signup Successful"
}
3. Login
Endpoint
POST /login
Form Data
Key	Value
username	user@gmail.com
password	password123
Response
{
  "message": "Login successful",
  "access_token": "jwt_token",
  "token_type": "bearer"
}
JWT Authentication

After login, copy the access token.

Click the Authorize button in Swagger UI.

Enter token like this:

Bearer your_jwt_token
4. Protected Route
Endpoint
GET /user/me
Response
{
  "message": "Welcome to dashboard",
  "user_email": "user@gmail.com"
}
5. Forgot Password
Endpoint
POST /forgot_password
Request Body
{
  "email": "user@gmail.com",
  "reset_password": "newpassword123",
  "confirm_password": "newpassword123"
}
Response
{
  "message": "RESET OTP SENT SUCESSFULLY"
}
6. Reset Password Validation
Endpoint
POST /reset_validation
Request Body
{
  "otp": "123456"
}
Response
{
  "message": "Password updated successfully"
}
Password Security

Passwords are hashed using:

bcrypt

Hashing handled inside:

app/utils.py
JWT Authentication Flow
User logs in
JWT token generated
Token returned to user
User sends token in Authorization header
Protected routes validate token
MongoDB Collections

Database:

users_db

Collections:

signup_users
login_users
Roles Supported
RFP Writer
Executive Person
Important Notes
Use Gmail App Password for SMTP authentication
Never expose .env file publicly
Store JWT secret securely
OTPs are temporarily stored in memory using Python dictionaries
Future Improvements
OTP Expiry Time
Refresh Tokens
Role-based Authorization
Email Templates
Redis for OTP Storage
Async MongoDB using Motor
Logging System
Author

Developed using FastAPI + MongoDB Authentication System.