import 'package:dio/dio.dart';
import '../../../../core/constants/api_endpoints.dart';
import '../models/user_model.dart';
import '../models/token_model.dart';

abstract class AuthRemoteDataSource {
  Future<TokenModel> login(String phone, String password);
  Future<TokenModel> refreshToken(String refreshToken);
  Future<UserModel> getMe();
}

class AuthRemoteDataSourceImpl implements AuthRemoteDataSource {
  final Dio dio;

  AuthRemoteDataSourceImpl(this.dio);

  @override
  Future<TokenModel> login(String phone, String password) async {
    final response = await dio.post(ApiEndpoints.login, data: {
      'phone': phone,
      'password': password,
    });
    return TokenModel.fromJson(response.data);
  }

  @override
  Future<TokenModel> refreshToken(String refreshToken) async {
    final response = await dio.post(ApiEndpoints.refresh, data: {
      'refresh_token': refreshToken,
    });
    return TokenModel.fromJson(response.data);
  }

  @override
  Future<UserModel> getMe() async {
    final response = await dio.get(ApiEndpoints.me);
    return UserModel.fromJson(response.data);
  }
}
