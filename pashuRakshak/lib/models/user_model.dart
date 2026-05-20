class UserModel {
  final String id;
  final String name;
  final String? mobile;
  final String? username;
  final String role;
  final int? cattleCount;
  final double? landAcres;
  final String? state;
  final String? district;
  final String? city;
  final String? address;
  final String? aadhaar;
  final String? bankAccount;
  final String? ifsc;

  UserModel({
    required this.id,
    required this.name,
    this.mobile,
    this.username,
    required this.role,
    this.cattleCount,
    this.landAcres,
    this.state,
    this.district,
    this.city,
    this.address,
    this.aadhaar,
    this.bankAccount,
    this.ifsc,
  });

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['_id'] ?? json['id'] ?? '',
      name: json['name'] ?? '',
      mobile: json['mobile'],
      username: json['username'],
      role: json['role'] ?? 'farmer',
      cattleCount: json['cattle_count'] is int ? json['cattle_count'] : int.tryParse(json['cattle_count']?.toString() ?? ''),
      landAcres: json['land_acres'] is num ? (json['land_acres'] as num).toDouble() : double.tryParse(json['land_acres']?.toString() ?? ''),
      state: json['state'],
      district: json['district'],
      city: json['city'],
      address: json['address'],
      aadhaar: json['aadhaar'],
      bankAccount: json['bank_account'],
      ifsc: json['ifsc'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'mobile': mobile,
      'username': username,
      'role': role,
      'cattle_count': cattleCount,
      'land_acres': landAcres,
      'state': state,
      'district': district,
      'city': city,
      'address': address,
      'aadhaar': aadhaar,
      'bank_account': bankAccount,
      'ifsc': ifsc,
    };
  }
}
