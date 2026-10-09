'use client';

import { useEffect, useState } from 'react';
import { ColumnDef } from '@tanstack/react-table';
import { useRouter } from 'next/navigation';
import { DataTable } from '@/components/data-table/data-table';
import { DataTableColumnHeader } from '@/components/data-table/data-table-column-header';
import { Badge } from '@/components/ui/badge';
import { MoreHorizontal, Edit2 } from 'lucide-react';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { toast } from 'sonner';
import { apiClient } from '@/lib/api-client';

type InventoryItem = {
  id: string;
  product_id: string;
  quantity: number;
  price: string;
  is_active: boolean;
};

export default function InventoryPage() {
  const router = useRouter();
  const [inventory, setInventory] = useState<InventoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchInventory() {
      try {
        const response: any = await apiClient.get('/api/v1/wholesaler-inventory/');
        setInventory(response.items || []);
      } catch (error: any) {
        toast.error("Omborni yuklashda xatolik: " + error.message);
      } finally {
        setLoading(false);
      }
    }
    fetchInventory();
  }, []);

  const columns: ColumnDef<InventoryItem>[] = [
    {
      accessorKey: 'product_id',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Product ID" />,
      cell: ({ row }) => {
        const id = row.getValue('product_id') as string;
        return <span className="font-medium">{id?.substring(0, 8) || 'N/A'}...</span>;
      }
    },
    {
      accessorKey: 'quantity',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Stock" />,
      cell: ({ row }) => {
        const qty = parseInt(row.getValue('quantity') || '0');
        return (
          <div className="flex items-center">
            <span className={qty < 10 ? 'text-red-500 font-bold' : ''}>{qty}</span>
          </div>
        );
      },
    },
    {
      accessorKey: 'price',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Price" />,
      cell: ({ row }) => {
        const amount = parseFloat(row.getValue('price') || '0');
        return new Intl.NumberFormat('uz-UZ', { style: 'currency', currency: 'UZS' }).format(amount);
      },
    },
    {
      accessorKey: 'is_active',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Status" />,
      cell: ({ row }) => (
        row.getValue('is_active') 
          ? <Badge className="bg-emerald-500 hover:bg-emerald-600 text-white">Active</Badge> 
          : <Badge variant="secondary">Inactive</Badge>
      ),
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
              <DropdownMenuItem onClick={() => router.push(`/inventory/${row.original.id}`)}>
                <Edit2 className="mr-2 h-4 w-4" />
                Update stock / price
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
        <h2 className="text-3xl font-bold tracking-tight">Inventory</h2>
      </div>
      {loading ? (
        <div className="flex items-center justify-center h-48 text-muted-foreground">Yuklanmoqda...</div>
      ) : (
        <DataTable columns={columns} data={inventory} searchKey="product_id" />
      )}
    </div>
  );
}
