import { NextResponse } from 'next/server';
import type { NextRequest } from 'next/server';
import { decodeJwt } from 'jose';

const publicPaths = ['/login', '/api', '/_next', '/favicon.ico'];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  const isPublicPath = publicPaths.some(path => pathname.startsWith(path));
  const token = request.cookies.get('access_token')?.value;

  let isValidToken = false;
  if (token) {
    try {
      const payload = decodeJwt(token);
      if (payload.exp && payload.exp * 1000 > Date.now()) {
        isValidToken = true;
      }
    } catch (e) {
      isValidToken = false;
    }
  }

  if (!isValidToken && !isPublicPath) {
    return NextResponse.redirect(new URL('/login', request.url));
  }

  if (isValidToken && pathname === '/login') {
    return NextResponse.redirect(new URL('/', request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!_next/static|_next/image|favicon.ico).*)'],
};
