import 'package:flutter/material.dart';
import 'package:mobile_scanner/mobile_scanner.dart';

class POSSaleScreen extends StatefulWidget {
  const POSSaleScreen({super.key});

  @override
  State<POSSaleScreen> createState() => _POSSaleScreenState();
}

class _POSSaleScreenState extends State<POSSaleScreen> {
  bool isScanMode = false;
  final List<String> sessionSales = []; // Mock list

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('POS Sale Entry'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16.0),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Text('Manual'),
                Switch(
                  value: isScanMode,
                  onChanged: (v) => setState(() => isScanMode = v),
                ),
                const Text('Scan Barcode'),
              ],
            ),
          ),
          if (isScanMode)
            Expanded(
              child: MobileScanner(
                onDetect: (capture) {
                  final List<Barcode> barcodes = capture.barcodes;
                  for (final barcode in barcodes) {
                    debugPrint('Barcode found! ${barcode.rawValue}');
                    // Show confirmation dialog with qty stepper
                  }
                },
              ),
            )
          else
            Expanded(
              child: Column(
                children: [
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 16.0),
                    child: TextField(
                      decoration: InputDecoration(
                        hintText: 'Search product...',
                        prefixIcon: const Icon(Icons.search),
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(12),
                        ),
                      ),
                    ),
                  ),
                  Expanded(
                    child: ListView.builder(
                      itemCount: 5,
                      itemBuilder: (context, index) {
                        return ListTile(
                          title: const Text('Coca Cola 1.5L'),
                          subtitle: const Text('12,000 UZS - Stock: 150'),
                          trailing: const Icon(Icons.add_shopping_cart),
                          onTap: () {
                            // Show qty dialog
                          },
                        );
                      },
                    ),
                  ),
                ],
              ),
            ),
          const Divider(),
          const Padding(
            padding: EdgeInsets.all(8.0),
            child: Text('Current Session Sales', style: TextStyle(fontWeight: FontWeight.bold)),
          ),
          Expanded(
            child: ListView.builder(
              itemCount: sessionSales.length,
              itemBuilder: (context, index) {
                return ListTile(
                  title: Text(sessionSales[index]),
                );
              },
            ),
          ),
        ],
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: ElevatedButton(
            onPressed: () {},
            child: const Text('Complete Sales Session'),
          ),
        ),
      ),
    );
  }
}
