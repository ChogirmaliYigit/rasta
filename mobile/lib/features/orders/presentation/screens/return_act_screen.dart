import 'package:flutter/material.dart';
import 'package:image_picker/image_picker.dart';
import 'dart:io';

class ReturnActScreen extends StatefulWidget {
  final String id;
  const ReturnActScreen({super.key, required this.id});

  @override
  State<ReturnActScreen> createState() => _ReturnActScreenState();
}

class _ReturnActScreenState extends State<ReturnActScreen> {
  final List<File> _photos = [];
  final ImagePicker _picker = ImagePicker();

  Future<void> _takePhoto() async {
    final XFile? photo = await _picker.pickImage(source: ImageSource.camera);
    if (photo != null) {
      setState(() {
        _photos.add(File(photo.path));
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Return / Report Issue'),
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Order #ORD-2026-${widget.id}', style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18)),
            const SizedBox(height: 16),
            const Text('Select items to return:'),
            const SizedBox(height: 8),
            ListView.builder(
              shrinkWrap: true,
              physics: const NeverScrollableScrollPhysics(),
              itemCount: 2,
              itemBuilder: (context, index) {
                return Card(
                  child: Padding(
                    padding: const EdgeInsets.all(8.0),
                    child: Column(
                      children: [
                        CheckboxListTile(
                          title: const Text('Coca Cola 1.5L (Delivered: 10)'),
                          value: index == 0,
                          onChanged: (v) {},
                        ),
                        if (index == 0)
                          Padding(
                            padding: const EdgeInsets.symmetric(horizontal: 16.0),
                            child: Column(
                              children: [
                                Row(
                                  children: [
                                    const Text('Return Qty: '),
                                    IconButton(icon: const Icon(Icons.remove), onPressed: () {}),
                                    const Text('2'),
                                    IconButton(icon: const Icon(Icons.add), onPressed: () {}),
                                  ],
                                ),
                                TextField(
                                  decoration: InputDecoration(
                                    hintText: 'Reason for this item',
                                    border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                                  ),
                                ),
                              ],
                            ),
                          ),
                      ],
                    ),
                  ),
                );
              },
            ),
            const SizedBox(height: 16),
            TextField(
              maxLines: 3,
              decoration: InputDecoration(
                labelText: 'General Reason / Comments',
                border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
              ),
            ),
            const SizedBox(height: 16),
            const Text('Photos (Proof of damage/issue):', style: TextStyle(fontWeight: FontWeight.bold)),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (var photo in _photos)
                  Stack(
                    alignment: Alignment.topRight,
                    children: [
                      Image.file(photo, width: 80, height: 80, fit: BoxFit.cover),
                      IconButton(
                        icon: const Icon(Icons.close, color: Colors.white, shadows: [Shadow(blurRadius: 2, color: Colors.black)]),
                        onPressed: () {
                          setState(() {
                            _photos.remove(photo);
                          });
                        },
                      ),
                    ],
                  ),
                InkWell(
                  onTap: _takePhoto,
                  child: Container(
                    width: 80,
                    height: 80,
                    color: Colors.grey[200],
                    child: const Icon(Icons.camera_alt, color: Colors.grey),
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
      bottomNavigationBar: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(16.0),
          child: ElevatedButton(
            onPressed: () {
              showDialog(
                context: context,
                builder: (context) => AlertDialog(
                  title: const Text('Confirm Return Act'),
                  content: const Text('Are you sure you want to submit this return act?'),
                  actions: [
                    TextButton(
                      onPressed: () => Navigator.pop(context),
                      child: const Text('Cancel'),
                    ),
                    ElevatedButton(
                      onPressed: () {
                        Navigator.pop(context);
                        Navigator.pop(context); // Go back to order detail
                      },
                      child: const Text('Submit'),
                    ),
                  ],
                ),
              );
            },
            child: const Text('Submit Return Act'),
          ),
        ),
      ),
    );
  }
}
