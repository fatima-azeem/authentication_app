# 🔐 Authentication App - Backend API

A modern, production-ready authentication API built with FastAPI, SQLAlchemy, PostgreSQL, and JWT. 
This robust backend provides secure user authentication, email verification, password reset functionality, and comprehensive session management.

## ✨ Features

### 🚀 Core Authentication
- **User Registration** with email verification
- **JWT-based Login** with access & refresh tokens
- **Password Reset** with OTP verification
- **Email Verification** via OTP codes
- **Session Management** with device tracking
- **Secure Logout** with token invalidation

### 🛠️ Technical Stack
- **FastAPI** - High-performance async API framework
- **PostgreSQL** - Robust relational database
- **SQLAlchemy** - Modern async ORM
- **Alembic** - Database migration management
- **JWT** - Secure token-based authentication
- **Argon2** - Industry-standard password hashing
- **Resend** - Reliable email service integration
- **Pydantic** - Data validation and settings management

### 🔧 Architecture & Quality
- **Async/Await** - Full asynchronous support
- **Environment Configuration** - Secure `.env` based settings
- **Type Safety** - Complete type hints with Pylance
- **Code Quality** - Linting with Ruff
- **Testing** - Comprehensive API testing suite
- **Database Migrations** - Version-controlled schema changes
- **Modular Design** - Clean separation of concerns

---

## 🏗️ Project Structure

```
authentication_app/
├── app/
│   ├── api/v1/           # API endpoints & routers
│   │   ├── auth/         # Authentication endpoints
│   │   │   ├── auth_router.py          # Login endpoint
│   │   │   ├── logout_router.py        # Logout endpoint
│   │   │   └── password_reset_router.py # Password reset flow
│   │   ├── register/     # User registration
│   │   ├── otp/          # OTP verification
│   │   └── resend/       # Resend OTP codes
│   ├── core/             # Core configuration
│   │   ├── config.py     # Environment settings
│   │   └── security.py   # API key validation
│   ├── db/               # Database layer
│   │   ├── database.py   # Database connection
│   │   ├── models/       # SQLAlchemy models
│   │   └── repositories/ # Data access layer
│   ├── schemas/          # Pydantic models
│   │   ├── login_schema.py
│   │   ├── register_schema.py
│   │   ├── otp_schema.py
│   │   └── password_reset_schema.py
│   ├── services/         # Business logic
│   │   ├── register_service.py
│   │   ├── login_service.py
│   │   ├── otp_service.py
│   │   ├── password_reset_service.py
│   │   └── email_service.py
│   ├── utils/            # Utility functions
│   │   ├── jwt_utils.py  # JWT token handling
│   │   └── otp_generator.py # OTP generation
│   └── main.py           # FastAPI application
├── alembic/              # Database migrations
├── tests/                # Test suite
├── pyproject.toml        # Python dependencies
├── uv.lock              # Dependency lock file
├── testapi.sh           # API testing script
└── README.md            # This file
```

## 🔌 API Endpoints

### Authentication Flow
- `POST /api/v1/register` - User registration
- `POST /api/v1/verify-otp` - Email verification
- `POST /api/v1/login` - User login
- `POST /api/v1/logout` - User logout

### Password Reset Flow
- `POST /api/v1/request-password-reset` - Request reset OTP
- `POST /api/v1/verify-password-reset-otp` - Verify reset OTP
- `POST /api/v1/reset-password` - Reset password with token

### Utility Endpoints
- `POST /api/v1/resend-otp` - Resend verification OTP
- `POST /api/v1/resend-password-reset-otp` - Resend reset OTP

---

## 🚀 Getting Started

### Prerequisites
- **Python 3.11+** (see `.python-version`)
- **PostgreSQL 12+** database
- **UV** or **pip** for dependency management
- **Resend API key** for email services

### 1. Clone the Repository

```bash
git clone https://github.com/fatima-azeem/authentication_app.git
cd authentication_app
```

### 2. Environment Setup

Create a `.env` file in the project root with the following variables:

```env
# Database Configuration
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/authdb

# Email Service (Resend)
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=noreply@yourdomain.com

# JWT Configuration
JWT_ACCESS_TOKEN_SECRET=your_super_secure_access_token_secret
JWT_REFRESH_TOKEN_SECRET=your_super_secure_refresh_token_secret
JWT_ACCESS_TOKEN_EXPIRATION=30m
JWT_REFRESH_TOKEN_EXPIRATION=7d

# API Security
BACKEND_API_KEY=your_api_key_for_client_authentication

# Development
DB_ECHO=false
```

**⚠️ Important**: Never commit your `.env` file to version control!

### 3. Install Dependencies

