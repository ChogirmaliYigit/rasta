'use client';

import { useParams, useRouter } from 'next/navigation';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { ArrowLeft, Building2, MapPin, Phone, Mail, CheckCircle, XCircle } from 'lucide-react';
import { toast } from 'sonner';

export default function OrganizationDetailsPage() {
  const { id } = useParams();
  const router = useRouter();

  // Mock org data
  const org = {
    id,
    name: 'Mega Market MChJ',
    type: 'RETAIL_STORE',
    inn: '123456789',
    director: 'Alisher O.',
    phone: '+998 90 123 45 67',
    email: 'info@megamarket.uz',
    address: 'Toshkent sh., Yunusobod t., Amir Temur ko\'chasi, 10-uy',
    status: 'ACTIVE',
    createdAt: '2023-10-01'
  };

  const handleApprove = () => {
    toast.success("Tashkilot muvaffaqiyatli tasdiqlandi!");
  };

  const handleSuspend = () => {
    toast.success("Tashkilot bloklandi!");
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      <div className="flex items-center gap-4">
        <Button variant="outline" size="icon" onClick={() => router.back()}>
          <ArrowLeft className="h-4 w-4" />
        </Button>
        <h2 className="text-3xl font-bold tracking-tight">Tashkilot profili</h2>
        <div className="ml-auto">
          {org.status === 'ACTIVE' ? (
            <Badge className="bg-emerald-500 hover:bg-emerald-600"><CheckCircle className="w-3 h-3 mr-1"/> Faol</Badge>
          ) : (
            <Badge variant="destructive"><XCircle className="w-3 h-3 mr-1"/> Bloklangan</Badge>
          )}
        </div>
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Building2 className="h-5 w-5 text-muted-foreground" />
              Asosiy ma'lumotlar
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground">Tashkilot nomi</p>
              <p className="font-medium text-lg">{org.name}</p>
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-muted-foreground">Turi</p>
                <Badge variant={org.type === 'WHOLESALER' ? 'default' : 'secondary'}>{org.type}</Badge>
              </div>
              <div>
                <p className="text-sm text-muted-foreground">STIR (INN)</p>
                <p className="font-medium">{org.inn}</p>
              </div>
            </div>
            <div>
              <p className="text-sm text-muted-foreground">Direktor</p>
              <p className="font-medium">{org.director}</p>
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2">
              <Phone className="h-5 w-5 text-muted-foreground" />
              Bog'lanish
            </CardTitle>
          </CardHeader>
          <CardContent className="space-y-4">
            <div>
              <p className="text-sm text-muted-foreground flex items-center gap-2">
                <Phone className="h-3 w-3" /> Telefon
              </p>
              <p className="font-medium">{org.phone}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground flex items-center gap-2">
                <Mail className="h-3 w-3" /> E-pochta
              </p>
              <p className="font-medium">{org.email}</p>
            </div>
            <div>
              <p className="text-sm text-muted-foreground flex items-center gap-2">
                <MapPin className="h-3 w-3" /> Manzil
              </p>
              <p className="font-medium">{org.address}</p>
            </div>
          </CardContent>
        </Card>
      </div>

      <Card>
        <CardContent className="pt-6">
          <div className="flex gap-4 justify-end">
            <Button variant="destructive" onClick={handleSuspend}>Bloklash (Suspend)</Button>
            <Button className="bg-emerald-600 hover:bg-emerald-700 text-white" onClick={handleApprove}>Tasdiqlash (Approve)</Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
