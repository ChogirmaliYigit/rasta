// GENERATED CODE - DO NOT MODIFY BY HAND

part of 'user_model.dart';

// **************************************************************************
// JsonSerializableGenerator
// **************************************************************************

UserModel _$UserModelFromJson(Map<String, dynamic> json) => UserModel(
      id: json['id'] as String,
      fullName: json['full_name'] as String,
      phone: json['phone'] as String,
      role: json['role'] as String,
      organizationId: json['organization_id'] as String,
      branchId: json['branch_id'] as String,
      isActive: json['is_active'] as bool,
    );

Map<String, dynamic> _$UserModelToJson(UserModel instance) => <String, dynamic>{
      'id': instance.id,
      'phone': instance.phone,
      'role': instance.role,
      'full_name': instance.fullName,
      'organization_id': instance.organizationId,
      'branch_id': instance.branchId,
      'is_active': instance.isActive,
    };
