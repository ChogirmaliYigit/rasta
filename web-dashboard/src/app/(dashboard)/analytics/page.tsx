'use client';

import { KpiCard } from '@/components/layout/kpi-card';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { DollarSign, Percent, ShoppingBag, TrendingUp } from 'lucide-react';
import {
  Area,
  AreaChart,
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts';

const revenueData = [
  { name: 'Jan', total: 120 },
  { name: 'Feb', total: 210 },
  { name: 'Mar', total: 180 },
  { name: 'Apr', total: 290 },
  { name: 'May', total: 320 },
  { name: 'Jun', total: 450 },
];

const topProductsData = [
  { name: 'Coca-Cola 1.5L', sales: 4000 },
  { name: 'Nestle Pure Life 1L', sales: 3000 },
  { name: 'Lay\'s Classic', sales: 2000 },
  { name: 'Red Bull', sales: 1500 },
];

const orderStatusData = [
  { name: 'Delivered', value: 400, color: '#10B981' }, // Emerald
  { name: 'Pending', value: 50, color: '#F59E0B' },   // Amber
  { name: 'Dispatched', value: 100, color: '#8B5CF6' },// Purple
  { name: 'Cancelled', value: 20, color: '#F43F5E' },  // Rose
];

export default function AnalyticsPage() {
  return (
    <div className="space-y-6">
      <h2 className="text-3xl font-bold tracking-tight">Analytics</h2>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KpiCard title="GMV" value="4.2B UZS" icon={DollarSign} trend="12% from last month" trendDirection="up" />
        <KpiCard title="Total Orders" value="12,450" icon={ShoppingBag} trend="5% from last month" trendDirection="up" />
        <KpiCard title="Avg Order Value" value="340K UZS" icon={TrendingUp} trend="2% from last month" trendDirection="up" />
        <KpiCard title="Return Rate" value="1.2%" icon={Percent} trend="0.5% higher" trendDirection="down" />
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>Revenue (Last 6 Months)</CardTitle>
          </CardHeader>
          <CardContent className="pl-2">
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={revenueData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorTotal" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#0F172A" stopOpacity={0.8}/>
                      <stop offset="95%" stopColor="#0F172A" stopOpacity={0}/>
                    </linearGradient>
                  </defs>
                  <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                  <YAxis stroke="#888888" fontSize={12} tickLine={false} axisLine={false} tickFormatter={(value) => `${value}M`} />
                  <CartesianGrid strokeDasharray="3 3" vertical={false} />
                  <Tooltip />
                  <Area type="monotone" dataKey="total" stroke="#0F172A" fillOpacity={1} fill="url(#colorTotal)" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>Order Status Distribution</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ResponsiveContainer width="100%" height="100%">
                <PieChart>
                  <Pie
                    data={orderStatusData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={80}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {orderStatusData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
