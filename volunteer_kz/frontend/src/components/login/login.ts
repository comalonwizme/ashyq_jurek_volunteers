import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Auth } from '../../services/auth';
import { Router } from '@angular/router';

@Component({
  selector: 'app-login',
  imports: [FormsModule],
  templateUrl: './login.html',
  styleUrl: './login.css',
})
export class Login {
  form = {
    username: '',
    password: ''
  }

  constructor(
    private authService: Auth,
    private kettikbarintasta: Router
  ){}

  is_load = false;
  errorMessage = "";

  login(){
    this.is_load = true
    this.errorMessage = ""
    this.authService.login(this.form).subscribe({
      next: (res: any) => {
        console.log("Ans from django: ", res);
        this.authService.saveTokens(
          res.access,
          res.refresh
        );
        localStorage.setItem('username', res.username);
        localStorage.setItem('role', res.role)
        this.kettikbarintasta.navigate(['/projects'])
      },
      error: (qate_zat) => {
        console.log('Error: ', qate_zat.error);
        this.errorMessage = qate_zat.error?.error || 'Қате логин немесе құпия сөз'
        this.is_load = false
      }
    })
  }
}
