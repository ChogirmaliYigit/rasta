import 'dart:io' show Platform;
import 'package:flutter/foundation.dart' show kIsWeb;

class ApiEndpoints {
  static String get baseUrl {
    const String env = String.fromEnvironment('ENVIRONMENT', defaultValue: 'development');
    const String apiUrl = String.fromEnvironment('API_URL', defaultValue: '');
    
    if (env == 'production' && apiUrl.isNotEmpty) {
      return apiUrl;
    }

    if (kIsWeb) {
      return 'http://localhost:8001/api/v1';
    }
    if (Platform.isAndroid) {
      return 'http://10.0.2.2:8001/api/v1';
    }
    return 'http://localhost:8001/api/v1';
  }

  static const String login = '/auth/login';
  static const String refresh = '/auth/refresh';
  static const String me = '/auth/me';
  static const String catalog = '/catalog';
  static const String orders = '/orders';
  static const String inventory = '/retailer-inventory';
  static const String posSales = '/pos-sales';
}
