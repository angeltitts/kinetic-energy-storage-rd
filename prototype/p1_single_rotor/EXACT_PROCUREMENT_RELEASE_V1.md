# P1 Exact Procurement Release v1

Date checked: 2026-08-30

Purpose: remove generic safety/instrumentation procurement ambiguity without changing the released P1 physical envelope. Exact part numbers below are primary build references; substitutions must meet the fail-closed requirements in `procurement_gate.py` and still pass incoming inspection.

## Safety chain

### S1 emergency stop — primary
- AutomationDirect GCX3131
- 22 mm, red 40 mm mushroom, twist-to-release, 1 NC contact, IP65
- checked price: $12.00
- source: https://www.automationdirect.com/adc/shopping/catalog/pushbuttons_-z-_switches_-z-_indicators/emergency_stop_pushbuttons/gcx3131

Substitution gate: mechanically latching emergency stop with >=1 NC contact. Momentary mushroom switches are not equivalents.

### K1 controller-bus isolation relay — primary
- Picker Components PC792A-1C-C2-24C-N-X
- automotive relay, SPDT, 24 VDC coil, chassis mount, 0.250 in quick-connect terminals
- contact rating: 20 A at 24 VDC resistive; maximum switching voltage 75 VDC
- checked DigiKey stock: >1000; checked unit price: $2.97
- source: https://www.digikey.com/en/products/detail/picker-components/PC792A-1C-C2-24C-N-X/12352838

Use the NO power contact so de-energizing K1 removes battery feed to the controller bus. Coil drive remains in series with the NC E-stop chain. Add appropriate coil transient suppression at the harness/driver interface and verify de-energization during stationary commissioning.

Substitution gate: 24 VDC coil preferred; contacts rated >=10 A and >=32 VDC. Do not substitute an AC-only contactor.

### F1 fuse holder + fuse — primary
- holder: Littelfuse FHAS100 sealed inline ATO holder, 32 VDC, up to 30 A, IP67, 12 AWG leads
- checked DigiKey price: $16.46
- source: https://www.digikey.com/en/product-highlight/l/littelfuse/fhas100-ato-and-mini-fuse-holders-series
- fuse: Littelfuse 0ATO010.VPGLO, 10 A, 32 VDC ATO/ATC fast-blow
- checked DigiKey price: $6.84 / 2-pack
- source: https://www.digikey.com/en/products/detail/littelfuse-inc/0ATO010-VPGLO/2518443

P1 remains capped at a 10 A fuse. A larger fuse is not an acceptable substitution.

## Passive regenerative sink

### Rdump — primary
- Ohmite HS100 22R J
- 22 ohm +/-5%, 100 W, aluminum chassis-mount wirewound resistor
- DigiKey PN HS10022RJ-ND
- checked stock: 46; checked unit price: $15.33
- source: https://www.digikey.com/en/products/detail/ohmite/HS100-22R-J/5307089

Mount to a noncombustible thermally conductive surface per manufacturer thermal requirements. Do not treat 100 W as free-air continuous capability. P1 thermal acceptance remains a physical test.

## Independent rotor-speed channel

### Optical pickup — primary
- Aratas / former Omron Components EE-SX1042
- 5 mm through-beam photointerrupter, phototransistor output
- response: 4 us rise / 4 us fall
- collector-emitter rating: 30 V max
- checked DigiKey stock: >3900; checked unit price: $3.19
- source: https://www.digikey.com/en/products/detail/omron-electronics-inc-emc-div/EE-SX1042/8742

Use with the released 12-feature optical target and a small fixed carrier PCB/bracket. At the 1650 RPM trip boundary the target produces 330 Hz, period 3.030 ms. The 4 us sensor response is >750x faster than the full pulse period. The procurement gate rejects sensors slower than 250 us.

The optical pickup remains independent of VESC commutation telemetry.

## Instrumentation

