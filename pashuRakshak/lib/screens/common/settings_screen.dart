import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../providers/auth_provider.dart';
import '../../providers/language_provider.dart';
import '../../providers/theme_provider.dart';
import '../auth/login_screen.dart';
import '../farmer/profile_screen.dart';

class SettingsScreen extends StatelessWidget {
  const SettingsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final auth = Provider.of<AuthProvider>(context);
    final langProvider = Provider.of<LanguageProvider>(context);

    return Scaffold(
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'App settings & Language / सेटिंग्स',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 20),

            // Language Selector Card
            Card(
              child: ListTile(
                leading: const Icon(Icons.translate),
                title: Text(l10n.changeLanguage),
                trailing: DropdownButton<Locale>(
                  value: langProvider.appLocale,
                  underline: const SizedBox(),
                  onChanged: (Locale? newLocale) {
                    if (newLocale != null) {
                      langProvider.changeLanguage(newLocale);
                    }
                  },
                  items: [
                    DropdownMenuItem(value: const Locale('en'), child: Text(l10n.english)),
                    DropdownMenuItem(value: const Locale('hi'), child: Text(l10n.hindi)),
                    DropdownMenuItem(value: const Locale('mr'), child: Text(l10n.marathi)),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 12),

            // Profile Card
            Card(
              child: ListTile(
                leading: const Icon(Icons.person_outline),
                title: Text(l10n.profile),
                trailing: const Icon(Icons.chevron_right),
                onTap: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (_) => const ProfileScreen()),
                  );
                },
              ),
            ),
            const SizedBox(height: 12),

            // Dark Mode Toggle
            Consumer<ThemeProvider>(
              builder: (context, themeProvider, _) => Card(
                child: SwitchListTile(
                  value: themeProvider.isDarkMode,
                  onChanged: (val) {
                    themeProvider.toggleTheme(val);
                  },
                  secondary: const Icon(Icons.dark_mode_outlined),
                  title: Text(l10n.darkMode),
                ),
              ),
            ),
            const SizedBox(height: 12),

            // Version info
            Card(
              child: ListTile(
                leading: const Icon(Icons.info_outline),
                title: Text(l10n.about),
                subtitle: Text('${l10n.version}: 1.0.0'),
              ),
            ),
            const SizedBox(height: 24),

            // Logout button
            SizedBox(
              width: double.infinity,
              height: 50,
              child: OutlinedButton.icon(
                style: OutlinedButton.styleFrom(
                  side: const BorderSide(color: Colors.red),
                  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(12)),
                ),
                onPressed: () async {
                  await auth.logout();
                  if (context.mounted) {
                    Navigator.pushAndRemoveUntil(
                      context,
                      MaterialPageRoute(builder: (_) => const LoginScreen()),
                      (route) => false,
                    );
                  }
                },
                icon: const Icon(Icons.logout, color: Colors.red),
                label: Text(l10n.logout, style: const TextStyle(color: Colors.red, fontWeight: FontWeight.bold)),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
