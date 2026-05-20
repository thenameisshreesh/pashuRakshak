import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/custom_button.dart';
import '../../widgets/custom_text_field.dart';
import '../../widgets/loading_overlay.dart';

class ProfileScreen extends StatefulWidget {
  const ProfileScreen({super.key});

  @override
  State<ProfileScreen> createState() => _ProfileScreenState();
}

class _ProfileScreenState extends State<ProfileScreen> {
  final _formKey = GlobalKey<FormState>();
  bool _isEditing = false;
  bool _isLoading = false;

  late TextEditingController _nameController;
  late TextEditingController _mobileController;
  late TextEditingController _stateController;
  late TextEditingController _districtController;
  late TextEditingController _cityController;
  late TextEditingController _cattleController;
  late TextEditingController _landController;
  late TextEditingController _addressController;

  @override
  void initState() {
    super.initState();
    final user = Provider.of<AuthProvider>(context, listen: false).user;
    
    _nameController = TextEditingController(text: user?.name ?? '');
    _mobileController = TextEditingController(text: user?.mobile ?? '');
    _stateController = TextEditingController(text: user?.state ?? '');
    _districtController = TextEditingController(text: user?.district ?? '');
    _cityController = TextEditingController(text: user?.city ?? '');
    _cattleController = TextEditingController(text: user?.cattleCount?.toString() ?? '0');
    _landController = TextEditingController(text: user?.landAcres?.toString() ?? '0.0');
    _addressController = TextEditingController(text: user?.address ?? '');
  }

  @override
  void dispose() {
    _nameController.dispose();
    _mobileController.dispose();
    _stateController.dispose();
    _districtController.dispose();
    _cityController.dispose();
    _cattleController.dispose();
    _landController.dispose();
    _addressController.dispose();
    super.dispose();
  }

  void _saveProfile() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);
    final auth = Provider.of<AuthProvider>(context, listen: false);

    try {
      // Send profile update request to backend (or simulate success)
      final success = await auth.updateProfile(
        name: _nameController.text.trim(),
        state: _stateController.text.trim(),
        district: _districtController.text.trim(),
        city: _cityController.text.trim(),
        address: _addressController.text.trim(),
        cattleCount: int.tryParse(_cattleController.text) ?? 0,
        landAcres: double.tryParse(_landController.text) ?? 0.0,
      );

      if (success && mounted) {
        setState(() => _isEditing = false);
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Profile updated successfully!')),
        );
      }
    } catch (e) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(e.toString().replaceAll('Exception:', ''))),
      );
    } finally {
      if (mounted) setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final user = Provider.of<AuthProvider>(context).user;

    return LoadingOverlay(
      isLoading: _isLoading,
      message: 'Updating profile...',
      child: Scaffold(
        appBar: AppBar(
          title: Text(l10n.profile),
          actions: [
            IconButton(
              icon: Icon(_isEditing ? Icons.close : Icons.edit),
              onPressed: () {
                setState(() {
                  if (_isEditing) {
                    // reset fields
                    _nameController.text = user?.name ?? '';
                    _stateController.text = user?.state ?? '';
                    _districtController.text = user?.district ?? '';
                    _cityController.text = user?.city ?? '';
                    _cattleController.text = user?.cattleCount?.toString() ?? '0';
                    _landController.text = user?.landAcres?.toString() ?? '0.0';
                    _addressController.text = user?.address ?? '';
                  }
                  _isEditing = !_isEditing;
                });
              },
            ),
          ],
        ),
        body: SingleChildScrollView(
          padding: const EdgeInsets.all(20.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                const SizedBox(height: 10),

                // Avatar / Greeting
                Center(
                  child: Column(
                    children: [
                      const CircleAvatar(
                        radius: 40,
                        backgroundColor: Colors.indigo,
                        child: Text(
                          '🧑‍🌾',
                          style: TextStyle(fontSize: 40),
                        ),
                      ),
                      const SizedBox(height: 12),
                      Text(
                        user?.name ?? '',
                        style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
                      ),
                      Text(
                        'Farmer ID: ${user?.id ?? ''}',
                        style: TextStyle(color: Colors.grey.shade500, fontSize: 13),
                      ),
                    ],
                  ),
                ),
                const SizedBox(height: 30),

                // Forms
                CustomTextField(
                  controller: _nameController,
                  label: l10n.fullName,
                  enabled: _isEditing,
                  prefixIcon: Icons.person_outline,
                  validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _mobileController,
                  label: l10n.mobileNumber,
                  enabled: false, // mobile cannot be edited
                  prefixIcon: Icons.phone_android_outlined,
                ),
                const SizedBox(height: 16),

                Row(
                  children: [
                    Expanded(
                      child: CustomTextField(
                        controller: _stateController,
                        label: l10n.state,
                        enabled: _isEditing,
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: CustomTextField(
                        controller: _districtController,
                        label: l10n.district,
                        enabled: _isEditing,
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),

                Row(
                  children: [
                    Expanded(
                      child: CustomTextField(
                        controller: _cityController,
                        label: l10n.village,
                        enabled: _isEditing,
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: CustomTextField(
                        controller: _cattleController,
                        label: l10n.cattleCount,
                        enabled: _isEditing,
                        keyboardType: TextInputType.number,
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _landController,
                  label: l10n.acresOfLand,
                  enabled: _isEditing,
                  keyboardType: TextInputType.number,
                  validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _addressController,
                  label: l10n.address,
                  enabled: _isEditing,
                  maxLines: 2,
                  validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                ),
                const SizedBox(height: 30),

                if (_isEditing)
                  CustomButton(
                    text: l10n.saveChanges,
                    onPressed: _saveProfile,
                  ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
