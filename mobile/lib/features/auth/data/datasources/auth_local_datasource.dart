import 'dart:convert';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';
import '../models/user_model.dart';
import '../models/token_model.dart';

abstract class AuthLocalDataSource {
  Future<void> saveTokens(TokenModel tokens);
  Future<void> saveUser(UserModel user);
  Future<String?> getAccessToken();
  Future<String?> getRefreshToken();
  Future<UserModel?> getUser();
  Future<void> clearAll();
}

class AuthLocalDataSourceImpl implements AuthLocalDataSource {
  final FlutterSecureStorage secureStorage;

  AuthLocalDataSourceImpl(this.secureStorage);

  @override
  Future<void> saveTokens(TokenModel tokens) async {
    await secureStorage.write(key: 'access_token', value: tokens.accessToken);
    await secureStorage.write(key: 'refresh_token', value: tokens.refreshToken);
  }

  @override
  Future<void> saveUser(UserModel user) async {
    await secureStorage.write(key: 'user', value: jsonEncode(user.toJson()));
  }

  @override
  Future<String?> getAccessToken() async {
    return await secureStorage.read(key: 'access_token');
  }

  @override
  Future<String?> getRefreshToken() async {
    return await secureStorage.read(key: 'refresh_token');
  }

  @override
  Future<UserModel?> getUser() async {
    final userStr = await secureStorage.read(key: 'user');
    if (userStr != null) {
      return UserModel.fromJson(jsonDecode(userStr));
    }
    return null;
  }

  @override
  Future<void> clearAll() async {
    await secureStorage.deleteAll();
  }
}
