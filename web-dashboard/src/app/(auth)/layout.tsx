export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-muted/40 p-4">
      <div className="w-full max-w-md space-y-8">
        <div className="flex flex-col items-center justify-center text-center space-y-2">
          <div className="h-12 w-12 rounded-lg bg-primary flex items-center justify-center">
            <span className="text-primary-foreground font-bold text-2xl">R</span>
          </div>
          <h1 className="text-2xl font-semibold tracking-tight text-foreground">
            Rasta B2B Marketplace
          </h1>
          <p className="text-sm text-muted-foreground">
            Sign in to your wholesale account
          </p>
        </div>
        {children}
      </div>
    </div>
  );
}
