import 'dart:convert';
import 'dart:io';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import '../core/constants/api_constants.dart';
import '../models/scheme_model.dart';
import '../models/application_model.dart';

class SchemeProvider with ChangeNotifier {
  List<SchemeModel> _schemes = [];
  List<ApplicationModel> _myApplications = [];
  bool _isLoading = false;

  List<SchemeModel> get schemes => _schemes;
  List<ApplicationModel> get myApplications => _myApplications;
  bool get isLoading => _isLoading;

  Future<void> fetchSchemes() async {
    _isLoading = true;
    notifyListeners();

    try {
      final response = await http.get(Uri.parse(ApiConstants.schemes));
      if (response.statusCode == 200) {
        final resData = json.decode(response.body);
        final List<dynamic> list = resData['data'] ?? resData;
        _schemes = list.map((item) => SchemeModel.fromJson(item)).toList();
      }
    } catch (e) {
      // Mock fallback if offline
      _schemes = [
        SchemeModel(
          id: '1',
          name: 'Rashtriya Gokul Mission',
          motive: 'To breed high-genetic quality cattle and enhance milk output.',
          eligibility: 'Farmers owning at least 5 cows with land holdings.',
          sponsor: 'Ministry of Animal Husbandry',
          benefits: '50% subsidy on dairy equipment and feed support.',
          description: 'A national scheme focused on development and conservation of indigenous breeds to enhance milk production.',
          requiredValidations: 2,
          requiredCattleCount: 5,
          durationDays: 365,
          active: true,
        ),
      ];
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

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

  Future<String> uploadFile(File file, String token) async {
    try {
      final request = http.MultipartRequest('POST', Uri.parse(ApiConstants.filesUpload));
      request.headers['Authorization'] = 'Bearer $token';
      request.files.add(await http.MultipartFile.fromPath('file', file.path));

      final streamedResponse = await request.send();
      final response = await http.Response.fromStream(streamedResponse);

      if (response.statusCode == 201) {
        final data = json.decode(response.body);
        return data['file_id'] ?? '';
      } else {
        throw Exception('Upload failed with status ${response.statusCode}');
      }
    } catch (e) {
      throw Exception('File upload failed: $e');
    }
  }

  Future<bool> submitApplication({
    required String token,
    required String farmerId,
    required String schemeId,
    required Map<String, dynamic> step1,
    required Map<String, dynamic> step2,
    required Map<String, dynamic> step3,
  }) async {
    _isLoading = true;
    notifyListeners();

    try {
      final body = {
        'farmer_id': farmerId,
        'scheme_id': schemeId,
        'step1_data': step1,
        'step2_data': step2,
        'step3_data': step3,
      };

      final response = await http.post(
        Uri.parse(ApiConstants.applications),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer $token',
        },
        body: json.encode(body),
      );

      if (response.statusCode == 201) {
        _isLoading = false;
        fetchMyApplications(token); // refresh applications
        return true;
      } else {
        final data = json.decode(response.body);
        throw Exception(data['message'] ?? 'Application submission failed');
      }
    } catch (e) {
      _isLoading = false;
      notifyListeners();
      rethrow;
    }
  }
}
