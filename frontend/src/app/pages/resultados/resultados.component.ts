import { Component, AfterViewInit } from '@angular/core';

declare var google: any;

@Component({
  selector: 'app-resultados',
  standalone: true,
  templateUrl: './resultados.component.html'
})
export class ResultadosComponent implements AfterViewInit {

  carregando = true;

  rotas = [
    { tipo: 'Mais rápida', tempo: '42 min', custo: 'R$ 4,50' },
    { tipo: 'Mais barata', tempo: '55 min', custo: 'R$ 2,30' },
    { tipo: 'Sustentável', tempo: '35 min', custo: 'R$ 0,00' }
  ];

  ngAfterViewInit() {
    const map = new google.maps.Map(document.getElementById('map'), {
      center: { lat: -23.5505, lng: -46.6333 },
      zoom: 10
    });

    new google.maps.Marker({
      position: { lat: -23.5505, lng: -46.6333 },
      map: map,
      title: 'São Paulo'
    });

    setTimeout(() => {
      this.carregando = false;
    }, 2000);
  }
}