Using UV (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 4. Database Setup

Run database migrations:
```bash
alembic upgrade head
```

### 5. Start the Development Server

```bash
# Using UV
uv run uvicorn app.main:app --reload --port 8000

# Or directly
uvicorn app.main:app --reload --port 8000
```

The API will be available at:
- **API Documentation**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/

---

## 🧪 Testing

### Automated API Testing

Run the comprehensive test suite:

```bash
# Run the automated test script
chmod +x testapi.sh
./testapi.sh

# Or test with custom data
./testapi.sh user@example.com MyPassword123 "John Doe" true
```

### Manual Testing

#### 1. User Registration
```bash
curl -X POST "http://localhost:8000/api/v1/register" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "full_name": "John Doe",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "is_term_accepted": true
  }'
```

#### 2. Email Verification
```bash
curl -X POST "http://localhost:8000/api/v1/verify-otp" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_api_key_here" \
  -d '{
    "email": "john@example.com",
    "otp": "123456"
  }'
```

#### 3. User Login
```bash
curl -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!",
    "device_id": "web_browser_001"
  }'
```

#### 4. Password Reset
```bash
# Request reset OTP
curl -X POST "http://localhost:8000/api/v1/request-password-reset" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com"
  }'

# Verify reset OTP
curl -X POST "http://localhost:8000/api/v1/verify-password-reset-otp" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "otp": "789012"
  }'

# Reset password
curl -X POST "http://localhost:8000/api/v1/reset-password" \
  -H "Content-Type: application/json" \
  -d '{
    "token": "789012",
    "new_password": "NewSecurePass123!"
  }'
```

---

## 🛠️ Development

### Code Quality

```bash
# Linting and formatting
ruff check .
ruff format .

# Type checking (using Pylance in VS Code)
# Or using mypy
mypy app/
```

### Database Operations

```bash
# Create new migration
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback migration
alembic downgrade -1
```

### Environment Management

```bash
# Using UV (recommended)
uv sync              # Install dependencies
uv add package_name  # Add new dependency
uv run command       # Run commands in environment

# Traditional approach
pip install -e .
pip install package_name
```

---

## 🔒 Security Features

### Authentication & Authorization
- **JWT Tokens**: Secure access and refresh token implementation
- **Password Security**: Argon2 hashing with salt
- **Session Management**: Device tracking and session invalidation
- **API Key Protection**: Endpoints protected with API keys

### Data Protection
- **Email Verification**: Mandatory email verification for new users
- **OTP Security**: Time-limited OTP codes with secure generation
- **Password Reset**: Secure token-based password reset flow
- **Input Validation**: Comprehensive request validation with Pydantic

### Infrastructure Security
- **Environment Variables**: Secure configuration management
- **Database Security**: Parameterized queries prevent SQL injection
- **CORS Configuration**: Proper cross-origin resource sharing
- **Rate Limiting**: Built-in protection against abuse

---

## 📋 Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `DATABASE_URL` | PostgreSQL connection string | - | Yes |
| `RESEND_API_KEY` | Resend service API key | - | Yes |
| `RESEND_FROM_EMAIL` | Sender email address | - | Yes |
| `JWT_ACCESS_TOKEN_SECRET` | JWT access token secret | - | Yes |
| `JWT_REFRESH_TOKEN_SECRET` | JWT refresh token secret | - | Yes |
| `BACKEND_API_KEY` | API key for client authentication | - | Yes |
| `JWT_ACCESS_TOKEN_EXPIRATION` | Access token expiry | 30m | No |
| `JWT_REFRESH_TOKEN_EXPIRATION` | Refresh token expiry | 7d | No |
| `DB_ECHO` | Enable SQL query logging | false | No |

### Database Schema

The application uses the following main tables:
- `user` - User accounts and authentication data
- `otp` - One-time password codes for verification
- `session` - User sessions and device tracking
- `password_reset_token` - Password reset tokens
- `on_boarding` - User onboarding and profile data

---

## 🔧 Deployment

### Production Deployment

1. **Environment Setup**:
   ```bash
   # Set production environment variables
   export DATABASE_URL="postgresql://..."
   export RESEND_API_KEY="..."
   # ... other variables
   ```

2. **Database Migration**:
   ```bash
   alembic upgrade head
   ```

3. **Start Production Server**:
   ```bash
   # Using Gunicorn with Uvicorn workers
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   
   # Or using Uvicorn directly
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Docker Deployment

```dockerfile
# Example Dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

---

## 📚 Documentation

- **API Documentation**: Available at `/docs` when running the server
- **Alternative Documentation**: Available at `/redoc`
- **Database Schema**: Generated automatically by Alembic
- **Code Documentation**: Comprehensive docstrings throughout codebase

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines
- Follow PEP 8 style guidelines
- Write comprehensive tests for new features
- Update documentation for API changes
- Use type hints throughout the codebase

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Fatima Azeem**
- GitHub: [@fatima-azeem](https://github.com/fatima-azeem)
- Email: fatima.azeemuddin@outlook.com

---

## 🙏 Acknowledgments

- **FastAPI** team for the excellent framework
- **SQLAlchemy** for the robust ORM
- **Resend** for reliable email services
- **Alembic** for database migration management

---

## 📝 Changelog

### v1.0.0 (Current)
- Initial release
- Complete authentication system
- Email verification
- Password reset functionality
- Session management
- Comprehensive API documentation

---

## 🐛 Known Issues

- None currently reported

## 🔮 Future Enhancements

- [ ] OAuth2 integration (Google, GitHub)
- [ ] Two-factor authentication (2FA)
- [ ] Rate limiting middleware
- [ ] Redis caching integration
- [ ] Admin dashboard
- [ ] User role management
- [ ] Audit logging

---

*This project is under active development. Contributions and feedback are welcome!*
# this project has been deployed to my home vps server