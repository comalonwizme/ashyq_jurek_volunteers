import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ProjectService } from '../../services/project.service';

@Component({
  selector: 'app-contacts',
  imports: [FormsModule],
  templateUrl: './contacts.html',
  styleUrl: './contacts.css',
})
export class Contacts {
  form = {
    name: '',
    email: '',
    topic: '',
    message: '',
  };
  isLoading = false;
  successMessage = '';
  errorMessage = '';

  constructor(private projectService: ProjectService) {}

  send() {
    this.isLoading = true;
    this.successMessage = '';
    this.errorMessage = '';
    this.projectService.sendContact(this.form).subscribe({
      next: () => {
        this.successMessage = 'Хабарламаңыз сәтті жіберілді!';
        this.form = { name: '', email: '', topic: '', message: '' };
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Хабарлама жіберу қатесі. Қайтадан көріңіз.';
        this.isLoading = false;
      },
    });
  }
}
