import { Component, OnInit } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { ProjectService } from '../../services/project.service';
import { Auth } from '../../services/auth';
import { Project } from '../../interfaces/api.interfaces';

@Component({
  selector: 'app-projects',
  imports: [FormsModule],
  templateUrl: './projects.html',
  styleUrl: './projects.css',
})
export class Projects implements OnInit {
  projects: Project[] = [];
  isLoading = false;
  errorMessage = '';
  filterStatus = '';

  constructor(
    private projectService: ProjectService,
    public authService: Auth
  ) {}

  ngOnInit() {
    this.loadProjects();
  }

  loadProjects() {
    this.isLoading = true;
    this.errorMessage = '';
    this.projectService.getProjects().subscribe({
      next: (data) => {
        this.projects = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Жобаларды жүктеу қатесі. Қайтадан көріңіз.';
        this.isLoading = false;
      },
    });
  }

  applyToProject(projectId: number) {
    this.projectService.applyToProject(projectId, '').subscribe({
      next: () => {
        alert('Өтінім сәтті жіберілді!');
        this.loadProjects();
      },
      error: (err) => {
        alert(err.error?.error || 'Өтінім жіберу қатесі');
      },
    });
  }

  get filteredProjects(): Project[] {
    if (!this.filterStatus) return this.projects;
    return this.projects.filter((p) => p.status === this.filterStatus);
  }

  statusLabel(s: string): string {
    const map: Record<string, string> = {
      open: 'Ашық',
      in_progress: 'Үдерісте',
      completed: 'Аяқталды',
      cancelled: 'Болдырылмады',
    };
    return map[s] ?? s;
  }
}
