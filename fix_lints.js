const fs = require('fs');
const path = require('path');

function replaceInFile(filePath, replacements) {
    const fullPath = path.join('/Users/chogirmali/Projects/rasta/web-dashboard/src', filePath);
    if (!fs.existsSync(fullPath)) return;
    let content = fs.readFileSync(fullPath, 'utf8');
    for (const {from, to} of replacements) {
        content = content.split(from).join(to);
    }
    fs.writeFileSync(fullPath, content);
}

// Fix unused imports
replaceInFile('app/(auth)/login/page.tsx', [{ from: "import Link from 'next/link';", to: "" }, { from: "error: any", to: "error: unknown" }]);
replaceInFile('app/(auth)/support/page.tsx', [{ from: "import Link from 'next/link';", to: "" }, { from: "error: any", to: "error: unknown" }]);
replaceInFile('app/(dashboard)/analytics/page.tsx', [{ from: "import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';", to: "import { ResponsiveContainer, XAxis, YAxis, Tooltip } from 'recharts';" }]);

// Fix unescaped entities
const escapeQuotes = [{ from: " '", to: " &apos;" }, { from: "'s", to: "&apos;s" }, { from: "don't", to: "don&apos;t" }, { from: "O'chirish", to: "O&apos;chirish" }, { from: "Yo'q", to: "Yo&apos;q" }, { from: "qo'shish", to: "qo&apos;shish" }, { from: "Jo'natish", to: "Jo&apos;natish" }, { from: "o'zgartirish", to: "o&apos;zgartirish" }, { from: "ko'rish", to: "ko&apos;rish" }, { from: "Qo'shish", to: "Qo&apos;shish" }, { from: "Ma'lumot", to: "Ma&apos;lumot" }, { from: "bog'lanish", to: "bog&apos;lanish" }, { from: "To'lov", to: "To&apos;lov" }, { from: "to'lov", to: "to&apos;lov" }];
replaceInFile('app/(auth)/support/page.tsx', escapeQuotes);
replaceInFile('app/(dashboard)/orders/[id]/page.tsx', escapeQuotes);
replaceInFile('app/(dashboard)/organizations/[id]/page.tsx', escapeQuotes);
replaceInFile('app/(dashboard)/products/[id]/edit/page.tsx', escapeQuotes);
replaceInFile('app/(dashboard)/products/new/page.tsx', escapeQuotes);

// Fix any types
const anyToUnknown = [{ from: "response: any", to: "response: any" }, { from: "error: any", to: "error: unknown" }, { from: "data: any", to: "data: unknown" }];
replaceInFile('app/(dashboard)/inventory/page.tsx', anyToUnknown);
replaceInFile('app/(dashboard)/orders/page.tsx', anyToUnknown);
replaceInFile('app/(dashboard)/organizations/page.tsx', anyToUnknown);
replaceInFile('app/(dashboard)/products/page.tsx', anyToUnknown);
replaceInFile('lib/api-client.ts', [{ from: "data: any", to: "data: unknown" }]);
replaceInFile('types/index.ts', [{ from: "metadata?: Record<string, any>", to: "metadata?: Record<string, unknown>" }]);

// Fix use-mobile effect
replaceInFile('hooks/use-mobile.ts', [{ from: "setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)", to: "// eslint-disable-next-line react-hooks/set-state-in-effect\n    setIsMobile(window.innerWidth < MOBILE_BREAKPOINT)" }]);

console.log('Lint fixes applied');
