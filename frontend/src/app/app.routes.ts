import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ResultadosComponent } from './pages/resultados/resultados.component';

export const routes: Routes = [
  { path: '', component: HomeComponent },
  { path: 'resultados', component: ResultadosComponent }
];