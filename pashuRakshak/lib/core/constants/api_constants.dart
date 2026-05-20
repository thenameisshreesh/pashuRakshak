class ApiConstants {
  // Use 10.0.2.2 for Android Emulator, localhost for iOS/web, or your local machine IP
  static const String baseUrl = 'http://10.0.2.2:5000/api';

  static const String login = '$baseUrl/auth/login';
  static const String registerFarmer = '$baseUrl/auth/register/farmer';
  static const String registerOfficer = '$baseUrl/auth/register/officer';
  static const String profile = '$baseUrl/auth/profile';

  static const String schemes = '$baseUrl/schemes';
  static const String applications = '$baseUrl/applications';
  static const String filesUpload = '$baseUrl/files/upload';
  
  static String fileUrl(String id) => '$baseUrl/files/$id';
}
