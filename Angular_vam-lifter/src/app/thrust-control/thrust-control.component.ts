import { Component } from '@angular/core';
import {
  IonContent,
  IonHeader,
  IonNote,
  IonItem,
  IonTitle,
  IonRange,
  IonLabel,
  IonToolbar,
  IonCard,
  IonCardHeader,
  IonCardTitle,
  IonCardContent,
  IonSelectOption, IonSelect, IonInput
} from '@ionic/angular/standalone';

import { VamEngineService, ShieldType } from '../vam-engine.service';
import {FormsModule} from "@angular/forms";
import {DecimalPipe, NgForOf, TitleCasePipe} from "@angular/common";


@Component({
  selector: 'app-thrust-control',
  standalone: true,
  imports: [IonContent, IonHeader, IonLabel, IonNote, IonRange, IonTitle, IonToolbar, IonItem, IonCard, IonCardHeader, IonCardTitle, IonCardContent, IonSelectOption, IonSelect, IonInput, FormsModule, NgForOf, TitleCasePipe, DecimalPipe],
  templateUrl: './thrust-control.component.html',
  styleUrl: './thrust-control.component.scss'
})

export class ThrustControlComponent {
  voltage = 15000; // in volts
  gap = 25; // in mm
  shield: ShieldType = 'bare';

  constructor(public vam: VamEngineService) {}

  get thrust(): number {
    return this.vam.getThrust(this.voltage, this.shield);
  }

  get current(): number {
    return this.vam.estimateCurrent(this.thrust);
  }

  get optimalGap(): number {
    return this.vam.getOptimalVortexGap(this.thrust);
  }

  get pressureDrop(): number {
    return this.vam.getBernoulliPressureDrop();
  }

  get fieldGradient(): number {
    return this.vam.getFieldGradient(this.voltage, this.gap);
  }

  get shieldOptions(): ShieldType[] {
    return ['bare', 'paper', 'glass'];
  }
}
