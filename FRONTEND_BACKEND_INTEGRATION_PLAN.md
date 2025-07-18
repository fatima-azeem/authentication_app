# Frontend-Backend Integration Plan & API Contract

## 🎯 Integration Overview

This document outlines the complete plan to connect the Flutter `auth_ui` frontend with the FastAPI `authentication_app` backend, including API contracts, implementation steps, and best practices.

## 📋 Implementation Plan

### Phase 1: Backend API Setup & Documentation
1. **API Documentation Review**
2. **CORS Configuration**
3. **API Key Management**
4. **Environment Configuration**

### Phase 2: Flutter HTTP Client Setup
1. **Dio HTTP Client Configuration**
2. **API Service Layer Creation**
3. **Token Management Service**
4. **Error Handling & Interceptors**

### Phase 3: Authentication Integration
1. **Login/Registration Flows**
2. **JWT Token Storage**
3. **OTP Verification**
4. **Password Reset**

### Phase 4: State Management & Security
1. **Authentication State Management**
2. **Secure Storage Implementation**
3. **Automatic Token Refresh**
4. **Biometric Authentication**

## 🔌 API Contract Documentation

### Base Configuration

#### Backend Base URL
```
Development: http://localhost:8000
Production: https://your-api-domain.com
```

#### Authentication Headers
```http
Content-Type: application/json
X-API-Key: your_backend_api_key
Authorization: Bearer {jwt_access_token}  # For protected endpoints
```

---

## 📡 API Endpoints Contract

### 1. User Registration

#### Endpoint
```http
POST /api/v1/register
```

#### Headers
```http
Content-Type: application/json
X-API-Key: your_backend_api_key
```

#### Request Body
```json
{
  "full_name": "John Doe",
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "confirm_password": "SecurePassword123!",
  "is_term_accepted": true
}
```

#### Response (201 Created)
```json
{
  "message": "User registered successfully. Please verify your email.",
  "user_id": "cm123456789",
  "email": "john.doe@example.com",
  "verification_required": true
}
```

#### Error Responses
```json
// 400 Bad Request - Email already exists
{
  "detail": "Email already registered"
}

// 400 Bad Request - Terms not accepted
{
  "detail": "Terms and Conditions must be accepted"
}

// 422 Validation Error
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

### 2. Email Verification (OTP)

#### Endpoint
```http
POST /api/v1/verify-otp
```

#### Headers
```http
Content-Type: application/json
X-API-Key: your_backend_api_key
```

#### Request Body
```json
{
  "email": "john.doe@example.com",
  "otp": "123456"
}
```

#### Response (200 OK)
```json
{
  "message": "Email verified successfully",
  "verified": true,
  "user_id": "cm123456789"
}
```

#### Error Responses
```json
// 404 Not Found
{
  "detail": "User not found"
}

// 400 Bad Request
{
  "detail": "Invalid OTP"
}
```

---

### 3. User Login

#### Endpoint
```http
POST /api/v1/login
```

#### Headers
```http
Content-Type: application/json
```

#### Request Body
```json
{
  "email": "john.doe@example.com",
  "password": "SecurePassword123!",
  "device_id": "flutter_app_device_123"  // Optional
}
```

#### Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800,  // 30 minutes in seconds
  "user": {
    "id": "cm123456789",
    "email": "john.doe@example.com",
    "role": "USER",
    "is_email_verified": true
  }
}
```

#### Error Responses
```json
// 401 Unauthorized
{
  "detail": "Invalid credentials"
}

// 403 Forbidden - Email not verified
{
  "detail": "Email not verified. Please verify your email first."
}
```

---

### 4. Password Reset Request

#### Endpoint
```http
POST /api/v1/request-password-reset
```

#### Headers
```http
Content-Type: application/json
X-API-Key: your_backend_api_key
```

#### Request Body
```json
{
  "email": "john.doe@example.com"
}
```

#### Response (204 No Content)
```
No content returned, but reset email is sent if user exists
```

---

### 5. Password Reset

#### Endpoint
```http
POST /api/v1/reset-password
```

#### Headers
```http
Content-Type: application/json
X-API-Key: your_backend_api_key
```

#### Request Body
```json
{
  "token": "reset_token_from_email",
  "new_password": "NewSecurePassword123!"
}
```

#### Response (200 OK)
```json
{
  "message": "Password reset successful."
}
```

#### Error Responses
```json
// 400 Bad Request
{
  "message": "Password must be at least 8 characters."
}

// 400 Bad Request - Invalid token
{
  "detail": "Invalid or expired reset token"
}
```

---

### 6. Token Refresh

#### Endpoint
```http
POST /api/v1/refresh-token
```

#### Headers
```http
Content-Type: application/json
Cookie: refresh_token=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

#### Response (200 OK)
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 1800
}
```

---

### 7. Logout

