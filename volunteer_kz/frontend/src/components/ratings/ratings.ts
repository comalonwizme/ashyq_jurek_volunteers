import { Component, OnInit } from '@angular/core';
import { ProjectService } from '../../services/project.service';
import { RatingEntry } from '../../interfaces/api.interfaces';

@Component({
  selector: 'app-ratings',
  imports: [],
  templateUrl: './ratings.html',
  styleUrl: './ratings.css',
})
export class Ratings implements OnInit {
  ratings: RatingEntry[] = [];
  isLoading = false;
  errorMessage = '';

  constructor(private projectService: ProjectService) {}

  ngOnInit() {
    this.loadRatings();
  }

  loadRatings() {
    this.isLoading = true;
    this.errorMessage = '';
    this.projectService.getRatings().subscribe({
      next: (data) => {
        this.ratings = data;
        this.isLoading = false;
      },
      error: () => {
        this.errorMessage = 'Рейтингті жүктеу қатесі';
        this.isLoading = false;
      },
    });
  }

  get topThree(): RatingEntry[] {
    return this.ratings.slice(0, 3);
  }

  get restRatings(): RatingEntry[] {
    return this.ratings.slice(3);
  }
}
