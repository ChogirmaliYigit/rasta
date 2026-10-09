'use client';

import { Bell } from 'lucide-react';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { Button } from '@/components/ui/button';
import { 
  Breadcrumb, 
  BreadcrumbItem, 
  BreadcrumbLink, 
  BreadcrumbList, 
  BreadcrumbPage, 
  BreadcrumbSeparator 
} from '@/components/ui/breadcrumb';
import { usePathname } from 'next/navigation';
import React from 'react';
import { toast } from 'sonner';

export function SiteHeader() {
  const pathname = usePathname();
  const paths = pathname === '/' ? ['Overview'] : pathname.split('/').filter(Boolean);

  return (
    <header className="sticky top-0 z-10 flex h-16 shrink-0 items-center gap-2 border-b bg-background px-4 shadow-sm md:px-6">
      <div className="flex items-center gap-2 w-full">
        <SidebarTrigger className="-ml-1" />
        <div className="mr-2 h-4 w-px bg-border hidden md:block" />
        
        <Breadcrumb className="hidden sm:block">
          <BreadcrumbList>
            {paths.map((path, index) => {
              const isLast = index === paths.length - 1;
              const title = path.charAt(0).toUpperCase() + path.slice(1);
              
              return (
                <React.Fragment key={path}>
                  <BreadcrumbItem>
                    {isLast ? (
                      <BreadcrumbPage>{title}</BreadcrumbPage>
                    ) : (
                      <BreadcrumbLink href={`/${paths.slice(0, index + 1).join('/')}`}>
                        {title}
                      </BreadcrumbLink>
                    )}
                  </BreadcrumbItem>
                  {!isLast && <BreadcrumbSeparator />}
                </React.Fragment>
              );
            })}
          </BreadcrumbList>
        </Breadcrumb>
        
        <div className="ml-auto flex items-center space-x-4">
          <Button 
            variant="ghost" 
            size="icon" 
            className="text-muted-foreground relative"
            onClick={() => toast.info('Yangi bildirishnomalar yo\'q')}
          >
            <Bell className="h-5 w-5" />
            <span className="absolute top-1.5 right-1.5 h-2 w-2 rounded-full bg-destructive"></span>
          </Button>
        </div>
      </div>
    </header>
  );
}
