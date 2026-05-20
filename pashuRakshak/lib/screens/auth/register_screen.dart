import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/custom_button.dart';
import '../../widgets/custom_text_field.dart';
import '../farmer/farmer_dashboard.dart';

class RegisterScreen extends StatefulWidget {
  const RegisterScreen({super.key});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();

  final _nameController = TextEditingController();
  final _mobileController = TextEditingController();
  final _passwordController = TextEditingController();
  final _stateController = TextEditingController();
  final _districtController = TextEditingController();
  final _cityController = TextEditingController();
  final _addressController = TextEditingController();
  final _cattleController = TextEditingController();
  final _landController = TextEditingController();
  final _aadhaarController = TextEditingController();

  String _errorMessage = '';

  @override
  void dispose() {
    _nameController.dispose();
    _mobileController.dispose();
    _passwordController.dispose();
    _stateController.dispose();
    _districtController.dispose();
    _cityController.dispose();
    _addressController.dispose();
    _cattleController.dispose();
    _landController.dispose();
    _aadhaarController.dispose();
    super.dispose();
  }

  void _handleRegister() async {
    setState(() {
      _errorMessage = '';
    });

    if (!_formKey.currentState!.validate()) return;

    final authProvider = Provider.of<AuthProvider>(context, listen: false);

    try {
      final success = await authProvider.registerFarmer(
        name: _nameController.text.trim(),
        mobile: _mobileController.text.trim(),
        password: _passwordController.text,
        state: _stateController.text.trim(),
        district: _districtController.text.trim(),
        city: _cityController.text.trim(),
        address: _addressController.text.trim(),
        cattleCount: int.tryParse(_cattleController.text) ?? 0,
        landAcres: double.tryParse(_landController.text) ?? 0.0,
        aadhaar: _aadhaarController.text.trim(),
      );

      if (success && mounted) {
        Navigator.pushAndRemoveUntil(
          context,
          MaterialPageRoute(builder: (_) => const FarmerDashboard()),
          (route) => false,
        );
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception:', '').trim();
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.createAccount),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                if (_errorMessage.isNotEmpty)
                  Container(
                    padding: const EdgeInsets.all(12),
                    margin: const EdgeInsets.only(bottom: 16),
                    decoration: BoxDecoration(
                      color: Colors.red.shade50,
                      borderRadius: BorderRadius.circular(8),
                      border: Border.all(color: Colors.red.shade200),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.error_outline, color: Colors.red),
                        const SizedBox(width: 8),
                        Expanded(
                          child: Text(
                            _errorMessage,
                            style: const TextStyle(color: Colors.red),
                          ),
                        ),
                      ],
                    ),
                  ),

                CustomTextField(
                  controller: _nameController,
                  label: l10n.fullName,
                  hint: 'Enter your full name',
                  prefixIcon: Icons.person_outline,
                  validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _mobileController,
                  label: l10n.mobileNumber,
                  hint: l10n.enterMobileNumber,
                  keyboardType: TextInputType.phone,
                  prefixIcon: Icons.phone_android_outlined,
                  validator: (val) {
                    if (val == null || val.isEmpty) return l10n.fieldRequired;
                    if (val.length != 10) return l10n.invalidMobile;
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _passwordController,
                  label: l10n.password,
                  hint: 'Min 6 characters',
                  isPassword: true,
                  prefixIcon: Icons.lock_outline,
                  validator: (val) {
                    if (val == null || val.isEmpty) return l10n.fieldRequired;
                    if (val.length < 6) return l10n.passwordTooShort;
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                Row(
                  children: [
                    Expanded(
                      child: CustomTextField(
                        controller: _stateController,
                        label: l10n.state,
                        hint: 'e.g. Maharashtra',
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: CustomTextField(
                        controller: _districtController,
                        label: l10n.district,
                        hint: 'e.g. Pune',
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
                        hint: 'Village/City name',
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: CustomTextField(
                        controller: _cattleController,
                        label: l10n.cattleCount,
                        hint: '0',
                        keyboardType: TextInputType.number,
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
                        controller: _landController,
                        label: l10n.acresOfLand,
                        hint: 'Acres (e.g. 2.5)',
                        keyboardType: TextInputType.numberWithOptions(decimal: true),
                        validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                      ),
                    ),
                    const SizedBox(width: 16),
                    Expanded(
                      child: CustomTextField(
                        controller: _aadhaarController,
                        label: 'Aadhaar Card No',
                        hint: '12-digit number',
                        keyboardType: TextInputType.number,
                        validator: (val) {
                          if (val == null || val.isEmpty) return l10n.fieldRequired;
                          if (val.length != 12) return 'Enter a valid 12-digit Aadhaar';
                          return null;
                        },
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _addressController,
                  label: l10n.address,
                  hint: 'Village address details',
                  validator: (val) => val == null || val.isEmpty ? l10n.fieldRequired : null,
                ),
                const SizedBox(height: 30),

                Consumer<AuthProvider>(
                  builder: (context, auth, _) => CustomButton(
                    text: l10n.register,
                    isLoading: auth.isLoading,
                    onPressed: _handleRegister,
                  ),
                ),
                const SizedBox(height: 16),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
