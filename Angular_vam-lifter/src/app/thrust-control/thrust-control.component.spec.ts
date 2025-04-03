import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ThrustControlComponent } from './thrust-control.component';

describe('ThrustControlComponent', () => {
  let component: ThrustControlComponent;
  let fixture: ComponentFixture<ThrustControlComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ThrustControlComponent]
    })
    .compileComponents();
    
    fixture = TestBed.createComponent(ThrustControlComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
