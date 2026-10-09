abstract class Failure {
  final String message;
  Failure(this.message);
}

class ServerFailure extends Failure {
  ServerFailure(super.message);
}

class NetworkFailure extends Failure {
  NetworkFailure([String message = 'No internet connection']) : super(message);
}

class CacheFailure extends Failure {
  CacheFailure(super.message);
}

class UnauthorizedFailure extends Failure {
  UnauthorizedFailure([String message = 'Unauthorized']) : super(message);
}
