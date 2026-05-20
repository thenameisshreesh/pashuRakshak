import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../providers/auth_provider.dart';
import '../../providers/language_provider.dart';
import '../../widgets/custom_button.dart';
import '../../widgets/custom_text_field.dart';
import '../farmer/farmer_dashboard.dart';
import '../officer/officer_dashboard.dart';
import 'register_screen.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});

  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _farmerFormKey = GlobalKey<FormState>();
  final _officerFormKey = GlobalKey<FormState>();

  final _mobileController = TextEditingController();
  final _usernameController = TextEditingController();
  final _passwordController = TextEditingController();

  String _errorMessage = '';

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
  }

  @override
  void dispose() {
    _tabController.dispose();
    _mobileController.dispose();
    _usernameController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _handleLogin() async {
    setState(() {
      _errorMessage = '';
    });

    final authProvider = Provider.of<AuthProvider>(context, listen: false);
    bool success = false;

    try {
      if (_tabController.index == 0) {
        if (!_farmerFormKey.currentState!.validate()) return;
        success = await authProvider.login(
          mobile: _mobileController.text.trim(),
          password: _passwordController.text,
        );
      } else {
        if (!_officerFormKey.currentState!.validate()) return;
        success = await authProvider.login(
          username: _usernameController.text.trim().toLowerCase(),
          password: _passwordController.text,
        );
      }

      if (success && mounted) {
        final role = authProvider.user?.role ?? 'farmer';
        if (role == 'officer' || role == 'admin') {
          Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const OfficerDashboard()));
        } else {
          Navigator.pushReplacement(context, MaterialPageRoute(builder: (_) => const FarmerDashboard()));
        }
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
    final langProvider = Provider.of<LanguageProvider>(context);

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
        actions: [
          PopupMenuButton<Locale>(
            icon: const Icon(Icons.language),
            onSelected: (locale) => langProvider.changeLanguage(locale),
            itemBuilder: (context) => [
              PopupMenuItem(value: const Locale('en'), child: Text(l10n.english)),
              PopupMenuItem(value: const Locale('hi'), child: Text(l10n.hindi)),
              PopupMenuItem(value: const Locale('mr'), child: Text(l10n.marathi)),
            ],
          ),
        ],
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 16.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.center,
            children: [
              const SizedBox(height: 20),
              // Emblem or Logo
              Container(
                height: 100,
                width: 100,
                decoration: BoxDecoration(
                  color: Colors.orange.shade50,
                  shape: BoxShape.circle,
                ),
                child: const Center(
                  child: Text('🐄', style: TextStyle(fontSize: 48)),
                ),
              ),
              const SizedBox(height: 16),
              Text(
                l10n.govtOfIndia,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              Text(
                l10n.smartLivestock,
                textAlign: TextAlign.center,
                style: TextStyle(color: Colors.grey.shade600, fontSize: 13),
              ),
              const SizedBox(height: 30),

              // TabBar for Dual Login
              Container(
                decoration: BoxDecoration(
                  color: Colors.grey.shade100,
                  borderRadius: BorderRadius.circular(12),
                ),
                child: TabBar(
                  controller: _tabController,
                  indicator: BoxDecoration(
                    color: Theme.of(context).primaryColor,
                    borderRadius: BorderRadius.circular(10),
                  ),
                  labelColor: Colors.white,
                  unselectedLabelColor: Colors.grey.shade600,
                  tabs: const [
                    Tab(text: 'Farmer / पशुपालक'),
                    Tab(text: 'Inspector / अधिकारी'),
                  ],
                ),
              ),
              const SizedBox(height: 24),

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

              // TabView Content
              SizedBox(
                height: 220,
                child: TabBarView(
                  controller: _tabController,
                  physics: const NeverScrollableScrollPhysics(),
                  children: [
                    // Farmer Form
                    Form(
                      key: _farmerFormKey,
                      child: Column(
                        children: [
                          CustomTextField(
                            controller: _mobileController,
                            label: l10n.mobileNumber,
                            hint: l10n.enterMobileNumber,
                            keyboardType: TextInputType.phone,
                            prefixIcon: Icons.phone_android,
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
                            hint: l10n.enterPassword,
                            isPassword: true,
                            prefixIcon: Icons.lock_outline,
                            validator: (val) {
                              if (val == null || val.isEmpty) return l10n.fieldRequired;
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),

                    // Officer Form
                    Form(
                      key: _officerFormKey,
                      child: Column(
                        children: [
                          CustomTextField(
                            controller: _usernameController,
                            label: 'Username',
                            hint: 'Enter official username',
                            prefixIcon: Icons.account_circle_outlined,
                            validator: (val) {
                              if (val == null || val.isEmpty) return l10n.fieldRequired;
                              return null;
                            },
                          ),
                          const SizedBox(height: 16),
                          CustomTextField(
                            controller: _passwordController,
                            label: l10n.password,
                            hint: l10n.enterPassword,
                            isPassword: true,
                            prefixIcon: Icons.lock_outline,
                            validator: (val) {
                              if (val == null || val.isEmpty) return l10n.fieldRequired;
                              return null;
                            },
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              Consumer<AuthProvider>(
                builder: (context, auth, _) => CustomButton(
                  text: l10n.login,
                  isLoading: auth.isLoading,
                  onPressed: _handleLogin,
                ),
              ),

              const SizedBox(height: 24),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Text(l10n.dontHaveAccount),
                  TextButton(
                    onPressed: () {
                      Navigator.push(context, MaterialPageRoute(builder: (_) => const RegisterScreen()));
                    },
                    child: Text(l10n.register),
                  ),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
