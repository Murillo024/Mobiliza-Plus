import { Component } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './home.component.html'
})
export class HomeComponent {

  origem = '';
  destino = '';

  
  constructor(private router: Router) {}

  buscarRota() {
    this.router.navigate(['/resultados'], {
      queryParams: {
        origem: this.origem,
        destino: this.destino
      }
    });
  }
}