import { NextRequest, NextResponse } from 'next/server';

export async function GET(req: NextRequest, props: { params: Promise<{ path: string[] }> }) {
  const params = await props.params;
  return handleProxy(req, params.path);
}
export async function POST(req: NextRequest, props: { params: Promise<{ path: string[] }> }) {
  const params = await props.params;
  return handleProxy(req, params.path);
}
export async function PUT(req: NextRequest, props: { params: Promise<{ path: string[] }> }) {
  const params = await props.params;
  return handleProxy(req, params.path);
}
export async function DELETE(req: NextRequest, props: { params: Promise<{ path: string[] }> }) {
  const params = await props.params;
  return handleProxy(req, params.path);
}
export async function PATCH(req: NextRequest, props: { params: Promise<{ path: string[] }> }) {
  const params = await props.params;
  return handleProxy(req, params.path);
}

async function handleProxy(req: NextRequest, path: string[]) {
  try {
    const backendUrl = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001';
    
    // Construct the backend URL
    const targetPath = '/' + path.join('/');
    const searchParams = req.nextUrl.searchParams.toString();
    const targetUrl = `${backendUrl}${targetPath}${searchParams ? '?' + searchParams : ''}`;
    
    // Extract headers (including cookies)
    const headers = new Headers(req.headers);
    headers.delete('host'); // Let fetch set the host
    
    // Check for auth cookie and append to Authorization header if missing
    const token = req.cookies.get('access_token')?.value;
    if (token && !headers.has('Authorization')) {
      headers.set('Authorization', `Bearer ${token}`);
    }

    // Determine body
    let body = undefined;
    if (req.method !== 'GET' && req.method !== 'HEAD') {
      body = await req.arrayBuffer(); // read raw body
    }

    // Fetch from backend
    const backendRes = await fetch(targetUrl, {
      method: req.method,
      headers,
      body,
      redirect: 'manual',
    });

    // Proxy the response back
    const responseHeaders = new Headers(backendRes.headers);
    // Don't forward content-encoding as it might break when we stream the response
    responseHeaders.delete('content-encoding');

    return new NextResponse(backendRes.body, {
      status: backendRes.status,
      statusText: backendRes.statusText,
      headers: responseHeaders,
    });
  } catch (error) {
    console.error('Proxy error:', error);
    return NextResponse.json({ error: 'Proxy Internal Server Error' }, { status: 500 });
  }
}
