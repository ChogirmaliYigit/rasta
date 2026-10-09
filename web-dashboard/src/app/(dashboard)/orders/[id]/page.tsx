'use client';

import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Package, CheckCircle, Clock, Truck, XCircle } from 'lucide-react';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';

function getStatusBadge(status: string) {
  switch (status.toUpperCase()) {
    case 'PENDING': return <Badge className="bg-yellow-500 hover:bg-yellow-600"><Clock className="w-3 h-3 mr-1"/> Pending</Badge>;
    case 'CONFIRMED': return <Badge className="bg-blue-500 hover:bg-blue-600"><CheckCircle className="w-3 h-3 mr-1"/> Confirmed</Badge>;
    case 'DISPATCHED': return <Badge className="bg-purple-500 hover:bg-purple-600"><Truck className="w-3 h-3 mr-1"/> Dispatched</Badge>;
    case 'DELIVERED': return <Badge className="bg-emerald-500 hover:bg-emerald-600"><CheckCircle className="w-3 h-3 mr-1"/> Delivered</Badge>;
    case 'CANCELLED': return <Badge variant="destructive"><XCircle className="w-3 h-3 mr-1"/> Cancelled</Badge>;
    default: return <Badge variant="outline">{status}</Badge>;
  }
}

export default function OrderDetailsPage() {
  const { id } = useParams();
  const router = useRouter();

  // Mock data for MVP
  const order = {
    id: id,
    retailer: 'Mega Market',
    status: 'PENDING',
    date: '2023-11-21',
    amount: 1500000,
    items: [
      { id: 1, name: 'Coca-Cola 1.5L', price: 12000, quantity: 100, total: 1200000 },
      { id: 2, name: 'Lay\'s Classic 150g', price: 15000, quantity: 20, total: 300000 },
    ],
    shippingAddress: 'Tashkent, Yunusabad, Amir Temur 10',
    contact: '+998 90 123 45 67',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-3xl font-bold tracking-tight">Buyurtma: {id}</h2>
        <div className="ml-auto">
          {getStatusBadge(order.status)}
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle>Mijoz ma'lumotlari</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">Tashkilot</p>
              <p className="font-medium">{order.retailer}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Manzil</p>
              <p className="font-medium">{order.shippingAddress}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Telefon</p>
              <p className="font-medium">{order.contact}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle>Buyurtma xulosasi</CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">Sana</p>
              <p className="font-medium">{order.date}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Jami summa</p>
              <p className="font-medium text-xl text-primary">{order.amount.toLocaleString()} UZS</p>
            </div>
            <div className="flex gap-2 mt-4">
              <Button className="w-full bg-blue-600 hover:bg-blue-700">Tasdiqlash</Button>
              <Button variant="destructive" className="w-full">Bekor qilish</Button>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Mahsulotlar</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>Mahsulot</TableHead>
                <TableHead className="text-right">Narxi</TableHead>
                <TableHead className="text-right">Soni</TableHead>
                <TableHead className="text-right">Jami</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {order.items.map((item) => (
                <TableRow key={item.id}>
                  <TableCell className="font-medium">
                    <div className="flex items-center gap-2">
                      <Package className="h-4 w-4 text-muted-foreground" />
                      {item.name}
                    </div>
                  </TableCell>
                  <TableCell className="text-right">{item.price.toLocaleString()} UZS</TableCell>
                  <TableCell className="text-right">{item.quantity}</TableCell>
                  <TableCell className="text-right font-bold">{item.total.toLocaleString()} UZS</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  );
}
