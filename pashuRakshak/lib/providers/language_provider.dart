import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class LanguageProvider with ChangeNotifier {
  Locale _appLocale = const Locale('en');

  Locale get appLocale => _appLocale;

  LanguageProvider() {
    fetchLocale();
  }

  Future<void> fetchLocale() async {
    final prefs = await SharedPreferences.getInstance();
    if (!prefs.containsKey('language_code')) {
      _appLocale = const Locale('en');
      return;
    }
    _appLocale = Locale(prefs.getString('language_code') ?? 'en');
    notifyListeners();
  }

  Future<void> changeLanguage(Locale type) async {
    final prefs = await SharedPreferences.getInstance();
    if (_appLocale == type) return;

    if (type == const Locale('mr')) {
      _appLocale = const Locale('mr');
      await prefs.setString('language_code', 'mr');
    } else if (type == const Locale('hi')) {
      _appLocale = const Locale('hi');
      await prefs.setString('language_code', 'hi');
    } else {
      _appLocale = const Locale('en');
      await prefs.setString('language_code', 'en');
    }
    notifyListeners();
  }
}
