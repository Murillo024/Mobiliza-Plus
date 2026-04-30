import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home/home.component';
import { ResultadosComponent } from './pages/resultados/resultados.component';
import { GoComponent } from './pages/go/go.component';
import { TransporteComponent } from './pages/transporte/transporte.component';

export const routes: Routes = [
  { path: '',           component: HomeComponent },
  { path: 'resultados', component: ResultadosComponent },
  { path: 'go',         component: GoComponent },
  { path: 'transporte', component: TransporteComponent }
];