#### Endpoint
```http
POST /api/v1/logout
```

#### Headers
```http
Content-Type: application/json
Authorization: Bearer {access_token}
```

#### Response (200 OK)
```json
{
  "message": "Successfully logged out"
}
```

---

## 🛠️ Flutter Implementation Steps

### Step 1: Create API Service Layer

Create the following files in your Flutter project:

#### 1.1 API Configuration
```dart
// lib/core/api/api_config.dart
class ApiConfig {
  static const String baseUrl = 'http://localhost:8000';  // Development
  static const String apiKey = 'your_backend_api_key';
  
  // API Endpoints
  static const String register = '/api/v1/register';
  static const String verifyOtp = '/api/v1/verify-otp';
  static const String login = '/api/v1/login';
  static const String requestPasswordReset = '/api/v1/request-password-reset';
  static const String resetPassword = '/api/v1/reset-password';
  static const String refreshToken = '/api/v1/refresh-token';
  static const String logout = '/api/v1/logout';
}
```

#### 1.2 HTTP Client Setup
```dart
// lib/core/api/dio_client.dart
import 'package:dio/dio.dart';
import 'package:pretty_dio_logger/pretty_dio_logger.dart';

class DioClient {
  static late Dio _dio;
  
  static void init() {
    _dio = Dio(BaseOptions(
      baseUrl: ApiConfig.baseUrl,
      connectTimeout: const Duration(seconds: 30),
      receiveTimeout: const Duration(seconds: 30),
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': ApiConfig.apiKey,
      },
    ));
    
    // Add logging interceptor
    _dio.interceptors.add(PrettyDioLogger(
      requestHeader: true,
      requestBody: true,
      responseBody: true,
      responseHeader: false,
      compact: false,
    ));
    
    // Add token interceptor
    _dio.interceptors.add(TokenInterceptor());
  }
  
  static Dio get instance => _dio;
}
```

#### 1.3 Authentication Service
```dart
// lib/core/services/auth_service.dart
import 'package:dio/dio.dart';

class AuthService {
  final Dio _dio = DioClient.instance;
  
  // Register user
  Future<AuthResponse> register({
    required String fullName,
    required String email,
    required String password,
    required String confirmPassword,
    required bool isTermAccepted,
  }) async {
    try {
      final response = await _dio.post(
        ApiConfig.register,
        data: {
          'full_name': fullName,
          'email': email,
          'password': password,
          'confirm_password': confirmPassword,
          'is_term_accepted': isTermAccepted,
        },
      );
      
      return AuthResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Verify OTP
  Future<OtpVerificationResponse> verifyOtp({
    required String email,
    required String otp,
  }) async {
    try {
      final response = await _dio.post(
        ApiConfig.verifyOtp,
        data: {
          'email': email,
          'otp': otp,
        },
      );
      
      return OtpVerificationResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Login
  Future<LoginResponse> login({
    required String email,
    required String password,
    String? deviceId,
  }) async {
    try {
      final response = await _dio.post(
        ApiConfig.login,
        data: {
          'email': email,
          'password': password,
          if (deviceId != null) 'device_id': deviceId,
        },
      );
      
      return LoginResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Request password reset
  Future<void> requestPasswordReset(String email) async {
    try {
      await _dio.post(
        ApiConfig.requestPasswordReset,
        data: {'email': email},
      );
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Reset password
  Future<PasswordResetResponse> resetPassword({
    required String token,
    required String newPassword,
  }) async {
    try {
      final response = await _dio.post(
        ApiConfig.resetPassword,
        data: {
          'token': token,
          'new_password': newPassword,
        },
      );
      
      return PasswordResetResponse.fromJson(response.data);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Logout
  Future<void> logout() async {
    try {
      await _dio.post(ApiConfig.logout);
    } on DioException catch (e) {
      throw _handleError(e);
    }
  }
  
  // Error handling
  String _handleError(DioException e) {
    if (e.response != null) {
      final data = e.response!.data;
      if (data is Map<String, dynamic>) {
        return data['detail'] ?? data['message'] ?? 'An error occurred';
      }
    }
    return 'Network error occurred';
  }
}
```

### Step 2: Data Models

