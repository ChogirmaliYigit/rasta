import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import 'package:flutter/foundation.dart';
import '../../config/app_config.dart';
import '../constants/api_endpoints.dart';
import 'api_exceptions.dart';

final secureStorageProvider = Provider((ref) => const FlutterSecureStorage());

final dioProvider = Provider<Dio>((ref) {
  final dio = Dio(BaseOptions(
    baseUrl: AppConfig.apiBaseUrl,
    connectTimeout: const Duration(seconds: 30),
    receiveTimeout: const Duration(seconds: 30),
    contentType: 'application/json',
  ));

  final secureStorage = ref.watch(secureStorageProvider);

  dio.interceptors.add(QueuedInterceptorsWrapper(
    onRequest: (options, handler) async {
      final token = await secureStorage.read(key: 'access_token');
      if (token != null) {
        options.headers['Authorization'] = 'Bearer $token';
      }
      return handler.next(options);
    },
    onError: (DioException e, handler) async {
      if (e.response?.statusCode == 401) {
        // Attempt refresh
        final refreshToken = await secureStorage.read(key: 'refresh_token');
        if (refreshToken != null) {
          try {
            final refreshDio = Dio(BaseOptions(baseUrl: AppConfig.apiBaseUrl));
            final response = await refreshDio.post(
              ApiEndpoints.refresh,
              data: {'refresh_token': refreshToken},
            );
            
            final newAccessToken = response.data['access_token'];
            final newRefreshToken = response.data['refresh_token'];
            
            await secureStorage.write(key: 'access_token', value: newAccessToken);
            await secureStorage.write(key: 'refresh_token', value: newRefreshToken);
            
            // Retry original request
            e.requestOptions.headers['Authorization'] = 'Bearer $newAccessToken';
            final retryResponse = await refreshDio.fetch(e.requestOptions);
            return handler.resolve(retryResponse);
          } catch (_) {
            await secureStorage.delete(key: 'access_token');
            await secureStorage.delete(key: 'refresh_token');
            // Redirect to login handled by router listening to auth state
            return handler.reject(e);
          }
        }
      }
      
      // Parse exception
      if (e.type == DioExceptionType.connectionTimeout || e.type == DioExceptionType.receiveTimeout || e.type == DioExceptionType.connectionError) {
         throw NetworkException();
      } else if (e.response?.statusCode == 401) {
         throw UnauthorizedException();
      } else if (e.response?.statusCode == 422) {
         throw ValidationException(e.response?.data['errors'] ?? {});
      } else {
         throw ServerException(
           statusCode: e.response?.statusCode,
           message: e.response?.data['message'] ?? e.message ?? 'Unknown error',
         );
      }
    },
  ));

  if (kDebugMode) {
    dio.interceptors.add(LogInterceptor(responseBody: true, requestBody: true));
  }

  return dio;
});
