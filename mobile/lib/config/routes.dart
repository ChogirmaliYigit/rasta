import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../features/auth/presentation/providers/auth_provider.dart';
import '../features/auth/presentation/screens/login_screen.dart';
import '../core/widgets/main_shell.dart';
import '../features/catalog/presentation/screens/catalog_screen.dart';
import '../features/catalog/presentation/screens/product_detail_screen.dart';
import '../features/inventory/presentation/screens/inventory_screen.dart';
import '../features/inventory/presentation/screens/pos_sale_screen.dart';
import '../features/orders/presentation/screens/orders_screen.dart';
import '../features/orders/presentation/screens/order_detail_screen.dart';
import '../features/orders/presentation/screens/return_act_screen.dart';
import '../features/reorder_alerts/presentation/screens/reorder_alerts_screen.dart';
import '../features/profile/presentation/screens/profile_screen.dart';
import '../features/cart/presentation/screens/cart_screen.dart';

final rootNavigatorKey = GlobalKey<NavigatorState>();
final shellNavigatorCatalogKey = GlobalKey<NavigatorState>(debugLabel: 'catalog');
final shellNavigatorInventoryKey = GlobalKey<NavigatorState>(debugLabel: 'inventory');
final shellNavigatorOrdersKey = GlobalKey<NavigatorState>(debugLabel: 'orders');
final shellNavigatorAlertsKey = GlobalKey<NavigatorState>(debugLabel: 'alerts');
final shellNavigatorProfileKey = GlobalKey<NavigatorState>(debugLabel: 'profile');

final routerProvider = Provider<GoRouter>((ref) {
  final authState = ref.watch(authProvider);

  return GoRouter(
    navigatorKey: rootNavigatorKey,
    initialLocation: '/catalog',
    redirect: (context, state) {
      final isAuth = authState.status == AuthStatus.authenticated;
      final isLoginRoute = state.uri.path == '/login';

      if (!isAuth && !isLoginRoute) {
        return '/login';
      }
      if (isAuth && isLoginRoute) {
        return '/catalog';
      }
      return null;
    },
    routes: [
      GoRoute(
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/cart',
        builder: (context, state) => const CartScreen(),
      ),
      StatefulShellRoute.indexedStack(
        builder: (context, state, navigationShell) {
          return MainShell(navigationShell: navigationShell);
        },
        branches: [
          StatefulShellBranch(
            navigatorKey: shellNavigatorCatalogKey,
            routes: [
              GoRoute(
                path: '/catalog',
                builder: (context, state) => const CatalogScreen(),
                routes: [
                  GoRoute(
                    path: 'product/:id',
                    builder: (context, state) => ProductDetailScreen(id: state.pathParameters['id']!),
                  ),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: shellNavigatorInventoryKey,
            routes: [
              GoRoute(
                path: '/inventory',
                builder: (context, state) => const InventoryScreen(),
                routes: [
                  GoRoute(
                    path: 'pos-sale',
                    builder: (context, state) => const POSSaleScreen(),
                  ),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: shellNavigatorOrdersKey,
            routes: [
              GoRoute(
                path: '/orders',
                builder: (context, state) => const OrdersScreen(),
                routes: [
                  GoRoute(
                    path: ':id',
                    builder: (context, state) => OrderDetailScreen(id: state.pathParameters['id']!),
                    routes: [
                      GoRoute(
                        path: 'return',
                        builder: (context, state) => ReturnActScreen(id: state.pathParameters['id']!),
                      ),
                    ],
                  ),
                ],
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: shellNavigatorAlertsKey,
            routes: [
              GoRoute(
                path: '/alerts',
                builder: (context, state) => const ReorderAlertsScreen(),
              ),
            ],
          ),
          StatefulShellBranch(
            navigatorKey: shellNavigatorProfileKey,
            routes: [
              GoRoute(
                path: '/profile',
                builder: (context, state) => const ProfileScreen(),
              ),
            ],
          ),
        ],
      ),
    ],
  );
});
