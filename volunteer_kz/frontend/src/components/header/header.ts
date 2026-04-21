import { Component, inject } from '@angular/core';
import { RouterLink } from '@angular/router';
import { CommonModule } from '@angular/common';
import { TranslocoModule, TranslocoService } from '@jsverse/transloco';
import { Auth } from '../../services/auth';
@Component({
  selector: 'app-header',
  imports: [RouterLink, CommonModule, TranslocoModule],
  templateUrl: './header.html',
  styleUrl: './header.css',
})
export class Header {
  constructor(
    private authService: Auth
  ){}

  checker(){
    return this.authService.isLogged();
  }

  log_out(){
    return this.authService.logout();
  }

  main_navbar = [
    {name: "NAV.MAIN MENU", link: "/home"},
    {name: "NAV.PROJECTS", link: "/projects"},
    {name: "NAV.RATINGS", link: "/ratings"},
    {name: "NAV.CONTACT", link: "/contact"}
  ]
  private transloco = inject(TranslocoService);

  login_bar = [
    {name: "LOGIN.LOG_IN", link: "/login"},
    {name: "LOGIN.REGISTER", link: "/register"}
  ]

  // constructor(
  //   private transloco: TranslocoService
  // ){};

  switchLanguage(lang: string){
    this.transloco.setActiveLang(lang);
  }
}