import '../entities/user_entity.dart';

abstract class AuthRepository {
  Future<UserEntity> login(String phone, String password);
  Future<void> logout();
  Future<UserEntity?> checkAuth();
}
