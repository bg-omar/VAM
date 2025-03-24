import { Injectable } from '@angular/core';

export type ShieldType = 'bare' | 'paper' | 'glass';

@Injectable({
    providedIn: 'root'
})
export class VamEngineService {
    // Constants
    private readonly rhoAe = 7.0e-7; // kg/m^3
    private readonly Ce = 1.09384563e6; // m/s
    private readonly g = 9.81; // m/s^2

    // Default model coefficients per shield type (fitted)
    private readonly modelParams = {
        bare:  { a: 1.2e-8, b: 0.00597, c: -0.21, V0: 6694 },
        paper: { a: 2.7e-8, b: 0.00612, c: -1.12, V0: -9381 },
        glass: { a: 3.6e-8, b: -0.0297, c: 12.43, V0: -6510 }
    };

    getThrust(voltage: number, shield: ShieldType): number {
        const { a, b, c, V0 } = this.modelParams[shield];
        return a * voltage ** 2 / (1 + Math.exp(-b * (voltage - V0))) + c; // g
    }

    getBernoulliPressureDrop(): number {
        return 0.5 * this.rhoAe * this.Ce ** 2; // Pa
    }

    getOptimalVortexGap(thrustGrams: number): number {
        const thrustNewtons = thrustGrams / 1000 * this.g;
        const deltaP = this.getBernoulliPressureDrop();
        const area = thrustNewtons / deltaP;
        const radius = Math.sqrt(area / Math.PI);
        return 2 * radius * 1000; // mm
    }

    getFieldGradient(voltage: number, gapMm: number): number {
        return voltage / (gapMm / 1000); // V/m
    }

    // Optional: Estimate current from thrust (empirical scale)
    estimateCurrent(thrustGrams: number): number {
        return Math.max(0, 0.15 * thrustGrams); // uA (approx)
    }
}
