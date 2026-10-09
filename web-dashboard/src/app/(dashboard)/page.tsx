'use client';

import { KpiCard } from '@/components/layout/kpi-card';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DollarSign, Package, ShoppingCart, TrendingUp } from 'lucide-react';
import { Badge } from '@/components/ui/badge';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import { useRouter } from 'next/navigation';
import Link from 'next/link';

const recentOrders = [
  { id: 'ORD-001', retailer: 'Mega Market', amount: 1250000, status: 'DELIVERED', date: '2023-11-20' },
  { id: 'ORD-002', retailer: 'Corner Shop', amount: 450000, status: 'PENDING', date: '2023-11-21' },
  { id: 'ORD-003', retailer: 'City Grocery', amount: 890000, status: 'CONFIRMED', date: '2023-11-21' },
  { id: 'ORD-004', retailer: 'Fresh Foods', amount: 2100000, status: 'DISPATCHED', date: '2023-11-22' },
  { id: 'ORD-005', retailer: 'Daily Mart', amount: 150000, status: 'CANCELLED', date: '2023-11-22' },
];

function getStatusBadge(status: string) {
  switch (status) {
    case 'PENDING': return <Badge className="bg-yellow-500 hover:bg-yellow-600">Pending</Badge>;
    case 'CONFIRMED': return <Badge className="bg-blue-500 hover:bg-blue-600">Confirmed</Badge>;
    case 'DISPATCHED': return <Badge className="bg-purple-500 hover:bg-purple-600">Dispatched</Badge>;
    case 'DELIVERED': return <Badge className="bg-emerald-500 hover:bg-emerald-600">Delivered</Badge>;
    case 'CANCELLED': return <Badge variant="destructive">Cancelled</Badge>;
    default: return <Badge variant="outline">{status}</Badge>;
  }
}

export default function DashboardOverview() {
  const router = useRouter();

  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Overview</h2>
      
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KpiCard
          title="Total Orders"
          value="1,245"
          icon={ShoppingCart}
          trend="12% from last month"
          trendDirection="up"
        />
        <KpiCard
          title="Total Revenue"
          value="452.8M UZS"
          icon={DollarSign}
          trend="8% from last month"
          trendDirection="up"
        />
        <KpiCard
          title="Active Products"
          value="8,492"
          icon={Package}
          trend="124 new this week"
          trendDirection="neutral"
        />
        <KpiCard
          title="Pending Orders"
          value="43"
          icon={TrendingUp}
          trend="Needs attention"
          trendDirection="down"
        />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Recent Orders</CardTitle>
          </CardHeader>
          <CardContent>
            <Table>
              <TableHeader>
                <TableRow>
                  <TableHead>Order</TableHead>
                  <TableHead>Retailer</TableHead>
                  <TableHead>Status</TableHead>
                  <TableHead className="text-right">Amount (UZS)</TableHead>
                </TableRow>
              </TableHeader>
              <TableBody>
                {recentOrders.map((order) => (
                  <TableRow 
                    key={order.id} 
                    className="cursor-pointer hover:bg-muted/50"
                    onClick={() => router.push(`/orders/${order.id}`)}
                  >
                    <TableCell className="font-medium text-primary">{order.id}</TableCell>
                    <TableCell>{order.retailer}</TableCell>
                    <TableCell>{getStatusBadge(order.status)}</TableCell>
                    <TableCell className="text-right">
                      {order.amount.toLocaleString()}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <Link href="/products?action=add" className="block">
              <div className="p-4 border rounded-lg flex items-center justify-between hover:bg-muted/50 cursor-pointer transition-colors">
                <div>
                  <p className="font-medium text-sm">Add New Product</p>
                  <p className="text-xs text-muted-foreground">List a new item in catalog</p>
                </div>
                <Package className="h-4 w-4 text-muted-foreground" />
              </div>
            </Link>
            <Link href="/orders?status=pending" className="block">
              <div className="p-4 border rounded-lg flex items-center justify-between hover:bg-muted/50 cursor-pointer transition-colors">
                <div>
                  <p className="font-medium text-sm">Review Pending Orders</p>
                  <p className="text-xs text-muted-foreground">43 orders await confirmation</p>
                </div>
                <ShoppingCart className="h-4 w-4 text-muted-foreground" />
              </div>
            </Link>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
