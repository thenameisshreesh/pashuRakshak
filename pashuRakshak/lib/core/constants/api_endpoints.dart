class ApiEndpoints {
  ApiEndpoints._();

  // Base URL - use 10.0.2.2 for Android emulator, localhost for web/iOS
  static const String baseUrl = 'http://10.0.2.2:5000';

  // Auth endpoints
  static const String login = '$baseUrl/api/auth/login';
  static const String register = '$baseUrl/api/auth/register';
  static const String refreshToken = '$baseUrl/api/auth/refresh';
  static const String profile = '$baseUrl/api/auth/profile';
  static const String updateProfile = '$baseUrl/api/auth/profile/update';

  // Scheme endpoints
  static const String schemes = '$baseUrl/api/schemes';
  static String schemeDetail(String id) => '$baseUrl/api/schemes/$id';

  // Application endpoints
  static const String applications = '$baseUrl/api/applications';
  static String applicationDetail(String id) => '$baseUrl/api/applications/$id';
  static const String submitApplication = '$baseUrl/api/applications/submit';
  static String applicationStatus(String id) => '$baseUrl/api/applications/$id/status';

  // Notification endpoints
  static const String notifications = '$baseUrl/api/notifications';
  static String markNotificationRead(String id) => '$baseUrl/api/notifications/$id/read';
  static const String markAllRead = '$baseUrl/api/notifications/mark-all-read';

  // File upload
  static const String uploadFile = '$baseUrl/api/upload';

  // Dashboard
  static const String dashboard = '$baseUrl/api/dashboard';
}