#### 2.1 Response Models
```dart
// lib/core/models/auth_models.dart

class AuthResponse {
  final String message;
  final String userId;
  final String email;
  final bool verificationRequired;
  
  AuthResponse({
    required this.message,
    required this.userId,
    required this.email,
    required this.verificationRequired,
  });
  
  factory AuthResponse.fromJson(Map<String, dynamic> json) {
    return AuthResponse(
      message: json['message'] ?? '',
      userId: json['user_id'] ?? '',
      email: json['email'] ?? '',
      verificationRequired: json['verification_required'] ?? false,
    );
  }
}

class LoginResponse {
  final String accessToken;
  final String refreshToken;
  final String tokenType;
  final int expiresIn;
  final User user;
  
  LoginResponse({
    required this.accessToken,
    required this.refreshToken,
    required this.tokenType,
    required this.expiresIn,
    required this.user,
  });
  
  factory LoginResponse.fromJson(Map<String, dynamic> json) {
    return LoginResponse(
      accessToken: json['access_token'] ?? '',
      refreshToken: json['refresh_token'] ?? '',
      tokenType: json['token_type'] ?? 'bearer',
      expiresIn: json['expires_in'] ?? 1800,
      user: User.fromJson(json['user'] ?? {}),
    );
  }
}

class User {
  final String id;
  final String email;
  final String role;
  final bool isEmailVerified;
  
  User({
    required this.id,
    required this.email,
    required this.role,
    required this.isEmailVerified,
  });
  
  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] ?? '',
      email: json['email'] ?? '',
      role: json['role'] ?? 'USER',
      isEmailVerified: json['is_email_verified'] ?? false,
    );
  }
}

class OtpVerificationResponse {
  final String message;
  final bool verified;
  final String userId;
  
  OtpVerificationResponse({
    required this.message,
    required this.verified,
    required this.userId,
  });
  
  factory OtpVerificationResponse.fromJson(Map<String, dynamic> json) {
    return OtpVerificationResponse(
      message: json['message'] ?? '',
      verified: json['verified'] ?? false,
      userId: json['user_id'] ?? '',
    );
  }
}

class PasswordResetResponse {
  final String message;
  
  PasswordResetResponse({required this.message});
  
  factory PasswordResetResponse.fromJson(Map<String, dynamic> json) {
    return PasswordResetResponse(
      message: json['message'] ?? '',
    );
  }
}
```

### Step 3: Token Management

#### 3.1 Secure Storage Service
```dart
// lib/core/services/storage_service.dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class StorageService {
  static const _storage = FlutterSecureStorage();
  
  // Keys
  static const String _accessTokenKey = 'access_token';
  static const String _refreshTokenKey = 'refresh_token';
  static const String _userDataKey = 'user_data';
  
  // Save tokens
  static Future<void> saveTokens({
    required String accessToken,
    required String refreshToken,
  }) async {
    await Future.wait([
      _storage.write(key: _accessTokenKey, value: accessToken),
      _storage.write(key: _refreshTokenKey, value: refreshToken),
    ]);
  }
  
  // Get access token
  static Future<String?> getAccessToken() async {
    return await _storage.read(key: _accessTokenKey);
  }
  
  // Get refresh token
  static Future<String?> getRefreshToken() async {
    return await _storage.read(key: _refreshTokenKey);
  }
  
  // Save user data
  static Future<void> saveUserData(User user) async {
    await _storage.write(key: _userDataKey, value: jsonEncode(user.toJson()));
  }
  
  // Get user data
  static Future<User?> getUserData() async {
    final userData = await _storage.read(key: _userDataKey);
    if (userData != null) {
      return User.fromJson(jsonDecode(userData));
    }
    return null;
  }
  
  // Clear all data
  static Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
```

#### 3.2 Token Interceptor
```dart
// lib/core/api/token_interceptor.dart
import 'package:dio/dio.dart';

class TokenInterceptor extends Interceptor {
  @override
  void onRequest(RequestOptions options, RequestInterceptorHandler handler) async {
    // Add access token to requests that need authentication
    if (_needsAuth(options.path)) {
      final token = await StorageService.getAccessToken();
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
    }
    handler.next(options);
  }
  
  @override
  void onError(DioException err, ErrorInterceptorHandler handler) async {
    // Handle token refresh on 401 errors
    if (err.response?.statusCode == 401 && _needsAuth(err.requestOptions.path)) {
      final refreshed = await _refreshToken();
      if (refreshed) {
        // Retry the original request
        final newToken = await StorageService.getAccessToken();
        err.requestOptions.headers['Authorization'] = 'Bearer $newToken';
        
        final dio = Dio();
        final response = await dio.fetch(err.requestOptions);
        handler.resolve(response);
        return;
      }
    }
    handler.next(err);
  }
  
  bool _needsAuth(String path) {
    final protectedPaths = ['/api/v1/logout'];
    return protectedPaths.any((p) => path.contains(p));
  }
  
  Future<bool> _refreshToken() async {
    try {
      final refreshToken = await StorageService.getRefreshToken();
      if (refreshToken == null) return false;
      
      final dio = Dio();
      final response = await dio.post(
        '${ApiConfig.baseUrl}${ApiConfig.refreshToken}',
        options: Options(headers: {'Cookie': 'refresh_token=$refreshToken'}),
      );
      
      final newAccessToken = response.data['access_token'];
      await StorageService.saveTokens(
        accessToken: newAccessToken,
        refreshToken: refreshToken,
      );
      
      return true;
    } catch (e) {
      await StorageService.clearAll();
      return false;
    }
  }
}
```

