import '../../domain/entities/user_entity.dart';
import '../../domain/repositories/auth_repository.dart';
import '../datasources/auth_local_datasource.dart';
import '../datasources/auth_remote_datasource.dart';

class AuthRepositoryImpl implements AuthRepository {
  final AuthRemoteDataSource remoteDataSource;
  final AuthLocalDataSource localDataSource;

  AuthRepositoryImpl({
    required this.remoteDataSource,
    required this.localDataSource,
  });

  @override
  Future<UserEntity> login(String phone, String password) async {
    final tokens = await remoteDataSource.login(phone, password);
    await localDataSource.saveTokens(tokens);
    final user = await remoteDataSource.getMe();
    await localDataSource.saveUser(user);
    return user;
  }

  @override
  Future<void> logout() async {
    await localDataSource.clearAll();
  }

  @override
  Future<UserEntity?> checkAuth() async {
    final token = await localDataSource.getAccessToken();
    if (token == null) return null;
    try {
      final user = await remoteDataSource.getMe();
      await localDataSource.saveUser(user);
      return user;
    } catch (e) {
      // If we can't fetch me, use local cached user
      return await localDataSource.getUser();
    }
  }
}
