import 'package:flutter/material.dart';
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../models/scheme_model.dart';
import '../../core/theme/app_theme.dart';
import 'apply_scheme_screen.dart';

class SchemeDetailScreen extends StatelessWidget {
  final SchemeModel scheme;

  const SchemeDetailScreen({super.key, required this.scheme});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      appBar: AppBar(
        title: Text(scheme.name),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Header Card
            Card(
              elevation: 2,
              shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
              child: Container(
                padding: const EdgeInsets.all(20),
                decoration: BoxDecoration(
                  gradient: LinearGradient(
                    colors: [AppTheme.navy.withOpacity(0.05), Colors.white],
                    begin: Alignment.topCenter,
                    end: Alignment.bottomCenter,
                  ),
                  borderRadius: BorderRadius.circular(16),
                ),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      scheme.name,
                      style: const TextStyle(
                        fontSize: 22,
                        fontWeight: FontWeight.bold,
                        color: AppTheme.navy,
                      ),
                    ),
                    const SizedBox(height: 8),
                    Text(
                      scheme.sponsor,
                      style: TextStyle(
                        fontSize: 14,
                        fontWeight: FontWeight.w600,
                        color: AppTheme.saffron.withOpacity(0.9),
                      ),
                    ),
                    const SizedBox(height: 12),
                    Text(
                      scheme.motive,
                      style: const TextStyle(fontSize: 15, height: 1.4),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 20),

            // Details list
            _buildDetailSection(
              title: l10n.eligibility,
              icon: Icons.check_circle_outline,
              content: scheme.eligibility,
            ),
            const SizedBox(height: 16),

            _buildDetailSection(
              title: 'Benefits & Subsidies',
              icon: Icons.monetization_on_outlined,
              content: scheme.benefits,
            ),
            const SizedBox(height: 16),

            _buildDetailSection(
              title: l10n.description,
              icon: Icons.info_outline,
              content: scheme.description,
            ),
            const SizedBox(height: 20),

            // Requirements Details
            Card(
              elevation: 0,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(12),
                side: BorderSide(color: Colors.grey.shade200),
              ),
              child: Padding(
                padding: const EdgeInsets.all(16.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text(
                      'Verification Requirements',
                      style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                    ),
                    const SizedBox(height: 12),
                    _buildRequirementRow(
                      icon: Icons.sensors,
                      title: 'Required RFID Validations',
                      value: '${scheme.requiredValidations} Scans',
                    ),
                    const Divider(height: 20),
                    _buildRequirementRow(
                      icon: Icons.pets,
                      title: 'Required Minimum Cattle',
                      value: '${scheme.requiredCattleCount} Cows',
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 40),

            // Apply Button
            ElevatedButton(
              onPressed: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (_) => ApplySchemeScreen(scheme: scheme),
                  ),
                );
              },
              child: Text(l10n.applyNow.toUpperCase()),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildDetailSection({required String title, required IconData icon, required String content}) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          children: [
            Icon(icon, color: AppTheme.navy, size: 20),
            const SizedBox(width: 8),
            Text(
              title,
              style: const TextStyle(
                fontSize: 16,
                fontWeight: FontWeight.bold,
                color: AppTheme.navy,
              ),
            ),
          ],
        ),
        const SizedBox(height: 8),
        Padding(
          padding: const EdgeInsets.only(left: 28.0),
          child: Text(
            content,
            style: const TextStyle(fontSize: 14, height: 1.4, color: Colors.black87),
          ),
        ),
      ],
    );
  }

  Widget _buildRequirementRow({required IconData icon, required String title, required String value}) {
    return Row(
      children: [
        Icon(icon, color: AppTheme.saffron),
        const SizedBox(width: 12),
        Expanded(
          child: Text(
            title,
            style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w500),
          ),
        ),
        Text(
          value,
          style: const TextStyle(fontSize: 14, fontWeight: FontWeight.bold, color: AppTheme.green),
        ),
      ],
    );
  }
}
