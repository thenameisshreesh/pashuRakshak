class AppConstants {
  AppConstants._();

  static const String appName = 'PashuRakshak';
  static const String appVersion = '1.0.0';
  static const String appBuildNumber = '1';

  // Storage Keys
  static const String tokenKey = 'auth_token';
  static const String refreshTokenKey = 'refresh_token';
  static const String languageKey = 'selected_language';
  static const String themeKey = 'dark_mode';
  static const String firstLaunchKey = 'first_launch';
  static const String userDataKey = 'user_data';

  // Supported Languages
  static const String langEnglish = 'en';
  static const String langHindi = 'hi';
  static const String langMarathi = 'mr';

  // Indian States
  static const List<String> indianStates = [
    'Andhra Pradesh', 'Arunachal Pradesh', 'Assam', 'Bihar',
    'Chhattisgarh', 'Goa', 'Gujarat', 'Haryana',
    'Himachal Pradesh', 'Jharkhand', 'Karnataka', 'Kerala',
    'Madhya Pradesh', 'Maharashtra', 'Manipur', 'Meghalaya',
    'Mizoram', 'Nagaland', 'Odisha', 'Punjab',
    'Rajasthan', 'Sikkim', 'Tamil Nadu', 'Telangana',
    'Tripura', 'Uttar Pradesh', 'Uttarakhand', 'West Bengal',
  ];

  // Cattle Types
  static const List<String> cattleTypes = [
    'Cow', 'Buffalo', 'Goat', 'Sheep', 'Pig', 'Poultry', 'Other',
  ];

  // Gender Options
  static const List<String> genderOptions = ['Male', 'Female', 'Other'];
}
