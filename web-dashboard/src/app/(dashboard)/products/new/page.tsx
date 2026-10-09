'use client';

import { useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { ArrowLeft, Save } from 'lucide-react';
import { toast } from 'sonner';

export default function NewProductPage() {
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    toast.success('Mahsulot muvaffaqiyatli saqlandi!');
    router.push('/products');
  };

  return (
    <div className="space-y-6 max-w-2xl mx-auto">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-3xl font-bold tracking-tight">Yangi mahsulot qo'shish</h2>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Mahsulot ma'lumotlari</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={handleSubmit} className="space-y-4">
            <div className="space-y-2">
              <Label htmlFor="title">Nomi</Label>
              <Input id="title" placeholder="Masalan: Coca-Cola 1.5L" required />
            </div>
            
            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="barcode">Shtrix kod (Barcode)</Label>
                <Input id="barcode" placeholder="Shtrix kodni kiriting" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="sku">SKU (Artikul)</Label>
                <Input id="sku" placeholder="SKU kodni kiriting" />
              </div>
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div className="space-y-2">
                <Label htmlFor="category">Kategoriya</Label>
                <Input id="category" placeholder="Masalan: Ichimliklar" required />
              </div>
              <div className="space-y-2">
                <Label htmlFor="unit">O'lchov birligi</Label>
                <Input id="unit" placeholder="PIECE, KG, LITER" required />
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
