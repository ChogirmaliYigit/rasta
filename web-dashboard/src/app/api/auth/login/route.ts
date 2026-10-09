import { NextResponse } from 'next/server';

export async function POST(request: Request) {
  try {
    const { phone, password } = await request.json();

    // Call FastAPI Backend
    const backendRes = await fetch('http://127.0.0.1:8001/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        phone: phone,
        password: password,
      }),
    });

    if (!backendRes.ok) {
      const err = await backendRes.json();
      return NextResponse.json({ error: err.detail || 'Invalid credentials' }, { status: backendRes.status });
    }

    const data = await backendRes.json();
    // data should contain { access_token, token_type }

    const meRes = await fetch('http://127.0.0.1:8001/api/v1/auth/me', {
      headers: {
        'Authorization': `Bearer ${data.access_token}`
      }
    });
    
    if (!meRes.ok) {
      return NextResponse.json({ error: 'Failed to fetch user data' }, { status: 401 });
    }
    
    const userData = await meRes.json();

    const response = NextResponse.json({ user: userData }, { status: 200 });

    response.cookies.set('access_token', data.access_token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      maxAge: 86400, // 1 day
    });

    return response;
  } catch (error) {
    console.error("Login Proxy Error:", error);
    return NextResponse.json({ error: 'Internal server error' }, { status: 500 });
  }
}