### Step 4: State Management

#### 4.1 Authentication Provider
```dart
// lib/providers/auth_provider.dart
import 'package:flutter/material.dart';

class AuthProvider extends ChangeNotifier {
  final AuthService _authService = AuthService();
  
  User? _user;
  bool _isAuthenticated = false;
  bool _isLoading = false;
  
  User? get user => _user;
  bool get isAuthenticated => _isAuthenticated;
  bool get isLoading => _isLoading;
  
  // Initialize authentication state
  Future<void> init() async {
    _isLoading = true;
    notifyListeners();
    
    try {
      final token = await StorageService.getAccessToken();
      final userData = await StorageService.getUserData();
      
      if (token != null && userData != null) {
        _user = userData;
        _isAuthenticated = true;
      }
    } catch (e) {
      await StorageService.clearAll();
    }
    
    _isLoading = false;
    notifyListeners();
  }
  
  // Register
  Future<String?> register({
    required String fullName,
    required String email,
    required String password,
    required String confirmPassword,
    required bool isTermAccepted,
  }) async {
    try {
      _isLoading = true;
      notifyListeners();
      
      final response = await _authService.register(
        fullName: fullName,
        email: email,
        password: password,
        confirmPassword: confirmPassword,
        isTermAccepted: isTermAccepted,
      );
      
      return null; // Success
    } catch (e) {
      return e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  // Login
  Future<String?> login({
    required String email,
    required String password,
  }) async {
    try {
      _isLoading = true;
      notifyListeners();
      
      final response = await _authService.login(
        email: email,
        password: password,
      );
      
      await StorageService.saveTokens(
        accessToken: response.accessToken,
        refreshToken: response.refreshToken,
      );
      await StorageService.saveUserData(response.user);
      
      _user = response.user;
      _isAuthenticated = true;
      
      return null; // Success
    } catch (e) {
      return e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
  
  // Logout
  Future<void> logout() async {
    try {
      await _authService.logout();
    } catch (e) {
      // Continue with logout even if API call fails
    }
    
    await StorageService.clearAll();
    _user = null;
    _isAuthenticated = false;
    notifyListeners();
  }
  
  // Verify OTP
  Future<String?> verifyOtp({
    required String email,
    required String otp,
  }) async {
    try {
      _isLoading = true;
      notifyListeners();
      
      await _authService.verifyOtp(email: email, otp: otp);
      return null; // Success
    } catch (e) {
      return e.toString();
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
```

## 🔧 Backend Configuration

### Update CORS Settings

Add this to your FastAPI backend:

```python
# app/main.py
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Add your Flutter app URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 🔐 Environment Configuration

### Backend (.env)
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost/authdb
BACKEND_API_KEY=your_secure_api_key_here
RESEND_API_KEY=your_resend_api_key
RESEND_FROM_EMAIL=noreply@yourdomain.com
JWT_ACCESS_TOKEN_SECRET=your_jwt_access_secret
JWT_REFRESH_TOKEN_SECRET=your_jwt_refresh_secret
JWT_ACCESS_TOKEN_EXPIRATION=30m
JWT_REFRESH_TOKEN_EXPIRATION=7d
```

### Flutter (Environment Variables)
```dart
// lib/core/config/environment.dart
class Environment {
  static const String apiBaseUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );
  
  static const String apiKey = String.fromEnvironment(
    'API_KEY',
    defaultValue: 'your_backend_api_key',
  );
}
```

## 🧪 Testing Integration

### 1. Start Backend
```bash
cd authentication_app
uvicorn app.main:app --reload --port 8000
```

### 2. Test API Endpoints
```bash
# Test registration
curl -X POST "http://localhost:8000/api/v1/register" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: your_backend_api_key" \
  -d '{
    "full_name": "Test User",
    "email": "test@example.com",
    "password": "TestPassword123!",
    "confirm_password": "TestPassword123!",
    "is_term_accepted": true
  }'
```

### 3. Update Flutter Dependencies
Add to `pubspec.yaml`:
```yaml
dependencies:
  dio: ^5.8.0+1
  pretty_dio_logger: ^1.4.0
  flutter_secure_storage: ^9.2.4
  provider: ^6.1.1
```

## 🚀 Deployment Considerations

### Production Backend URL
Update the Flutter app's API base URL for production:
```dart
static const String baseUrl = kDebugMode 
  ? 'http://localhost:8000'
  : 'https://your-production-api.com';
```

### SSL/TLS Requirements
- Backend must use HTTPS in production
- Configure proper SSL certificates
- Update CORS settings for production domain

This comprehensive plan provides everything needed to successfully integrate your Flutter frontend with the FastAPI backend, including proper error handling, security measures, and production-ready configurations.
