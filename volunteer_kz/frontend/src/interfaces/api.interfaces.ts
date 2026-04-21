export interface LoginResponse {
  access: string;
  refresh: string;
  username: string;
  role: string;
  message: string;
}

export interface Project {
  id: number;
  title: string;
  description: string;
  address: string;
  start_date: string;
  end_date: string;
  hours_count: number;
  volunteers_needed: number;
  status: 'open' | 'in_progress' | 'completed' | 'cancelled';
  category: number | null;
  category_name: string;
  applications_count: number;
  created_at: string;
}

export interface ProjectApplication {
  id: number;
  project: number;
  project_title: string;
  cover_letter: string;
  status: string;
  volunteer_username: string;
  applied_at: string;
}

export interface RatingEntry {
  rank: number;
  username: string;
  totalHour: number;
  initials: string;
}

export interface ContactMessage {
  name: string;
  email: string;
  topic: string;
  message: string;
}
