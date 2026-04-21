import { Component } from '@angular/core';
import { Auth } from '../../services/auth';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
@Component({
  selector: 'app-registration',
  imports: [FormsModule],
  templateUrl: './registration.html',
  styleUrl: './registration.css',
})
export class Registration {
  form = {
    username: '',
    email: '',
    password: ''
  };
  is_load = false;
  errorMessage = "";
  constructor(
    private authService: Auth,
    private router: Router
  ){}

  register(){
    this.is_load = true
    this.errorMessage = "";
    this.authService.register(this.form).subscribe({
      next: (res: any) => {
        console.log("Ans from django: ", res);
        this.authService.saveTokens(
          res.access,
          res.refresh
        );
        localStorage.setItem('role', res.role);
        localStorage.setItem('username', res.username)
        this.router.navigate(['projects/'])
      },
      error: (err) => {
        console.log("Error response:", err.error);
        this.errorMessage = err.error?.username?.[0] || err.error?.email?.[0] || 'Тіркелу қатесі',
        this.is_load = false
      }
    })
  }
}
