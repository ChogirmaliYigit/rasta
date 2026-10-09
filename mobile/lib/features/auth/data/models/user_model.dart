import 'package:json_annotation/json_annotation.dart';
import '../../domain/entities/user_entity.dart';

part 'user_model.g.dart';

@JsonSerializable()
class UserModel extends UserEntity {
  @JsonKey(name: 'full_name')
  final String fullName;
  
  @JsonKey(name: 'organization_id')
  final String organizationId;
  
  @JsonKey(name: 'branch_id')
  final String branchId;
  
  @JsonKey(name: 'is_active')
  final bool isActive;

  const UserModel({
    required super.id,
    required this.fullName,
    required super.phone,
    required super.role,
    required this.organizationId,
    required this.branchId,
    required this.isActive,
  }) : super(
          fullName: fullName,
          organizationId: organizationId,
          branchId: branchId,
          isActive: isActive,
        );

  factory UserModel.fromJson(Map<String, dynamic> json) => _$UserModelFromJson(json);
  Map<String, dynamic> toJson() => _$UserModelToJson(this);
}
