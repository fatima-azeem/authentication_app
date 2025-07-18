# API Integration Testing & Setup Guide

## 🚀 Quick Start - Testing the Integration

### 1. Backend Setup (Terminal 1)

```bash
# Navigate to backend directory
cd /Users/fatima/Development/projects/authentication_app

# Create .env file with your configuration
cat > .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://user:password@localhost/authdb
BACKEND_API_KEY=test_api_key_12345
RESEND_API_KEY=your_resend_api_key_here
RESEND_FROM_EMAIL=noreply@yourapp.com
JWT_ACCESS_TOKEN_SECRET=your_very_secure_jwt_access_secret_here
JWT_REFRESH_TOKEN_SECRET=your_very_secure_jwt_refresh_secret_here
JWT_ACCESS_TOKEN_EXPIRATION=30m
JWT_REFRESH_TOKEN_EXPIRATION=7d
EOF

# Install dependencies (if using uv)
uv sync

# Or if using pip
# pip install -r requirements.txt

# Run database migrations
alembic upgrade head

# Start the FastAPI server
uvicorn app.main:app --reload --port 8000 --host 0.0.0.0
```

### 2. Flutter Setup (Terminal 2)

```bash
# Navigate to Flutter directory
cd /Users/fatima/projects/flutter_projects/auth_ui

# Update API configuration
# Edit lib/core/api/api_config.dart and update:
# - baseUrl to match your backend URL
# - apiKey to match your BACKEND_API_KEY from .env
```

Update `lib/core/api/api_config.dart`:
```dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000';  // or your backend URL
  static const String apiKey = 'test_api_key_12345';      // Match your .env BACKEND_API_KEY
  
  // Rest of the configuration...
}
```

```bash
# Get Flutter dependencies
flutter pub get

# Run the Flutter app
flutter run
```

## 🧪 API Testing with cURL

### Test Backend Endpoints

#### 1. Test Registration
```bash
curl -X POST "http://localhost:8000/api/v1/register" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test_api_key_12345" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "TestPassword123!",
    "confirm_password": "TestPassword123!",
    "is_term_accepted": true
  }'
```

Expected Response:
```json
{
  "message": "User registered successfully. Please verify your email.",
  "user_id": "cm...",
  "email": "test@example.com",
  "verification_required": true
}
```

#### 2. Test OTP Verification
```bash
curl -X POST "http://localhost:8000/api/v1/verify-otp" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test_api_key_12345" \
  -d '{
    "email": "test@example.com",
    "otp": "123456"
  }'
```

#### 3. Test Login
```bash
curl -X POST "http://localhost:8000/api/v1/login" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "TestPassword123!",
    "device_id": "test_device"
  }'
```

#### 4. Test Password Reset Request
```bash
curl -X POST "http://localhost:8000/api/v1/request-password-reset" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: test_api_key_12345" \
  -d '{
    "email": "test@example.com"
  }'
```

## 📱 Flutter Integration Testing

### Step 1: Update Dependencies

Add these to your `pubspec.yaml` if not already present:

```yaml
dependencies:
  # ... existing dependencies
  dio: ^5.8.0+1
  pretty_dio_logger: ^1.4.0
  flutter_secure_storage: ^9.2.4
  provider: ^6.1.1

dev_dependencies:
  # ... existing dev dependencies
  integration_test:
    sdk: flutter
```

### Step 2: Initialize the App with Provider

Your `main.dart` should look like this:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:auth_ui/core/api/dio_client.dart';
import 'package:auth_ui/shared/providers/auth_provider.dart';
import 'package:auth_ui/features/splash/splash_screen.dart';
import 'package:auth_ui/theme/app_theme.dart';

void main() {
  // Initialize Dio client
  DioClient.init();
  
  runApp(const MyApp());
}

class MyApp extends StatefulWidget {
  const MyApp({super.key});

  @override
  State<MyApp> createState() => _MyAppState();
}

class _MyAppState extends State<MyApp> {
  bool isDarkMode = false;

  void toggleTheme() {
    setState(() {
      isDarkMode = !isDarkMode;
    });
  }

