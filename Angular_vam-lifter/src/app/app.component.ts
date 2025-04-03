import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import {ThrustControlComponent} from "./thrust-control/thrust-control.component";

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ThrustControlComponent],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent {
  title = 'vam-lifter';
}
