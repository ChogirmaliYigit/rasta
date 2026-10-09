'use client';

import { ColumnDef } from '@tanstack/react-table';
import { DataTable } from '@/components/data-table/data-table';
import { DataTableColumnHeader } from '@/components/data-table/data-table-column-header';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { BillingEntry } from '@/types';

const mockBilling: BillingEntry[] = [
  { id: 'txn_1', organization_id: 'org_1', transaction_type: 'CREDIT_PAYMENT', amount: 5000000, balance_after: 5000000, reference_order_id: null, description: 'Bank Transfer - Top up', created_at: '2023-11-20T10:00:00Z' },
  { id: 'txn_2', organization_id: 'org_1', transaction_type: 'DEBIT_FEE', amount: 15000, balance_after: 4985000, reference_order_id: 'ORD-2023-001', description: 'Platform fee for order ORD-2023-001', created_at: '2023-11-21T11:00:00Z' },
  { id: 'txn_3', organization_id: 'org_1', transaction_type: 'DEBIT_FEE', amount: 4500, balance_after: 4980500, reference_order_id: 'ORD-2023-002', description: 'Platform fee for order ORD-2023-002', created_at: '2023-11-21T15:30:00Z' },
];

export default function BillingPage() {
  const columns: ColumnDef<BillingEntry>[] = [
    {
      accessorKey: 'created_at',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Date" />,
      cell: ({ row }) => new Date(row.getValue('created_at')).toLocaleString(),
    },
    {
      accessorKey: 'transaction_type',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Type" />,
      cell: ({ row }) => {
        const type = row.getValue('transaction_type') as string;
        if (type === 'CREDIT_PAYMENT') return <span className="text-emerald-500 font-medium">Top Up</span>;
        if (type === 'DEBIT_FEE') return <span className="text-rose-500 font-medium">Platform Fee</span>;
        return <span>{type}</span>;
      },
    },
    {
      accessorKey: 'description',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Description" />,
    },
    {
      accessorKey: 'amount',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Amount" />,
      cell: ({ row }) => {
        const isCredit = row.original.transaction_type === 'CREDIT_PAYMENT';
        return (
          <div className={`font-medium ${isCredit ? 'text-emerald-500' : 'text-rose-500'}`}>
            {isCredit ? '+' : '-'}{row.original.amount.toLocaleString()} UZS
          </div>
        );
      },
    },
    {
      accessorKey: 'balance_after',
      header: ({ column }) => <DataTableColumnHeader column={column} title="Balance" />,
      cell: ({ row }) => (
        <div className="font-medium text-muted-foreground">
          {row.original.balance_after.toLocaleString()} UZS
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-3xl font-bold tracking-tight">Billing & Transactions</h2>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        <Card className="bg-primary text-primary-foreground">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-primary-foreground/80">Current Balance</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold">4,980,500 UZS</div>
            <p className="text-xs text-primary-foreground/80 mt-1">Sufficient for ~332 standard orders</p>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Transaction History</CardTitle>
        </CardHeader>
        <CardContent>
          <DataTable columns={columns} data={mockBilling} searchKey="description" />
        </CardContent>
      </Card>
    </div>
  );
}
