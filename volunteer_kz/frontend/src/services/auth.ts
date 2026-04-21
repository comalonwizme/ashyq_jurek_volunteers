import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Injectable({ providedIn: 'root' })
export class Auth {
  private api = 'http://localhost:8000';
  private http = inject(HttpClient);
  private router = inject(Router);
  private platformId = inject(PLATFORM_ID);

  private get isBrowser(): boolean {
    return isPlatformBrowser(this.platformId);
  }

  register(data: any) {
    return this.http.post(`${this.api}/register/`, data);
  }

  login(data: any) {
    return this.http.post(`${this.api}/login/`, data);
  }

  logout() {
    const refresh = this.getRefreshToken();
    if (refresh && this.isBrowser) {
      this.http.post(`${this.api}/logout/`, { refresh }).subscribe({ error: () => {} });
    }
    if (this.isBrowser) {
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('username');
      localStorage.removeItem('role');
    }
    this.router.navigate(['/login']);
  }

  saveTokens(access: string, refresh: string) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  getAccessToken(): string | null {
    return this.isBrowser ? localStorage.getItem('access_token') : null;
  }

  getRefreshToken(): string | null {
    return this.isBrowser ? localStorage.getItem('refresh_token') : null;
  }

  isLogged(): boolean {
    return this.isBrowser ? !!localStorage.getItem('access_token') : false;
  }

  getRole(): string | null {
    return this.isBrowser ? localStorage.getItem('role') : null;
  }
}
