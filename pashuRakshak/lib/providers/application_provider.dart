import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../core/constants/api_constants.dart';
import '../models/application_model.dart';

class ApplicationProvider with ChangeNotifier {
  List<ApplicationModel> _myApplications = [];
  bool _isLoading = false;

  List<ApplicationModel> get myApplications => _myApplications;
  bool get isLoading => _isLoading;

  Future<void> fetchMyApplications(String token) async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.get(
        Uri.parse(ApiConstants.applications),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
      );

      if (response.statusCode == 200) {
        final resData = json.decode(response.body);
        final List<dynamic> list = resData['data'] ?? resData;
        _myApplications = list.map((item) => ApplicationModel.fromJson(item)).toList();
      }
    } catch (e) {
      _myApplications = [];
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }
}
