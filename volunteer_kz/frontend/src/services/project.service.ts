import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Project, ProjectApplication, RatingEntry, ContactMessage } from '../interfaces/api.interfaces';

@Injectable({ providedIn: 'root' })
export class ProjectService {
  private api = 'http://localhost:8000';
  private http = inject(HttpClient);

  getProjects() {
    return this.http.get<Project[]>(`${this.api}/projects/`);
  }

  getProject(id: number) {
    return this.http.get<Project>(`${this.api}/projects/${id}/`);
  }

  createProject(data: Partial<Project>) {
    return this.http.post<Project>(`${this.api}/projects/`, data);
  }

  updateProject(id: number, data: Partial<Project>) {
    return this.http.put<Project>(`${this.api}/projects/${id}/`, data);
  }

  deleteProject(id: number) {
    return this.http.delete(`${this.api}/projects/${id}/`);
  }

  applyToProject(id: number, coverLetter: string) {
    return this.http.post<ProjectApplication>(
      `${this.api}/projects/${id}/apply/`,
      { cover_letter: coverLetter }
    );
  }

  getRatings() {
    return this.http.get<RatingEntry[]>(`${this.api}/ratings/`);
  }

  sendContact(data: ContactMessage) {
    return this.http.post<{ message: string }>(`${this.api}/contact/`, data);
  }
}
