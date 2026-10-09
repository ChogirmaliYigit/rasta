import { cookies } from 'next/headers';
import { decodeJwt } from 'jose';
import { User } from '@/types';

export interface Session {
  user: User;
  access_token: string;
}

export async function getSession(): Promise<Session | null> {
  const cookieStore = await cookies();
  const token = cookieStore.get('access_token')?.value;
  
  if (!token) return null;
  
  try {
    const payload = decodeJwt(token);
    return {
      user: payload as unknown as User,
      access_token: token,
    };
  } catch (error) {
    return null;
  }
}

export async function clearSession() {
  const cookieStore = await cookies();
  cookieStore.delete('access_token');
  cookieStore.delete('refresh_token');
}
