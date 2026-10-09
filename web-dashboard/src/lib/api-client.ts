export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8001';

class ApiClient {
  private async fetch<T>(url: string, options: RequestInit = {}): Promise<T> {
    const isServer = typeof window === 'undefined';
    
    const headers = new Headers(options.headers || {});
    headers.set('Content-Type', 'application/json');

    let targetUrl = '';
    
    if (isServer) {
      // In server components, fetch directly to backend and attach cookie manually
      const { cookies } = await import('next/headers');
      const token = (await cookies()).get('access_token')?.value;
      if (token) {
        headers.set('Authorization', `Bearer ${token}`);
      }
      // Make sure url starts with /
      const path = url.startsWith('/') ? url : `/${url}`;
      targetUrl = `${API_BASE_URL}${path}`;
    } else {
      // In client components, route through Next.js proxy to attach HttpOnly cookie
      const path = url.startsWith('/') ? url : `/${url}`;
      targetUrl = `/api/proxy${path}`;
    }

    const response = await fetch(targetUrl, {
      ...options,
      headers,
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || errorData.error || errorData.message || response.statusText);
    }

    return response.json();
  }

  get<T>(url: string, options?: RequestInit) {
    return this.fetch<T>(url, { ...options, method: 'GET' });
  }

  post<T>(url: string, data: unknown, options?: RequestInit) {
    return this.fetch<T>(url, {
      ...options,
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  put<T>(url: string, data: unknown, options?: RequestInit) {
    return this.fetch<T>(url, {
      ...options,
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  delete<T>(url: string, options?: RequestInit) {
    return this.fetch<T>(url, { ...options, method: 'DELETE' });
  }
}

export const apiClient = new ApiClient();
