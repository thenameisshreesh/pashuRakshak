import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../providers/auth_provider.dart';
import '../../providers/scheme_provider.dart';
import '../../widgets/status_badge.dart';
import '../../widgets/custom_button.dart';
import '../auth/login_screen.dart';
import '../common/settings_screen.dart';
import '../common/notifications_screen.dart';
import 'apply_scheme_screen.dart';
import 'scheme_detail_screen.dart';

class FarmerDashboard extends StatefulWidget {
  const FarmerDashboard({super.key});

  @override
  State<FarmerDashboard> createState() => _FarmerDashboardState();
}

class _FarmerDashboardState extends State<FarmerDashboard> {
  int _selectedIndex = 0;

  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      Provider.of<SchemeProvider>(context, listen: false).fetchSchemes();
      final auth = Provider.of<AuthProvider>(context, listen: false);
      if (auth.token != null) {
        Provider.of<SchemeProvider>(context, listen: false).fetchMyApplications(auth.token!);
      }
    });
  }

  void _onItemTapped(int index) {
    setState(() {
      _selectedIndex = index;
    });
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final auth = Provider.of<AuthProvider>(context);
    final user = auth.user;

    final List<Widget> pages = [
      _buildHomeTab(user, l10n),
      _buildApplicationsTab(l10n),
      const NotificationsScreen(),
      const SettingsScreen(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: Text(l10n.appTitle),
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            onPressed: () => setState(() => _selectedIndex = 2),
          ),
        ],
      ),
      body: pages[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: _onItemTapped,
        type: BottomNavigationBarType.fixed,
        selectedItemColor: Theme.of(context).primaryColor,
        unselectedItemColor: Colors.grey,
        items: [
          BottomNavigationBarItem(icon: const Icon(Icons.home_outlined), label: l10n.home),
          BottomNavigationBarItem(icon: const Icon(Icons.assignment_outlined), label: l10n.myApplications),
          BottomNavigationBarItem(icon: const Icon(Icons.notifications_outlined), label: l10n.notifications),
          BottomNavigationBarItem(icon: const Icon(Icons.settings_outlined), label: l10n.settings),
        ],
      ),
    );
  }

  Widget _buildHomeTab(user, l10n) {
    final schemeProvider = Provider.of<SchemeProvider>(context);

    return SingleChildScrollView(
      padding: const EdgeInsets.all(20.0),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Welcome Card
          Card(
            color: Colors.orange.shade50,
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Row(
                children: [
                  CircleAvatar(
                    radius: 26,
                    backgroundColor: Theme.of(context).primaryColor,
                    child: const Text('👤', style: TextStyle(fontSize: 24)),
                  ),
                  const SizedBox(width: 16),
                  Expanded(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          '${l10n.welcomeBack},',
                          style: TextStyle(fontSize: 13, color: Colors.grey.shade600),
                        ),
                        Text(
                          user?.name ?? 'Farmer Name',
                          style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
          const SizedBox(height: 20),

          // Stats row
          Text(
            l10n.quickStats,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 10),
          Row(
            children: [
              Expanded(
                child: _buildStatItem('🐄 Registered Cows', '${user?.cattleCount ?? 0}'),
              ),
              const SizedBox(width: 12),
              Expanded(
                child: _buildStatItem('🌾 Acres owned', '${user?.landAcres ?? 0.0} Ac'),
              ),
            ],
          ),
          const SizedBox(height: 24),

          // Active Schemes List
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Text(
                l10n.activeSchemes,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
              TextButton(
                onPressed: () {},
                child: Text(l10n.knowMore),
              ),
            ],
          ),
          const SizedBox(height: 8),

          if (schemeProvider.isLoading)
            const Center(child: CircularProgressIndicator())
          else if (schemeProvider.schemes.isEmpty)
            Center(child: Text(l10n.noSchemesAvailable))
          else
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: schemeProvider.schemes.length,
              itemBuilder: (context, index) {
                final scheme = schemeProvider.schemes[index];
                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  clipBehavior: Clip.antiAlias,
                  child: InkWell(
                    onTap: () {
                      Navigator.push(
                        context,
                        MaterialPageRoute(
                          builder: (_) => SchemeDetailScreen(scheme: scheme),
                        ),
                      );
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            scheme.name,
                            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                          ),
                          const SizedBox(height: 4),
                          Text(
                            'Sponsor: ${scheme.sponsor}',
                            style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
                          ),
                          const SizedBox(height: 8),
                          Text(
                            scheme.motive,
                            maxLines: 2,
                            overflow: TextOverflow.ellipsis,
                            style: const TextStyle(fontSize: 13),
                          ),
                          const SizedBox(height: 14),
                          Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              Text(
                                'Min: ${scheme.requiredCattleCount} cows',
                                style: const TextStyle(fontWeight: FontWeight.w600, fontSize: 13),
                              ),
                              ElevatedButton(
                                style: ElevatedButton.styleFrom(
                                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
                                ),
                                onPressed: () {
                                  Navigator.push(
                                    context,
                                    MaterialPageRoute(
                                      builder: (_) => ApplySchemeScreen(scheme: scheme),
                                    ),
                                  );
                                },
                                child: Text(l10n.applyNow),
                              ),
                            ],
                          ),
                        ],
                      ),
                    ),
                  ),
                );
              },
            ),
        ],
      ),
    );
  }

  Widget _buildStatItem(String label, String value) {
    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(color: Colors.grey.shade200),
      ),
      child: Padding(
        padding: const EdgeInsets.symmetric(vertical: 16.0, horizontal: 12.0),
        child: Column(
          children: [
            Text(label, style: TextStyle(fontSize: 12, color: Colors.grey.shade600)),
            const SizedBox(height: 6),
            Text(value, style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  Widget _buildApplicationsTab(l10n) {
    final schemeProvider = Provider.of<SchemeProvider>(context);

    if (schemeProvider.isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (schemeProvider.myApplications.isEmpty) {
      return Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            const Text('📋', style: TextStyle(fontSize: 48)),
            const SizedBox(height: 10),
            Text(l10n.noApplications),
          ],
        ),
      );
    }

    return ListView.builder(
      padding: const EdgeInsets.all(20.0),
      itemCount: schemeProvider.myApplications.length,
      itemBuilder: (context, index) {
        final app = schemeProvider.myApplications[index];
        return Card(
          margin: const EdgeInsets.only(bottom: 16),
          child: Padding(
            padding: const EdgeInsets.all(16.0),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Expanded(
                      child: Text(
                        app.schemeName,
                        style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                    ),
                    StatusBadge(status: app.status),
                  ],
                ),
                const Divider(height: 24),
                Text('Application ID: ${app.id}', style: const TextStyle(fontFamily: 'monospace', fontSize: 11)),
                const SizedBox(height: 6),
                Text('Registered Cattle: ${app.step1Data['cattle_count'] ?? 0} cows'),
                Text('Aadhaar Number: ${app.step2Data['aadhaar'] ?? 'N/A'}'),
                if (app.rfidTagsAllocated > 0) ...[
                  const SizedBox(height: 8),
                  Container(
                    padding: const EdgeInsets.all(8),
                    decoration: BoxDecoration(
                      color: Colors.green.shade50,
                      borderRadius: BorderRadius.circular(6),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.sensors, color: Colors.green, size: 18),
                        const SizedBox(width: 8),
                        Text(
                          '${app.rfidTagsAllocated} RFID tags allocated and secured.',
                          style: TextStyle(color: Colors.green.shade700, fontSize: 12),
                        ),
                      ],
                    ),
                  ),
                ],
                if (app.status == 'rejected' && app.rejectionReason != null) ...[
                  const SizedBox(height: 12),
                  Container(
                    padding: const EdgeInsets.all(10),
                    decoration: BoxDecoration(
                      color: Colors.red.shade50,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Text('Rejection Details:', style: TextStyle(fontWeight: FontWeight.bold, color: Colors.red)),
                        Text('Reason: ${app.rejectionReason}', style: const TextStyle(color: Colors.red)),
                        if (app.rejectionNotes != null && app.rejectionNotes!.isNotEmpty)
                          Text('Notes: ${app.rejectionNotes}', style: const TextStyle(color: Colors.red)),
                      ],
                    ),
                  ),
                ],
              ],
            ),
          ),
        );
      },
    );
  }
}
