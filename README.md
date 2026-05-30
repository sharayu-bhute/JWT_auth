JWT Authentication API
A production-ready JWT authentication system built with FastAPI and PostgreSQL, featuring real-world security mechanisms beyond basic login/logout.

Features

JWT Access + Refresh Token flow
Token Blacklisting — revokes tokens on logout
Bcrypt + SHA256 password hashing
Account Lockout — locks after 5 failed login attempts
IP-based Rate Limiting — blocks after 5 requests/minute
Role-based Access Control — user and admin roles
CORS configured for frontend integration
Demo UI — vanilla HTML/CSS/JS frontend to test all endpoints


Tech Stack
LayerTechnology
Framework | FastAPI | Database - Postgre | SQLORM - SQLAlchemy Auth |Python-Jose (JWT) | Hashing Passlib (bcrypt) | Server Uvicorn Env Python-dotenv
 
Project Structure
JWT_auth/
├── app/
│   ├── core/
│   │   ├── config.py         # Env variables
│   │   ├── database.py       # DB connection
│   │   ├── deps.py           # Auth dependencies
│   │   ├── jwt.py            # Token creation
│   │   ├── rate_limiter.py   # IP rate limiting
│   │   ├── security.py       # Password hashing
│   │   └── token_blacklist.py # Blacklist store
│   ├── models/
│   │   └── user.py           # User DB model
│   ├── routes/
│   │   └── user_routes.py    # All endpoints
│   ├── schemas/
│   │   └── user.py           # Pydantic schemas
│   ├── services/
│   │   ├── auth_service.py   # Login logic
│   │   └── user_service.py   # Signup logic
│   └── main.py               # App entry point
├── frontend/
│   └── AuthDemo.html         # Demo UI
├── .env.example
├── requirements.txt
└── README.md

Setup & Installation
1. Clone the repository
bashgit clone https://github.com/yourusername/JWT_auth.git
cd JWT_auth
2. Create a virtual environment
bashpython -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
3. Install dependencies
bashpip install -r requirements.txt
4. Configure environment variables
Create a .env file in the root directory:
envDATABASE_URL=postgresql://user:password@localhost:5432/auth_db
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
5. Set up PostgreSQL
Create the database:
sqlCREATE DATABASE auth_db;
Tables are created automatically on first run via SQLAlchemy.
6. Run the server
bashuvicorn app.main:app --reload
Server runs at http://127.0.0.1:8000

API Endpoints
MethodEndpointDescriptionAuth RequiredPOST/signupRegister a new user❌POST/loginLogin and get tokens❌GET/protectedAccess protected route✅GET/adminAdmin only route✅ AdminPOST/refreshGet new access token❌POST/logoutRevoke access token✅

Security Details
Password Hashing
Passwords are double-hashed — SHA256 first, then bcrypt — for extra security.
Token Blacklisting
On logout, the access token is added to an in-memory blacklist. Any subsequent request with that token returns 401 Token revoked.
Account Lockout
After 5 consecutive failed login attempts, the account is locked and returns 403 Account is locked.
Rate Limiting
Each IP is limited to 5 login requests per minute. Exceeding this returns 429 Too Many Requests.

Demo UI
Open frontend/AuthDemo.html directly in your browser. No setup needed.
It lets you test the full auth flow:
Signup → Login → Protected → Rate Limit → Account Lockout → Logout → Token Revoked

 
Environment Variables
VariableDescriptionExampleDATABASE_URLPostgreSQL connection stringpostgresql://user:pass@localhost/dbSECRET_KEYJWT signing key (keep secret!)a3f8b2c1...ALGORITHMJWT algorithmHS256ACCESS_TOKEN_EXPIRE_MINUTESToken expiry in minutes30

Future Improvements
 Persistent token blacklist using Redis
 Email verification on signup
 Password reset flow
 Refresh token rotation
 Docker Compose setup


Author
Sharayu bhute

LinkedIn : https://www.linkedin.com/in/sharayu-bhute/
