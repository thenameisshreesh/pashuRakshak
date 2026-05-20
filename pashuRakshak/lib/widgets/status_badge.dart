import 'package:flutter/material.dart';
import '../core/theme/app_theme.dart';

class StatusBadge extends StatelessWidget {
  final String status;

  const StatusBadge({super.key, required this.status});

  @override
  Widget build(BuildContext context) {
    Color bgColor;
    Color textColor;

    switch (status.toLowerCase()) {
      case 'approved':
      case 'pass':
      case 'matched':
        bgColor = AppTheme.green.withOpacity(0.1);
        textColor = AppTheme.green;
        break;
      case 'rejected':
      case 'fail':
      case 'unmatched':
        bgColor = Colors.red.withOpacity(0.1);
        textColor = Colors.red;
        break;
      case 'pending':
      case 'under_review':
      case 'scheduled':
        bgColor = AppTheme.saffron.withOpacity(0.1);
        textColor = AppTheme.saffron;
        break;
      case 'suspicious':
        bgColor = Colors.orange.withOpacity(0.1);
        textColor = Colors.orange;
        break;
      default:
        bgColor = Colors.grey.withOpacity(0.1);
        textColor = Colors.grey;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(8),
      ),
      child: Text(
        status.toUpperCase(),
        style: TextStyle(
          color: textColor,
          fontSize: 12,
          fontWeight: FontWeight.bold,
          letterSpacing: 0.5,
        ),
      ),
    );
  }
}
