import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:http/http.dart' as http;
import 'package:pashu_rakshak/l10n/app_localizations.dart';
import '../../core/constants/api_constants.dart';
import '../../providers/auth_provider.dart';
import '../../models/notification_model.dart';

class NotificationsScreen extends StatefulWidget {
  const NotificationsScreen({super.key});

  @override
  State<NotificationsScreen> createState() => _NotificationsScreenState();
}

class _NotificationsScreenState extends State<NotificationsScreen> {
  List<NotificationModel> _notifications = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _fetchNotifications();
  }

  Future<void> _fetchNotifications() async {
    setState(() => _isLoading = true);
    final auth = Provider.of<AuthProvider>(context, listen: false);

    try {
      final response = await http.get(
        Uri.parse('${ApiConstants.baseUrl}/notifications'),
        headers: {
          'Content-Type': 'application/json',
          'Authorization': 'Bearer ${auth.token}',
        },
      );

      if (response.statusCode == 200) {
        final data = json.decode(response.body);
        final List<dynamic> list = data['notifications'] ?? data['data'] ?? data;
        setState(() {
          _notifications = list.map((item) => NotificationModel.fromJson(item)).toList();
        });
      }
    } catch (e) {
      // Mock Fallback
      setState(() {
        _notifications = [
          NotificationModel(
            id: 'n1',
            title: '🚨 Surprise Inspection Scheduled',
            body: 'Surprise audit scheduled for your farm on 2026-05-25 at 10:00. Please ensure all cows are present inside the RFID boundary.',
            read: false,
            createdAt: DateTime.now(),
            type: 'alert',
          ),
          NotificationModel(
            id: 'n2',
            title: '✓ Application Submitted',
            body: 'Your application under Rashtriya Gokul Mission is pending verification by the district officer.',
            read: true,
            createdAt: DateTime.now().subtract(const Duration(days: 1)),
            type: 'info',
          ),
        ];
      });
    } finally {
      setState(() => _isLoading = false);
    }
  }

  @override
  Widget build(BuildContext context) {
    final l10n = AppLocalizations.of(context)!;

    return Scaffold(
      body: RefreshIndicator(
        onRefresh: _fetchNotifications,
        child: Padding(
          padding: const EdgeInsets.all(20.0),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                l10n.notifications,
                style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
              ),
              const SizedBox(height: 20),

              Expanded(
                child: _isLoading
                    ? const Center(child: CircularProgressIndicator())
                    : _notifications.isEmpty
                        ? Center(child: Text(l10n.noNotifications))
                        : ListView.builder(
                            itemCount: _notifications.length,
                            itemBuilder: (context, index) {
                              final notif = _notifications[index];
                              final bool isUnread = !notif.read;

                              return Card(
                                color: isUnread ? Colors.orange.shade50 : null,
                                margin: const EdgeInsets.only(bottom: 12),
                                child: ListTile(
                                  leading: const Icon(Icons.info_outline),
                                  title: Text(
                                    notif.title,
                                    style: TextStyle(
                                      fontWeight: isUnread ? FontWeight.bold : FontWeight.normal,
                                    ),
                                  ),
                                  subtitle: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      const SizedBox(height: 4),
                                      Text(notif.body),
                                      const SizedBox(height: 6),
                                      Text(
                                        notif.createdAt.toIso8601String().split('T').first,
                                        style: TextStyle(color: Colors.grey.shade400, fontSize: 11),
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
      ),
    );
  }
}
