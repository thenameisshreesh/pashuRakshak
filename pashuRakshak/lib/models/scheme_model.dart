class SchemeModel {
  final String id;
  final String name;
  final String motive;
  final String eligibility;
  final String sponsor;
  final String benefits;
  final String description;
  final int requiredValidations;
  final int requiredCattleCount;
  final int durationDays;
  final bool active;

  SchemeModel({
    required this.id,
    required this.name,
    required this.motive,
    required this.eligibility,
    required this.sponsor,
    required this.benefits,
    required this.description,
    required this.requiredValidations,
    required this.requiredCattleCount,
    required this.durationDays,
    required this.active,
  });

  factory SchemeModel.fromJson(Map<String, dynamic> json) {
    return SchemeModel(
      id: json['_id'] ?? json['id'] ?? '',
      name: json['name'] ?? '',
      motive: json['motive'] ?? '',
      eligibility: json['eligibility'] ?? '',
      sponsor: json['sponsor'] ?? '',
      benefits: json['benefits'] ?? '',
      description: json['description'] ?? '',
      requiredValidations: json['required_validations'] ?? 1,
      requiredCattleCount: json['required_cattle_count'] ?? 1,
      durationDays: json['duration_days'] ?? 365,
      active: json['active'] ?? true,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'motive': motive,
      'eligibility': eligibility,
      'sponsor': sponsor,
      'benefits': benefits,
      'description': description,
      'required_validations': requiredValidations,
      'required_cattle_count': requiredCattleCount,
      'duration_days': durationDays,
      'active': active,
    };
  }
}
