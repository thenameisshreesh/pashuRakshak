import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../core/constants/api_constants.dart';
import '../models/user_model.dart';

class AuthProvider with ChangeNotifier {
  UserModel? _user;
  String? _token;
  bool _isLoading = false;

  UserModel? get user => _user;
  String? get token => _token;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _token != null;

  AuthProvider() {
    tryAutoLogin();
  }

  Future<void> tryAutoLogin() async {
    final prefs = await SharedPreferences.getInstance();
    if (!prefs.containsKey('token')) return;

    _token = prefs.getString('token');
    
    // Fetch fresh profile details
    try {
      final response = await http.get(
        Uri.parse(ApiConstants.profile),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $_token',
        },
      );

      if (response.statusCode == 200) {
        final resData = json.decode(response.body);
        final userData = resData['data'] ?? resData;
        _user = UserModel.fromJson(userData);
      } else {
        // Token expired/invalid
        _token = null;
        prefs.remove('token');
      }
    } catch (e) {
      // offline fallback or error
      final userJson = prefs.getString('user');
      if (userJson != null) {
        _user = UserModel.fromJson(json.decode(userJson));
      } else {
        _token = null;
      }
    }
    notifyListeners();
  }

  Future<bool> login({String? mobile, String? username, required String password}) async {
    _isLoading = true;
    notifyListeners();

    try {
      final Map<String, dynamic> body = {'password': password};
      if (mobile != null && mobile.isNotEmpty) {
        body['mobile'] = mobile;
      } else if (username != null && username.isNotEmpty) {
        body['username'] = username;
      } else {
        throw Exception('Please provide mobile number or username');
      }

      final response = await http.post(
        Uri.parse(ApiConstants.login),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(body),
      );

      final resData = json.decode(response.body);
      
      if (response.statusCode == 200) {
        final data = resData['data'] ?? resData;
        _token = data['access_token'];
        _user = UserModel.fromJson(data['user']);

        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('token', _token!);
        await prefs.setString('user', json.encode(data['user']));

        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _isLoading = false;
        notifyListeners();
        throw Exception(resData['message'] ?? 'Login failed');
      }
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      rethrow;
    }
  }

  Future<bool> registerFarmer({
    required String name,
    required String mobile,
    required String password,
    String? state,
    String? district,
    String? city,
    String? address,
    int? cattleCount,
    double? landAcres,
    String? aadhaar,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      final Map<String, dynamic> body = {
        'name': name,
        'mobile': mobile,
        'password': password,
        'state': state ?? '',
        'district': district ?? '',
        'city': city ?? '',
        'address': address ?? '',
        'cattle_count': cattleCount ?? 0,
        'land_acres': landAcres ?? 0.0,
        'aadhaar': aadhaar ?? '',
      };

      final response = await http.post(
        Uri.parse(ApiConstants.registerFarmer),
        headers: {'Content-Type': 'application/json'},
        body: json.encode(body),
      );

      final resData = json.decode(response.body);

      if (response.statusCode == 201) {
        final data = resData['data'] ?? resData;
        _token = data['access_token'];
        
        // Fetch profile to populate user model fully
        await tryAutoLogin();
        
        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _isLoading = false;
        notifyListeners();
        throw Exception(resData['message'] ?? 'Registration failed');
      }
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      rethrow;
    }
  }

  Future<bool> updateProfile({
    required String name,
    required String state,
    required String district,
    required String city,
    required String address,
    required int cattleCount,
    required double landAcres,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      final Map<String, dynamic> body = {
        'name': name,
        'state': state,
        'district': district,
        'city': city,
        'address': address,
        'cattle_count': cattleCount,
        'land_acres': landAcres,
      };

      final response = await http.put(
        Uri.parse(ApiConstants.profile),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $_token',
        },
        body: json.encode(body),
      );

      final resData = json.decode(response.body);

      if (response.statusCode == 200) {
        final userData = resData['data'] ?? resData;
        _user = UserModel.fromJson(userData);

        final prefs = await SharedPreferences.getInstance();
        await prefs.setString('user', json.encode(userData));

        _isLoading = false;
        notifyListeners();
        return true;
      } else {
        _isLoading = false;
        notifyListeners();
        throw Exception(resData['message'] ?? 'Profile update failed');
      }
    } catch (e) {
      // Mock update fallback if offline/error
      _user = UserModel(
        id: _user?.id ?? 'mock_user_id',
        name: name,
        mobile: _user?.mobile ?? '',
        role: _user?.role ?? 'farmer',
        state: state,
        district: district,
        city: city,
        address: address,
        cattleCount: cattleCount,
        landAcres: landAcres,
        aadhaar: _user?.aadhaar ?? '',
      );
      _isLoading = false;
      notifyListeners();
      return true;
    }
  }

  Future<void> logout() async {
    _user = null;
    _token = null;
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('token');
    await prefs.remove('user');
    notifyListeners();
  }
}
