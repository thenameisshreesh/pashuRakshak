import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../core/constants/api_constants.dart';
import '../../providers/auth_provider.dart';
import '../../widgets/status_badge.dart';
import '../common/settings_screen.dart';
import 'scan_tags_screen.dart';

class OfficerDashboard extends StatefulWidget {
  const OfficerDashboard({super.key});

  @override
  State<OfficerDashboard> createState() => _OfficerDashboardState();
}

class _OfficerDashboardState extends State<OfficerDashboard> {
  int _selectedIndex = 0;
  List<dynamic> _raids = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _fetchRaids();
  }

  Future<void> _fetchRaids() async {
    setState(() => _isLoading = true);
    final auth = Provider.of<AuthProvider>(context, listen: false);

    try {
      final response = await http.get(
        Uri.parse('${ApiConstants.baseUrl}/raids'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${auth.token}',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        setState(() {
          _raids = data['raids'] ?? data['data'] ?? data;
        });
      }
    } catch (e) {
      // Mock Fallback
      setState(() {
        _raids = [
          {
            '_id': 'r1',
            'farmer_name': 'Ramesh Patil',
            'farmer_mobile': '9876543210',
            'scheme_name': 'Rashtriya Gokul Mission',
            'officer_name': auth.user?.name ?? 'Gov Officer',
            'date': '2026-05-25',
            'time': '10:00',
            'status': 'scheduled'
          },
          {
            '_id': 'r2',
            'farmer_name': 'Sanjay Pawar',
            'farmer_mobile': '9876543211',
            'scheme_name': 'Gaushala Dev Grant',
            'officer_name': auth.user?.name ?? 'Gov Officer',
            'date': '2026-05-26',
            'time': '14:30',
            'status': 'scheduled'
          }
        ];
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;
    final auth = Provider.of<AuthProvider>(context);
    final user = auth.user;

    final List<Widget> pages = [
      _buildRaidsTab(l10n),
      const SettingsScreen(),
    ];

    return Scaffold(
      appBar: AppBar(
        title: const Text('PashuRakshak - Official'),
      ),
      body: pages[_selectedIndex],
      bottomNavigationBar: BottomNavigationBar(
        currentIndex: _selectedIndex,
        onTap: (idx) => setState(() => _selectedIndex = idx),
        selectedItemColor: Theme.of(context).primaryColor,
        items: [
          const BottomNavigationBarItem(icon: Icon(Icons.assignment_turned_in_outlined), label: 'Audits'),
          BottomNavigationBarItem(icon: const Icon(Icons.settings_outlined), label: l10n.settings),
        ],
      ),
    );
  }

  Widget _buildRaidsTab(l10n) {
    return RefreshIndicator(
      onRefresh: _fetchRaids,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Surprise Inspections Dashboard',
              style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
            ),
            const SizedBox(height: 6),
            const Text(
              'Verify cattle counts on-site using standard RFID readers.',
              style: TextStyle(color: Colors.grey, fontSize: 13),
            ),
            const SizedBox(height: 20),

            Expanded(
              child: _isLoading
                  ? const Center(child: CircularProgressIndicator())
                  : _raids.isEmpty
                      ? const Center(child: Text('No audits scheduled.'))
                      : ListView.builder(
                          itemCount: _raids.length,
                          itemBuilder: (context, index) {
                            final raid = _raids[index];
                            return Card(
                              margin: const EdgeInsets.only(bottom: 12),
                              child: Padding(
                                padding: const EdgeInsets.all(16.0),
                                child: Column(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Row(
                                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                      children: [
                                        Text(
                                          raid['farmer_name'] ?? 'Farmer',
                                          style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                                        ),
                                        StatusBadge(status: raid['status'] ?? 'scheduled'),
                                      ],
                                    ),
                                    const SizedBox(height: 6),
                                    Text('Scheme: ${raid['scheme_name'] ?? ''}', style: const TextStyle(fontSize: 13)),
                                    Text('Time: ${raid['date']} at ${raid['time']}', style: const TextStyle(fontSize: 13, color: Colors.grey)),
                                    const Divider(height: 20),
                                    SizedBox(
                                      width: double.infinity,
                                      child: ElevatedButton.icon(
                                        style: ElevatedButton.styleFrom(
                                          backgroundColor: Theme.of(context).primaryColor,
                                        ),
                                        onPressed: () {
                                          Navigator.push(
                                            context,
                                            MaterialPageRoute(
                                              builder: (_) => ScanTagsScreen(raidId: raid['_id']),
                                            ),
                                          );
                                        },
                                        icon: const Icon(Icons.sensors, color: Colors.white),
                                        label: const Text('Start Mobile RFID Scan Gate', style: TextStyle(color: Colors.white)),
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
            ),
          ],
        ),
      ),
    );
  }
}
