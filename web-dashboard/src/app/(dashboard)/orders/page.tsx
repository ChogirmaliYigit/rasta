'use client';

import { useEffect, useState } from 'react';
import { ColumnDef } from '@tanstack/react-table';
import { useRouter } from 'next/navigation';
import { DataTable } from '@/components/data-table/data-table';
import { DataTableColumnHeader } from '@/components/data-table/data-table-column-header';
import { Badge } from '@/components/ui/badge';
import { MoreHorizontal, Eye } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import { apiClient } from '@/lib/api-client';
import { Order } from '@/types';

export default function OrdersPage() {
  const router = useRouter();
  const [orders, setOrders] = useState<Order[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchOrders() {
      try {
        const response: any = await apiClient.get('/api/v1/orders/');
        setOrders(response.items || []);
      } catch (error: any) {
        toast.error("Buyurtmalarni yuklashda xatolik: " + error.message);
      } finally {
        setLoading(false);
      }
    }
    fetchOrders();
  }, []);

  const columns: ColumnDef<Order>[] = [
    {
      accessorKey: 'id',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Order ID" />,
      cell: ({ row }) => {
        const id = row.getValue('id') as string;
        return <span className="font-medium">{id.substring(0, 8)}...</span>;
      }
    },
    {
      accessorKey: 'retailer_id',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Retailer ID" />,
      cell: ({ row }) => {
        const id = row.getValue('retailer_id') as string;
        return <span>{id?.substring(0, 8) || 'N/A'}...</span>;
      }
    },
    {
      accessorKey: 'status',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => {
        const status = row.getValue('status') as string;
        if (status === 'delivered') return <Badge className="bg-emerald-500 hover:bg-emerald-600 text-white">Delivered</Badge>;
        if (status === 'cancelled') return <Badge variant="destructive">Cancelled</Badge>;
        if (status === 'shipped') return <Badge className="bg-blue-500 hover:bg-blue-600 text-white">Shipped</Badge>;
        return <Badge variant="outline" className="capitalize">{status}</Badge>;
      },
    },
    {
      accessorKey: 'total_amount',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Total" />,
      cell: ({ row }) => {
        const amount = parseFloat(row.getValue('total_amount') || '0');
        return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS' }).format(amount);
      },
    },
    {
      accessorKey: 'created_at',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Date" />,
      cell: ({ row }) => {
        const dateStr = row.getValue('created_at') as string;
        return dateStr ? new Date(dateStr).toLocaleDateString() : '';
      }
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
              <DropdownMenuItem onClick={() => router.push(`/orders/${row.original.id}`)}>
                <Eye className="mr-2 h-4 w-4" />
                View details
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
        <h2 className="text-3xl font-bold tracking-tight">Orders</h2>
      </div>
      {loading ? (
        <div className="flex items-center justify-center h-48 text-muted-foreground">Yuklanmoqda...</div>
      ) : (
        <DataTable columns={columns} data={orders} searchKey="id" />
      )}
    </div>
  );
}
