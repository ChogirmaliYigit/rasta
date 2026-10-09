'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { toast } from 'sonner';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Textarea } from '@/components/ui/textarea';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Loader2, ArrowLeft } from 'lucide-react';


export default function SupportPage() {
  const router = useRouter();
  const [isLoading, setIsLoading] = useState(false);

  async function onSubmit(e: React.FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setIsLoading(true);
    
    const formData = new FormData(e.currentTarget);
    const data = {
      phone: formData.get('phone'),
      name: formData.get('name'),
      message: formData.get('message'),
    };

    try {
      const response = await fetch('/api/support', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error('Xatolik yuz berdi');
      }

      toast.success('Xabar administratorga yuborildi. Tez orada siz bilan bog\'lanamiz.');
      router.push('/login');
    } catch (error: any) {
      toast.error('Xabarni yuborishda xatolik yuz berdi.');
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <Card className="border-0 shadow-lg">
      <CardHeader>
        <CardTitle>Yordam markazi</CardTitle>
        <CardDescription>
          Tizimga kirishda muammo bo'lsa yoki parolni unutgan bo'lsangiz, administratorga xabar qoldiring.
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={onSubmit} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="name">Ismingiz (yoki tashkilot nomi)</Label>
            <Input id="name" name="name" required />
          </div>
          
          <div className="space-y-2">
            <Label htmlFor="phone">Telefon raqam</Label>
            <Input id="phone" name="phone" placeholder="+998 90 123 45 67" required />
          </div>

          <div className="space-y-2">
            <Label htmlFor="message">Muammo haqida qisqacha</Label>
            <Textarea id="message" name="message" required />
          </div>

          <div className="grid grid-cols-2 gap-4 pt-2">
            <Button type="button" variant="outline" className="w-full" onClick={() => router.push('/login')} disabled={isLoading}>
              <ArrowLeft className="mr-2 h-4 w-4" /> Bekor qilish
            </Button>
            <Button type="submit" className="w-full" disabled={isLoading}>
              {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
              Yuborish
            </Button>
          </div>
        </form>
      </CardContent>
    </Card>
  );
}
