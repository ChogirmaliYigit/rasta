import 'package:flutter_riverpod/flutter_riverpod.dart';

class CartItem {
  final String productId;
  final String productName;
  final double price;
  final int quantity;
  final String wholesalerBranchId;

  CartItem({
    required this.productId,
    required this.productName,
    required this.price,
    required this.quantity,
    required this.wholesalerBranchId,
  });

  CartItem copyWith({
    String? productId,
    String? productName,
    double? price,
    int? quantity,
    String? wholesalerBranchId,
  }) {
    return CartItem(
      productId: productId ?? this.productId,
      productName: productName ?? this.productName,
      price: price ?? this.price,
      quantity: quantity ?? this.quantity,
      wholesalerBranchId: wholesalerBranchId ?? this.wholesalerBranchId,
    );
  }
}

class CartNotifier extends StateNotifier<List<CartItem>> {
  CartNotifier() : super([]);

  void addItem(CartItem item) {
    final index = state.indexWhere((element) => element.productId == item.productId);
    if (index >= 0) {
      final updated = List<CartItem>.from(state);
      updated[index] = updated[index].copyWith(quantity: updated[index].quantity + item.quantity);
      state = updated;
    } else {
      state = [...state, item];
    }
  }

  void removeItem(String productId) {
    state = state.where((element) => element.productId != productId).toList();
  }

  void updateQty(String productId, int quantity) {
    if (quantity <= 0) {
      removeItem(productId);
      return;
    }
    final index = state.indexWhere((element) => element.productId == productId);
    if (index >= 0) {
      final updated = List<CartItem>.from(state);
      updated[index] = updated[index].copyWith(quantity: quantity);
      state = updated;
    }
  }

  void clear() {
    state = [];
  }

  Map<String, List<CartItem>> getGroupedByWholesaler() {
    final grouped = <String, List<CartItem>>{};
    for (var item in state) {
      if (grouped.containsKey(item.wholesalerBranchId)) {
        grouped[item.wholesalerBranchId]!.add(item);
      } else {
        grouped[item.wholesalerBranchId] = [item];
      }
    }
    return grouped;
  }
}

final cartProvider = StateNotifierProvider<CartNotifier, List<CartItem>>((ref) {
  return CartNotifier();
});
