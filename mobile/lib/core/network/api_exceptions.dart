class ServerException implements Exception {
  final int? statusCode;
  final String message;

  ServerException({this.statusCode, required this.message});
}

class NetworkException implements Exception {}

class UnauthorizedException implements Exception {}

class ValidationException implements Exception {
  final Map<String, dynamic> errors;

  ValidationException(this.errors);
}
