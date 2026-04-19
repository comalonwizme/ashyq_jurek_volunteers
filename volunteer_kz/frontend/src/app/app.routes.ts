import { Routes } from '@angular/router';
import { Home } from '../components/home/home';
import { Login } from '../components/login/login';
import { Registration } from '../components/registration/registration';
import { Projects } from '../components/projects/projects';
import { Ratings } from '../components/ratings/ratings';
import { Problems } from '../components/problems/problems';

export const routes: Routes = [
    {path: '', redirectTo: "home", pathMatch: "full"},
    {path: 'home', component: Home},
    {path: 'login', component: Login},
    {path: "register", component: Registration},
    {path: "projects", component: Projects},
    {path: 'ratings', component: Ratings},
    {path: "problems", component: Problems}
];
