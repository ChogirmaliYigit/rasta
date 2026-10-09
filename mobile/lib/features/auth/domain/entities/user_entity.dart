import 'package:equatable/equatable.dart';

class UserEntity extends Equatable {
  final String id;
  final String fullName;
  final String phone;
  final String role;
  final String organizationId;
  final String branchId;
  final bool isActive;

  const UserEntity({
    required this.id,
    required this.fullName,
    required this.phone,
    required this.role,
    required this.organizationId,
    required this.branchId,
    required this.isActive,
  });

  @override
  List<Object?> get props => [id, fullName, phone, role, organizationId, branchId, isActive];
}
