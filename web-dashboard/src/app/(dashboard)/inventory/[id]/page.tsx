'use client';

import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ArrowLeft, Save, Package, DollarSign } from 'lucide-react';
import { toast } from 'sonner';

export default function InventoryManagePage() {
  const { id } = useParams();
  const router = useRouter();

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Ombor ma\'lumotlari yangilandi!');
    router.push('/inventory');
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-3xl font-bold tracking-tight">Omborni boshqarish</h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Mahsulot zaxirasi va narxi</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSave} className="space-y-6">
            <div className="bg-muted/50 p-4 rounded-lg flex items-center gap-4">
              <Package className="h-8 w-8 text-primary" />
              <div>
                <p className="font-semibold text-lg">Coca-Cola 1.5L (Mock)</p>
                <p className="text-sm text-muted-foreground">ID: {id}</p>
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="stock">Mavjud qoldiq (dona/kg)</Label>
                <Input id="stock" type="number" defaultValue="5000" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="moq">Minimal buyurtma (MOQ)</Label>
                <Input id="moq" type="number" defaultValue="100" required />
              </div>
            </div>

            <div className="space-y-2">
              <Label htmlFor="price">Sotuv narxi (UZS)</Label>
              <div className="relative">
                <DollarSign className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                <Input id="price" type="number" defaultValue="12000" className="pl-9" required />
              </div>
            </div>

            <div className="pt-4 flex justify-end gap-2">
              <Button type="button" variant="outline" onClick={() => router.back()}>Bekor qilish</Button>
              <Button type="submit"><Save className="w-4 h-4 mr-2" /> Saqlash</Button>
            </div>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
