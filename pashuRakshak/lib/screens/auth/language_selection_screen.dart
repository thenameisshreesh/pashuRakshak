import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../providers/language_provider.dart';
import '../../core/theme/app_theme.dart';
import 'login_screen.dart';

class LanguageSelectionScreen extends StatelessWidget {
  const LanguageSelectionScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final langProvider = Provider.of<LanguageProvider>(context);

    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24.0, vertical: 40.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Spacer(flex: 2),
              // Logo/Icon
              Center(
                child: Container(
                  height: 120,
                  width: 120,
                  decoration: BoxDecoration(
                    color: Colors.orange.shade50,
                    shape: BoxShape.circle,
                  ),
                  child: const Center(
                    child: Text('🐄', style: TextStyle(fontSize: 64)),
                  ),
                ),
              ),
              const SizedBox(height: 24),
              const Text(
                'PashuRakshak',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 32,
                  fontWeight: FontWeight.bold,
                  color: AppTheme.navy,
                ),
              ),
              const SizedBox(height: 8),
              Text(
                'Smart Livestock Verification & Grant Monitoring\nपशु सत्यापन एवं अनुदान निगरानी प्रणाली',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 14,
                  color: Colors.grey.shade600,
                  height: 1.4,
                ),
              ),
              const Spacer(flex: 1),
              const Text(
                'Please Select Language / भाषा चुनें',
                textAlign: TextAlign.center,
                style: TextStyle(
                  fontSize: 18,
                  fontWeight: FontWeight.w600,
                ),
              ),
              const SizedBox(height: 20),
              
              // Language Option Cards
              _buildLanguageCard(
                context,
                title: 'English',
                subtitle: 'Smart Livestock Verification',
                locale: const Locale('en'),
                currentLocale: langProvider.appLocale,
                onTap: () {
                  langProvider.changeLanguage(const Locale('en'));
                },
              ),
              const SizedBox(height: 12),
              _buildLanguageCard(
                context,
                title: 'हिन्दी',
                subtitle: 'स्मार्ट पशु सत्यापन प्रणाली',
                locale: const Locale('hi'),
                currentLocale: langProvider.appLocale,
                onTap: () {
                  langProvider.changeLanguage(const Locale('hi'));
                },
              ),
              const SizedBox(height: 12),
              _buildLanguageCard(
                context,
                title: 'मराठी',
                subtitle: 'स्मार्ट पशु पडताळणी प्रणाली',
                locale: const Locale('mr'),
                currentLocale: langProvider.appLocale,
                onTap: () {
                  langProvider.changeLanguage(const Locale('mr'));
                },
              ),
              
              const Spacer(flex: 2),
              
              ElevatedButton(
                onPressed: () {
                  Navigator.pushReplacement(
                    context,
                    MaterialPageRoute(builder: (_) => const LoginScreen()),
                  );
                },
                child: const Text('GET STARTED / शुरू करें'),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildLanguageCard(
    BuildContext context, {
    required String title,
    required String subtitle,
    required Locale locale,
    required Locale currentLocale,
    required VoidCallback onTap,
  }) {
    final isSelected = currentLocale.languageCode == locale.languageCode;
    final theme = Theme.of(context);

    return Card(
      elevation: isSelected ? 4 : 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(16),
        side: BorderSide(
          color: isSelected ? AppTheme.saffron : Colors.grey.shade200,
          width: isSelected ? 2.0 : 1.0,
        ),
      ),
      color: isSelected ? Colors.orange.shade50.withOpacity(0.2) : Colors.white,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(16),
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 20.0, vertical: 16.0),
          child: Row(
            children: [
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      title,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: isSelected ? AppTheme.navy : Colors.black87,
                      ),
                    ),
                    const SizedBox(height: 4),
                    Text(
                      subtitle,
                      style: TextStyle(
                        fontSize: 12,
                        color: Colors.grey.shade500,
                      ),
                    ),
                  ],
                ),
              ),
              if (isSelected)
                const Icon(
                  Icons.check_circle,
                  color: AppTheme.saffron,
                  size: 28,
                )
              else
                Icon(
                  Icons.circle_outlined,
                  color: Colors.grey.shade300,
                  size: 28,
                ),
            ],
          ),
        ),
      ),
    );
  }
}