  @override
  Widget build(BuildContext context) {
    return ChangeNotifierProvider(
      create: (context) => AuthProvider()..init(),
      child: MaterialApp(
        debugShowCheckedModeBanner: false,
        title: 'AuthUI - Modern Authentication',
        themeMode: isDarkMode ? ThemeMode.dark : ThemeMode.light,
        darkTheme: AppTheme.dark,
        theme: AppTheme.light,
        home: const SplashScreen(),
      ),
    );
  }
}
```

### Step 3: Test Flow

1. **Registration Flow:**
   - Open the app
   - Navigate to Register screen
   - Fill in the form with valid data
   - Submit registration
   - Navigate to email verification
   - Enter OTP "123456" (hardcoded for demo)
   - Should succeed and navigate to login

2. **Login Flow:**
   - Use the registered email
   - Use the password you set during registration
   - Should authenticate and navigate to home screen

3. **Password Reset Flow:**
   - From login screen, tap "Forgot password?"
   - Enter your email
   - For demo, you can proceed directly to reset password screen
   - Set new password
   - Should navigate back to login

## 🔧 Troubleshooting

### Common Issues & Solutions

#### 1. CORS Error
If you get CORS errors, add this to your FastAPI `main.py`:

```python
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your Flutter app domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### 2. API Key Mismatch
Ensure the API key in Flutter matches your backend `.env`:
- Backend: `BACKEND_API_KEY=test_api_key_12345`
- Flutter: `static const String apiKey = 'test_api_key_12345';`

#### 3. Database Connection
If you get database errors:
```bash
# Create a PostgreSQL database
createdb authdb

# Or use SQLite for testing (update DATABASE_URL in .env)
DATABASE_URL=sqlite+aiosqlite:///./test.db
```

#### 4. Network Connection Issues
For iOS Simulator / Android Emulator:
- Use `http://10.0.2.2:8000` for Android Emulator
- Use `http://127.0.0.1:8000` for iOS Simulator
- Update `baseUrl` in `api_config.dart` accordingly

#### 5. SSL Certificate Issues (Development)
If using HTTPS in development, you might need to disable SSL verification:

```dart
// Only for development - NEVER in production
(_dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate = (client) {
  client.badCertificateCallback = (cert, host, port) => true;
  return client;
};
```

## 📊 API Response Status Codes

| Status Code | Meaning | Action |
|-------------|---------|---------|
| 200 | Success | Continue with flow |
| 201 | Created | Registration successful |
| 204 | No Content | Password reset email sent |
| 400 | Bad Request | Show error message to user |
| 401 | Unauthorized | Redirect to login |
| 403 | Forbidden | Show access denied message |
| 404 | Not Found | User not found |
| 422 | Validation Error | Show field-specific errors |
| 500 | Server Error | Show generic error message |

## 🔐 Security Considerations

### Production Checklist

1. **Environment Variables:**
   - Use strong, unique JWT secrets
   - Never commit API keys
   - Use environment-specific configurations

2. **HTTPS:**
   - Always use HTTPS in production
   - Implement certificate pinning in Flutter

3. **Token Management:**
   - Implement proper token refresh logic
   - Clear tokens on app uninstall
   - Use secure storage for sensitive data

4. **API Rate Limiting:**
   - Implement rate limiting on backend
   - Handle rate limit responses in Flutter

5. **Input Validation:**
   - Validate all inputs on both client and server
   - Sanitize user inputs
   - Use parameterized queries

## 🚀 Next Steps

### Enhancements to Implement

1. **Biometric Authentication:**
   ```dart
   // Use the local_auth package already in dependencies
   final bool didAuthenticate = await auth.authenticate(
     localizedReason: 'Please authenticate to access your account',
   );
   ```

2. **Offline Support:**
   - Implement local database with sqflite
   - Cache user data and sync when online
   - Handle network connectivity changes

3. **Push Notifications:**
   - Integrate Firebase Cloud Messaging
   - Send verification codes via push

4. **Social Authentication:**
   - Add Google/Apple/Facebook login
   - Implement OAuth flows

5. **Enhanced Security:**
   - Implement device fingerprinting
   - Add suspicious activity detection
   - Implement account lockout policies

This comprehensive setup should get your Flutter frontend successfully communicating with your FastAPI backend!
