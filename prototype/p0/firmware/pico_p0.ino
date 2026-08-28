/*
P0 Differential Hoop Rig
RP2040 / Raspberry Pi Pico reference firmware.

Hardware:
- 3 Hall sensors
- 4 equally spaced, mechanically retained index magnets per rotor
- 3 brushed DC motor channels
- one direction pin + one PWM pin per motor
- physical emergency stop MUST interrupt motor power directly

Serial commands at 115200 baud:
  RUN
  STOP
  RESET
  SET a b c
Example:
  SET 180 120 60

Safety:
- targets are clamped to 300 RPM
- measured overspeed above 330 RPM latches FAULT
- FAULT requires RESET after the rotor is stopped
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

const float MAX_COMMAND_RPM = 300.0f;
const float OVERSPEED_RPM = 330.0f;

// Four evenly spaced index magnets give a pulse every 0.30 s at 50 RPM.
// The previous one-pulse/rev arrangement produced a pulse only every 1.20 s
// at 50 RPM, longer than the old 1.0 s stale timeout, so valid low-speed
// operation was intermittently reported as zero RPM.
const unsigned int PULSES_PER_REV = 4;
const unsigned long STALE_TIMEOUT_US = 750000UL;

volatile unsigned long lastPulseUsA = 0;
volatile unsigned long lastPulseUsB = 0;
volatile unsigned long lastPulseUsC = 0;
volatile unsigned long periodUsA = 0;
volatile unsigned long periodUsB = 0;
volatile unsigned long periodUsC = 0;

float targetA = 0.0f;
float targetB = 0.0f;
float targetC = 0.0f;

float rpmA = 0.0f;
float rpmB = 0.0f;
float rpmC = 0.0f;

float integA = 0.0f;
float integB = 0.0f;
float integC = 0.0f;

bool runEnabled = false;
bool faultLatched = false;

const float KP = 0.8f;
const float KI = 0.25f;

String serialLine;

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
  if (periodUs == 0 || lastPulseUs == 0) return 0.0f;
  if (micros() - lastPulseUs > STALE_TIMEOUT_US) return 0.0f;
  return 60000000.0f / ((float)periodUs * (float)PULSES_PER_REV);
}

int controlMotor(float target, float measured, float &integrator, float dt) {
  target = constrain(target, 0.0f, MAX_COMMAND_RPM);
  float error = target - measured;
  integrator += error * dt;
  integrator = constrain(integrator, -300.0f, 300.0f);
  float command = KP * error + KI * integrator;
  return (int)constrain(command, 0.0f, 255.0f);
}

void stopAll() {
  analogWrite(PWM_A, 0);
  analogWrite(PWM_B, 0);
  analogWrite(PWM_C, 0);
}

void resetIntegrators() {
  integA = 0.0f;
  integB = 0.0f;
  integC = 0.0f;
}

void processCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();

  if (cmd == "RUN") {
    if (!faultLatched) {
      runEnabled = true;
      Serial.println("OK RUN");
    } else {
      Serial.println("ERR FAULT_LATCHED");
    }
    return;
  }

  if (cmd == "STOP") {
    runEnabled = false;
    stopAll();
    resetIntegrators();
    Serial.println("OK STOP");
    return;
  }

  if (cmd == "RESET") {
    if (rpmA < 5.0f && rpmB < 5.0f && rpmC < 5.0f) {
      faultLatched = false;
      runEnabled = false;
      resetIntegrators();
      stopAll();
      Serial.println("OK RESET");
    } else {
      Serial.println("ERR ROTORS_NOT_STOPPED");
    }
    return;
  }

  if (cmd.startsWith("SET ")) {
    float a, b, c;
    int parsed = sscanf(cmd.c_str(), "SET %f %f %f", &a, &b, &c);
    if (parsed == 3) {
      targetA = constrain(a, 0.0f, MAX_COMMAND_RPM);
      targetB = constrain(b, 0.0f, MAX_COMMAND_RPM);
      targetC = constrain(c, 0.0f, MAX_COMMAND_RPM);
      Serial.print("OK SET ");
      Serial.print(targetA);
      Serial.print(" ");
      Serial.print(targetB);
      Serial.print(" ");
      Serial.println(targetC);
    } else {
      Serial.println("ERR USE: SET a b c");
    }
    return;
  }

  Serial.println("ERR COMMANDS: SET a b c | RUN | STOP | RESET");
}

void readSerialCommands() {
  while (Serial.available()) {
    char ch = (char)Serial.read();
    if (ch == '\n' || ch == '\r') {
      if (serialLine.length() > 0) {
        processCommand(serialLine);
        serialLine = "";
      }
    } else if (serialLine.length() < 80) {
      serialLine += ch;
    }
  }
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

  Serial.println("P0 Differential Hoop Rig ready.");
  Serial.println("Hall sensing: 4 pulses/revolution.");
  Serial.println("Example: SET 180 120 60");
  Serial.println("Then: RUN");
}

void loop() {
  readSerialCommands();

  static unsigned long lastMs = millis();
  unsigned long nowMs = millis();
  if (nowMs - lastMs < 100) return;

  float dt = (nowMs - lastMs) / 1000.0f;
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
    runEnabled = false;
  }

  int outA = 0;
  int outB = 0;
  int outC = 0;

  if (faultLatched || !runEnabled) {
    stopAll();
  } else {
    outA = controlMotor(targetA, rpmA, integA, dt);
    outB = controlMotor(targetB, rpmB, integB, dt);
    outC = controlMotor(targetC, rpmC, integC, dt);

    analogWrite(PWM_A, outA);
    analogWrite(PWM_B, outB);
    analogWrite(PWM_C, outC);
  }

  // CSV log:
  // ms,targetA,rpmA,pwmA,targetB,rpmB,pwmB,targetC,rpmC,pwmC,fault
  Serial.print(nowMs);
  Serial.print(",");
  Serial.print(targetA);
  Serial.print(",");
  Serial.print(rpmA);
  Serial.print(",");
  Serial.print(outA);
  Serial.print(",");
  Serial.print(targetB);
  Serial.print(",");
  Serial.print(rpmB);
  Serial.print(",");
  Serial.print(outB);
  Serial.print(",");
  Serial.print(targetC);
  Serial.print(",");
  Serial.print(rpmC);
  Serial.print(",");
  Serial.print(outC);
  Serial.print(",");
  Serial.println(faultLatched ? 1 : 0);
}