### Vibration — primary
- Adafruit MPU-6050 breakout, Product ID 3886
- 3-axis accelerometer + 3-axis gyro, I2C, 3.3/5 V-friendly breakout
- checked price: $12.95, in stock
- source: https://www.adafruit.com/product/3886

Mount rigidly to the bearing-support frame; do not mount to the polycarbonate guard.

### DC-bus cross-check — primary
- INA226-based bidirectional current/power module, 36 V measurement class, >=5 A current capability
- current commodity reference: Uxcell INA226 36 V module set
- checked price reference: $14.09 for 4 modules
- source: https://www.walmart.com/ip/16543901692

This channel is a cross-check, not the safety trip path. Verify the delivered shunt value and calibration before accepting energy measurements. Do not use the common INA219 26 V breakout because the P1 battery can reach 29.2 V.

### Contact temperatures — primary
Use four DS18B20-class contact probes for left bearing, right bearing, motor case, and VESC heat sink. A practical stocked reference is Adafruit waterproof DS18B20 ($9.95 class) or the PTFE high-temperature version, Product ID 3846, for locations needing higher cable-temperature margin.
- high-temp reference: -55 to 125 C sensor range, 1-Wire, +/-0.5 C from -10 to +85 C
- checked price: $19.95, in stock
- source: https://www.adafruit.com/product/3846

For the dump resistor thermal validation, use a K-type thermocouple on the resistor chassis rather than relying on a plastic-jacketed DS18B20 probe.

### Dump-resistor temperature — primary
- Adafruit K-type glass-braid thermocouple, Product ID 270, $9.95, in stock
- Adafruit MAX31855 K-type amplifier, Product ID 269, $14.95, in stock
- sources: https://www.adafruit.com/product/270 and https://www.adafruit.com/product/269

## DC source/sink

### Battery — retained primary
- Bioenno Power BLF-2410AS
- 24 V nominal, 10 Ah LiFePO4, built-in PCM
- 10 A max continuous discharge; 20 A peak for 5 s
- charger: 29.2 V / 2 A
- checked price: $229.99 battery + charger option
- source: https://www.bioennopower.com/products/24v-10ah-lfp-battery-abs-blf-2410as

Important: the published 29.2 V / 2 A charger specification does **not** by itself authorize arbitrary regenerative charging from a VESC. Until Bioenno explicitly confirms regenerative-source behavior, P1 must not depend on the battery as the sole regen sink. The already released 22 ohm passive controller-side dump remains mandatory and regenerative battery current remains capped at <=1 A.

Begin controlled regen tests only inside the released bus-voltage window and with measured battery state that does not force the bus above that window.

## Core drive items retained from procurement freeze
- Flipsky sensored 5055 200 KV class motor; delivered mounting face must be measured before drilling the motor plate.
- Flipsky Mini FSESC 4.20 50 A class controller or released equivalent; P1 software/current limits remain far below hardware capability.
- 2 x 12 mm KP001-dimensional pillow blocks; incoming bore and geometry measurement required.
- 12 mm precision-ground shaft, nominal 260 mm.
- HTD 5M, 15 mm wide, 15T motor pulley / 48T rotor pulley / 400 mm 80T belt; verify delivered bores and runout before powered commissioning.
- 6 mm minimum clear polycarbonate 360-degree guard; acrylic is not a substitute.

## Explicit correction to legacy BOM wording

A generic "6S battery pack" is not the released P1 source definition. The retained primary source is the 24 V-class Bioenno LiFePO4 pack above. Any alternative source must be voltage-compatible with the controller, fuse, K1, dump path, instrumentation, and released bus window and must have documented source/sink behavior. Battery chemistry/series count alone is not an acceptable equivalence rule.

## Procurement hold point

Before ordering a substitute for S1, K1, F1, Rdump, or the RPM pickup, encode its relevant ratings in `procurement_gate.py` and retain a passing check. Before powered commissioning, physical incoming inspection remains authoritative for delivered dimensions, polarity, contact behavior, sensor operation, and thermal mounting.
