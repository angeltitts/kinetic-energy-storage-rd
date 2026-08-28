/*
P0 Differential Hoop Rig
RP2040 / Raspberry Pi Pico reference firmware.

Functional goals:
- read one Hall pulse/revolution for each rotor
- independently control three DC motors
- hard software RPM limit at 330 RPM
- latched fault state
- serial data logging

IMPORTANT:
The physical emergency-stop must interrupt motor power directly.
Do not rely on software as the only safety stop.
*/

const int HALL_A = 2;
const int HALL_B = 3;
const int HALL_C = 4;

const int PWM_A = 6;
const int PWM_B = 7;
const int PWM_C = 8;

const int DIR_A = 9;
const int DIR_B = 10;
const int DIR_C = 11;

const float MAX_COMMAND_RPM = 300.0;
const float OVERSPEED_RPM = 330.0;

volatile unsigned long lastPulseUsA = 0;
volatile unsigned long lastPulseUsB = 0;
volatile unsigned long lastPulseUsC = 0;
volatile unsigned long periodUsA = 0;
volatile unsigned long periodUsB = 0;
volatile unsigned long periodUsC = 0;

float targetA = 0;
float targetB = 0;
float targetC = 0;

float rpmA = 0;
float rpmB = 0;
float rpmC = 0;

float integA = 0;
float integB = 0;
float integC = 0;

bool faultLatched = false;

const float KP = 0.8;
const float KI = 0.25;

void pulseA() {
  unsigned long now = micros();
  if (lastPulseUsA != 0) periodUsA = now - lastPulseUsA;
  lastPulseUsA = now;
}
void pulseB() {
  unsigned long now = micros();
  if (lastPulseUsB != 0) periodUsB = now - lastPulseUsB;
  lastPulseUsB = now;
}
void pulseC() {
  unsigned long now = micros();
  if (lastPulseUsC != 0) periodUsC = now - lastPulseUsC;
  lastPulseUsC = now;
}

float periodToRPM(unsigned long periodUs, unsigned long lastPulseUs) {
  if (periodUs == 0) return 0.0;
  if (micros() - lastPulseUs > 1000000UL) return 0.0;
  return 60000000.0 / (float)periodUs;
}

int controlMotor(float target, float measured, float &integrator, float dt) {
  target = constrain(target, 0.0, MAX_COMMAND_RPM);
  float error = target - measured;
  integrator += error * dt;
  integrator = constrain(integrator, -300.0, 300.0);
  float command = KP * error + KI * integrator;
  return (int)constrain(command, 0.0, 255.0);
}

void stopAll() {
  analogWrite(PWM_A, 0);
  analogWrite(PWM_B, 0);
  analogWrite(PWM_C, 0);
}

void setup() {
  Serial.begin(115200);

  pinMode(HALL_A, INPUT_PULLUP);
  pinMode(HALL_B, INPUT_PULLUP);
  pinMode(HALL_C, INPUT_PULLUP);

  pinMode(PWM_A, OUTPUT);
  pinMode(PWM_B, OUTPUT);
  pinMode(PWM_C, OUTPUT);

  pinMode(DIR_A, OUTPUT);
  pinMode(DIR_B, OUTPUT);
  pinMode(DIR_C, OUTPUT);

  digitalWrite(DIR_A, HIGH);
  digitalWrite(DIR_B, HIGH);
  digitalWrite(DIR_C, HIGH);

  attachInterrupt(digitalPinToInterrupt(HALL_A), pulseA, FALLING);
  attachInterrupt(digitalPinToInterrupt(HALL_B), pulseB, FALLING);
  attachInterrupt(digitalPinToInterrupt(HALL_C), pulseC, FALLING);

  stopAll();
}

void loop() {
  static unsigned long lastMs = millis();
  unsigned long nowMs = millis();
  if (nowMs - lastMs < 100) return;

  float dt = (nowMs - lastMs) / 1000.0;
  lastMs = nowMs;

  noInterrupts();
  unsigned long pA = periodUsA;
  unsigned long pB = periodUsB;
  unsigned long pC = periodUsC;
  unsigned long lA = lastPulseUsA;
  unsigned long lB = lastPulseUsB;
  unsigned long lC = lastPulseUsC;
  interrupts();

  rpmA = periodToRPM(pA, lA);
  rpmB = periodToRPM(pB, lB);
  rpmC = periodToRPM(pC, lC);

  if (rpmA > OVERSPEED_RPM || rpmB > OVERSPEED_RPM || rpmC > OVERSPEED_RPM) {
    faultLatched = true;
  }

  if (faultLatched) {
    stopAll();
  } else {
    int outA = controlMotor(targetA, rpmA, integA, dt);
    int outB = controlMotor(targetB, rpmB, integB, dt);
    int outC = controlMotor(targetC, rpmC, integC, dt);

    analogWrite(PWM_A, outA);
    analogWrite(PWM_B, outB);
    analogWrite(PWM_C, outC);
  }

  Serial.print(nowMs);
  Serial.print(",");
  Serial.print(targetA);
  Serial.print(",");
  Serial.print(rpmA);
  Serial.print(",");
  Serial.print(targetB);
  Serial.print(",");
  Serial.print(rpmB);
  Serial.print(",");
  Serial.print(targetC);
  Serial.print(",");
  Serial.print(rpmC);
  Serial.print(",");
  Serial.println(faultLatched ? 1 : 0);
}

/*
For the first bench test, set targets directly here or extend the serial parser.

Example targets:
targetA = 180;
targetB = 120;
targetC = 60;

Keep all commands <= 300 RPM.
*/
