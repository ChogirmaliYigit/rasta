import { AppSidebar } from '@/components/layout/app-sidebar';
import { SiteHeader } from '@/components/layout/site-header';
import { SidebarProvider, SidebarInset } from '@/components/ui/sidebar';
import { cookies } from 'next/headers';
import * as jose from 'jose';

export default async function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const cookieStore = await cookies();
  const token = cookieStore.get('access_token')?.value;
  let userRole = 'SUPERADMIN';
  let userName = 'Admin User';
  
  if (token) {
    try {
      const decoded = jose.decodeJwt(token);
      if (decoded.role) userRole = decoded.role as string;
      if (decoded.full_name) userName = decoded.full_name as string;
    } catch (e) {
      console.error(e);
    }
  }

  return (
    <SidebarProvider>
      <AppSidebar userRole={userRole} userName={userName} />
      <SidebarInset>
        <SiteHeader />
        <main className="flex-1 space-y-4 p-4 md:p-8 pt-6">
          {children}
        </main>
      </SidebarInset>
    </SidebarProvider>
  );
}
