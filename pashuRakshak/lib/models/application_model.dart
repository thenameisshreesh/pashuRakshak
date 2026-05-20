class ApplicationModel {
  final String id;
  final String farmerId;
  final String schemeId;
  final String schemeName;
  final String farmerName;
  final String status;
  final String? rejectionReason;
  final String? rejectionNotes;
  final int rfidTagsAllocated;
  final DateTime createdAt;
  final Map<String, dynamic> step1Data;
  final Map<String, dynamic> step2Data;
  final Map<String, dynamic> step3Data;

  ApplicationModel({
    required this.id,
    required this.farmerId,
    required this.schemeId,
    required this.schemeName,
    required this.farmerName,
    required this.status,
    this.rejectionReason,
    this.rejectionNotes,
    required this.rfidTagsAllocated,
    required this.createdAt,
    required this.step1Data,
    required this.step2Data,
    required this.step3Data,
  });

  factory ApplicationModel.fromJson(Map<String, dynamic> json) {
    return ApplicationModel(
      id: json['_id'] ?? json['id'] ?? '',
      farmerId: json['farmer_id'] ?? '',
      schemeId: json['scheme_id'] ?? '',
      schemeName: json['scheme_name'] ?? 'Cattle Scheme',
      farmerName: json['farmer_name'] ?? 'Farmer',
      status: json['status'] ?? 'pending',
      rejectionReason: json['rejection_reason'],
      rejectionNotes: json['rejection_notes'],
      rfidTagsAllocated: json['rfid_tags_allocated'] ?? 0,
      createdAt: DateTime.tryParse(json['created_at']?.toString() ?? '') ?? DateTime.now(),
      step1Data: json['step1_data'] ?? {},
      step2Data: json['step2_data'] ?? {},
      step3Data: json['step3_data'] ?? {},
    );
  }
}
