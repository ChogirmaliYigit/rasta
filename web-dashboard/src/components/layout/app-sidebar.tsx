'use client';

import * as React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  BarChart3, 
  Box, 
  Building2, 
  CreditCard, 
  LayoutDashboard, 
  Package, 
  Settings, 
  ShoppingCart,
  LogOut
} from 'lucide-react';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarSeparator,
} from '@/components/ui/sidebar';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useRouter } from 'next/navigation';

const allItems = [
  { title: 'Overview', url: '/', icon: LayoutDashboard, roles: ['SUPERADMIN', 'WHOLESALER_ADMIN'] },
  { title: 'Orders', url: '/orders', icon: ShoppingCart, roles: ['SUPERADMIN', 'WHOLESALER_ADMIN'] },
  { title: 'Products', url: '/products', icon: Package, roles: ['SUPERADMIN', 'WHOLESALER_ADMIN'] },
  { title: 'Inventory', url: '/inventory', icon: Box, roles: ['SUPERADMIN', 'WHOLESALER_ADMIN'] },
  { title: 'Analytics', url: '/analytics', icon: BarChart3, roles: ['SUPERADMIN'] },
  { title: 'Organizations', url: '/organizations', icon: Building2, roles: ['SUPERADMIN'] },
  { title: 'Billing', url: '/billing', icon: CreditCard, roles: ['SUPERADMIN', 'WHOLESALER_ADMIN'] },
  { title: 'Settings', url: '/settings', icon: Settings, roles: ['SUPERADMIN', 'WHOLESALER_ADMIN'] },
];

export function AppSidebar({ userRole = 'SUPERADMIN', userName = 'Admin User' }: { userRole?: string, userName?: string }) {
  const pathname = usePathname();
  const router = useRouter();

  const handleLogout = async () => {
    await fetch('/api/auth/logout', { method: 'POST' });
    router.push('/login');
    router.refresh();
  };

  const visibleItems = allItems.filter(item => item.roles.includes(userRole));
  const initials = userName.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();

  return (
    <Sidebar variant="sidebar" collapsible="icon">
      <SidebarHeader className="border-b h-16 flex items-center justify-center px-4">
        <div className="flex items-center gap-2 overflow-hidden w-full">
          <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-primary text-primary-foreground font-bold">
            R
          </div>
          <span className="truncate font-semibold text-lg group-data-[state=collapsed]:hidden">
            Rasta
          </span>
        </div>
      </SidebarHeader>
      <SidebarContent>
        <SidebarMenu className="px-2 mt-4 space-y-1">
          {visibleItems.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton 
                isActive={pathname === item.url}
                tooltip={item.title}
                render={
                  <Link href={item.url}>
                    <item.icon />
                    <span>{item.title}</span>
                  </Link>
                }
              />
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarContent>
      <SidebarSeparator />
      <SidebarFooter className="p-4">
        <SidebarMenu>
          <SidebarMenuItem>
            <div className="flex items-center gap-3 overflow-hidden group-data-[state=collapsed]:hidden mb-4">
              <Avatar className="h-9 w-9">
                <AvatarImage src="" />
                <AvatarFallback>{initials}</AvatarFallback>
              </Avatar>
              <div className="flex flex-col">
                <span className="text-sm font-medium">{userName}</span>
                <span className="text-xs text-muted-foreground">{userRole}</span>
              </div>
            </div>
            <SidebarMenuButton onClick={handleLogout} tooltip="Logout">
              <LogOut className="text-muted-foreground" />
              <span>Log out</span>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarFooter>
    </Sidebar>
  );
}
