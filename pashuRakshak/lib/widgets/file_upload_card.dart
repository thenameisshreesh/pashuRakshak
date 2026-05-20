import 'dart:io';
import 'package:flutter/material.dart';

class FileUploadCard extends StatelessWidget {
  final String title;
  final String subtitle;
  final File? file;
  final VoidCallback onTap;
  final VoidCallback? onClear;

  const FileUploadCard({
    super.key,
    required this.title,
    required this.subtitle,
    required this.file,
    required this.onTap,
    this.onClear,
  });

  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final isUploaded = file != null;

    return Card(
      elevation: 0,
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(12),
        side: BorderSide(
          color: isUploaded ? theme.colorScheme.tertiary.withOpacity(0.3) : Colors.grey.shade200,
          width: isUploaded ? 1.5 : 1.0,
        ),
      ),
      color: isUploaded ? theme.colorScheme.tertiary.withOpacity(0.02) : Colors.white,
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              title,
              style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 14),
            ),
            const SizedBox(height: 4),
            Text(
              subtitle,
              style: TextStyle(color: Colors.grey.shade500, fontSize: 12),
            ),
            const SizedBox(height: 12),
            InkWell(
              onTap: onTap,
              borderRadius: BorderRadius.circular(8),
              child: Container(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 14),
                decoration: BoxDecoration(
                  color: Colors.grey.shade50,
                  border: Border.all(color: Colors.grey.shade200),
                  borderRadius: BorderRadius.circular(8),
                ),
                child: Row(
                  children: [
                    Icon(
                      isUploaded ? Icons.insert_drive_file : Icons.cloud_upload_outlined,
                      color: isUploaded ? theme.colorScheme.tertiary : Colors.grey,
                    ),
                    const SizedBox(width: 12),
                    Expanded(
                      child: Text(
                        isUploaded 
                            ? file!.path.split('/').last.split('\\').last 
                            : 'Choose file to upload',
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                        style: TextStyle(
                          color: isUploaded ? Colors.black87 : Colors.grey.shade600,
                          fontSize: 13,
                          fontWeight: isUploaded ? FontWeight.w500 : FontWeight.normal,
                        ),
                      ),
                    ),
                    if (isUploaded) ...[
                      const Icon(Icons.check_circle, color: Colors.green, size: 20),
                      if (onClear != null) ...[
                        const SizedBox(width: 8),
                        GestureDetector(
                          onTap: onClear,
                          child: const Icon(Icons.cancel, color: Colors.red, size: 20),
                        ),
                      ],
                    ],
                  ],
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
