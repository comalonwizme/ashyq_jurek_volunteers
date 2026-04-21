import { Injectable, inject, PLATFORM_ID } from '@angular/core';
import { HttpClient} from '@angular/common/http';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';

@Injectable({
  providedIn: 'root',
})
export class Auth {
  private api = 'http://localhost:8000';
  private http = inject(HttpClient);
  private router = inject(Router);
  private platformId = inject(PLATFORM_ID);
  
  private get isBrowser(): boolean{
    return isPlatformBrowser(this.platformId);
  }

  register(data: any){
    return this.http.post(`${this.api}/register/`, data)
  }

  login(data: any){
    return this.http.post(`${this.api}/login/`, data)
  }

  saveTokens(access: string, refresh: string){
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
  }

  getAccessToken(): string | null {
    return localStorage.getItem('access_token');
  }

  getRefreshToken(): string | null {
    return localStorage.getItem('refresh_token');
  }

  isLogged() : boolean{
    if(this.isBrowser){
      return !!localStorage.getItem('access_token')
    }
    return false;
  }

  logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    this.router.navigate(['/login'])
  }

  getRole() : string | null{
    return localStorage.getItem('role');
  }
}