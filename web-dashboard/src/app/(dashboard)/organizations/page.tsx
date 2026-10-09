'use client';

import { useEffect, useState } from 'react';
import { ColumnDef } from '@tanstack/react-table';
import { useRouter } from 'next/navigation';
import { DataTable } from '@/components/data-table/data-table';
import { DataTableColumnHeader } from '@/components/data-table/data-table-column-header';
import { Badge } from '@/components/ui/badge';
import { MoreHorizontal, FileText } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import { apiClient } from '@/lib/api-client';
import { Organization } from '@/types';

export default function OrganizationsPage() {
  const router = useRouter();
  const [organizations, setOrganizations] = useState<Organization[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchOrgs() {
      try {
        const response: any = await apiClient.get('/api/v1/organizations/');
        setOrganizations(response.items || []);
      } catch (error: any) {
        toast.error("Tashkilotlarni yuklashda xatolik: " + error.message);
      } finally {
        setLoading(false);
      }
    }
    fetchOrgs();
  }, []);

  const columns: ColumnDef<Organization>[] = [
    {
      accessorKey: 'name',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Organization Name" />,
    },
    {
      accessorKey: 'type',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Type" />,
      cell: ({ row }) => (
        <Badge variant="outline" className="capitalize">
          {row.getValue('type')}
        </Badge>
      ),
    },
    {
      accessorKey: 'status',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.getValue('status') as string;
        if (status === 'active') {
          return <Badge className="bg-emerald-500 hover:bg-emerald-600 text-white">Active</Badge>;
        }
        if (status === 'pending') {
          return <Badge className="bg-amber-500 hover:bg-amber-600 text-white">Pending</Badge>;
        }
        return <Badge variant="destructive" className="capitalize">{status}</Badge>;
      },
    },
    {
      accessorKey: 'tax_id',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Tax ID" />,
    },
    {
      id: 'actions',
      cell: ({ row }) => {
        return (
          <DropdownMenu>
            <DropdownMenuTrigger className="flex h-8 w-8 p-0 items-center justify-center rounded-md hover:bg-muted outline-none focus:bg-muted focus:ring-1 focus:ring-ring">
              <span className="sr-only">Open menu</span>
              <MoreHorizontal className="h-4 w-4" />
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end">
              <DropdownMenuItem onClick={() => router.push(`/organizations/${row.original.id}`)}>
                <FileText className="mr-2 h-4 w-4" />
                View Details
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        );
      },
    },
  ];

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Organizations</h2>
      </div>
      {loading ? (
        <div className="flex items-center justify-center h-48 text-muted-foreground">Yuklanmoqda...</div>
      ) : (
        <DataTable columns={columns} data={organizations} searchKey="name" />
      )}
    </div>
  );
}
