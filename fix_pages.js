const fs = require('fs');
const path = require('path');

const pages = [
  'web-dashboard/src/app/(dashboard)/orders/page.tsx',
  'web-dashboard/src/app/(dashboard)/products/page.tsx',
  'web-dashboard/src/app/(dashboard)/inventory/page.tsx',
  'web-dashboard/src/app/(dashboard)/organizations/page.tsx'
];

pages.forEach(file => {
  let content = fs.readFileSync(file, 'utf8');
  
  // Fix asChild error by removing asChild and Button wrapper
  const asChildPattern = /<DropdownMenuTrigger asChild>[\s\S]*?<Button variant="ghost" className="h-8 w-8 p-0">([\s\S]*?)<\/Button>[\s\S]*?<\/DropdownMenuTrigger>/g;
  content = content.replace(asChildPattern, `<DropdownMenuTrigger className="flex h-8 w-8 p-0 items-center justify-center rounded-md hover:bg-muted outline-none focus:bg-muted focus:ring-1 focus:ring-ring">$1</DropdownMenuTrigger>`);

  // Inject useRouter import if it's missing but router is used
  if (content.includes('router.') && !content.includes("import { useRouter } from 'next/navigation'")) {
    content = content.replace(
      /import { ColumnDef } from '@tanstack\/react-table';/,
      `import { ColumnDef } from '@tanstack/react-table';\nimport { useRouter } from 'next/navigation';`
    );
  }
  
  // Initialize router if it's used but not initialized
  if (content.includes('router.') && !content.includes('const router = useRouter()')) {
    content = content.replace(
      /export default function (\w+)\(\) {/,
      `export default function $1() {\n  const router = useRouter();`
    );
  }

  fs.writeFileSync(file, content);
});
console.log('Fixes applied successfully');
