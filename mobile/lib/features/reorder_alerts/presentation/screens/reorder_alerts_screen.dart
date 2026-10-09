import 'package:flutter/material.dart';

class ReorderAlertsScreen extends StatelessWidget {
  const ReorderAlertsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Smart Reorder Alerts'),
      ),
      body: ListView.builder(
        itemCount: 5,
        padding: const EdgeInsets.all(16),
        itemBuilder: (context, index) {
          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            child: Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Coca Cola 1.5L',
                        style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                      ),
                      Icon(Icons.warning, color: Colors.red),
                    ],
                  ),
                  const SizedBox(height: 8),
                  const Text('Current Stock: 10'),
                  const Text('Safety Threshold: 50'),
                  const Text('Deficit: 40', style: TextStyle(color: Colors.red)),
                  const SizedBox(height: 12),
                  SizedBox(
                    width: double.infinity,
                    child: ElevatedButton(
                      onPressed: () {},
                      child: const Text('Quick Reorder'),
                    ),
                  ),
                ],
              ),
            ),
          );
        },
      ),
    );
  }
}
