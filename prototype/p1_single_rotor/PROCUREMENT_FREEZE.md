# P1 Procurement Freeze — Build Release v1.0

Date: 2026-08-28

This document freezes the low-energy prototype around specific purchasable components or exact equivalents.

## Core purchased components

### Motor
Primary:
- Flipsky Sensored Outrunner BLDC Motor 5055, 200KV, 1500W
- Price reference: about $43
- Voltage range: 6-12S
- Shaft diameter: 8 mm
- 12N/14P
- Rated torque: 0.85 N·m
- Product family source: https://flipsky.net/
- Supplier/spec corroboration: https://flipskycn.en.made-in-china.com/product/BUXrsNKjNwkv/

Reason:
- inexpensive
- sensored
- plenty of torque margin for a 31 J test article
- 8 mm shaft supports an off-the-shelf timing pulley

### Motor controller
Primary:
- Flipsky Mini FSESC4.20, 50A class
- Price reference: $56
- voltage range: 8-60 V
- 60,000 ERPM limit
- current capability far above this prototype's imposed battery-current limit

Source:
https://flipsky.net/collections/v4-series

P1 firmware/configuration limits remain much lower than hardware capability.

### DC source/sink
Primary:
- Bioenno Power BLF-2410AS
- 24 V / 10 Ah LiFePO4
- price reference: $229.99 with charger option
- 10 A continuous discharge, 20 A peak (5 s)
- 29.2 V / 2 A recommended charger
- built-in protection/balancing

Source:
https://www.bioennopower.com/products/24v-10ah-lfp-battery-abs-blf-2410as

P1 limits:
- VESC battery discharge current <= 5 A
- VESC regenerative battery current <= 1 A until manufacturer charge-current acceptance is confirmed in writing
- do not operate at full battery state-of-charge during regenerative tests; begin at a state that permits charge acceptance

Alternative if available:
- ExpertPower EP2410, 25.6 V / 10 Ah LiFePO4
- published continuous charge: 10 A
- published continuous discharge: 10 A
- price reference: $94.99, but currently listed out of stock at time of freeze
- https://www.expertpower.us/products/24v-10ah-lifepo4-ep2410

### Bearings
- 2 x AMI KP001 or dimensional-equivalent 12 mm pillow-block bearings
- bore: 12 mm
- bolt spacing: 56 mm
- M6 mounting
- base-to-center: 19 mm
- overall length: 71 mm
- reference commercial price: $38.31 each from Motion; commodity equivalents are cheaper

Source:
https://www.motion.com/products/sku/03770000

### Shaft
- 12 mm precision-ground steel shaft
- nominal length: 260 mm
- h8 or better preferred
- straightness sufficient to achieve assembled OD runout <= 0.25 mm

### Timing transmission

Motor pulley:
- HTD 5M, 15 tooth, 15 mm belt width
- 8 mm finished bore
- source family: Maedler PN 17231500 is pilot-bore stock; use a vendor-finished 8 mm bore equivalent if possible

Rotor-shaft pulley:
- HTD 5M, 48 tooth, 15 mm belt width
- 12 mm finished bore
- reference online 12 mm-bore 48T options are readily available

Belt:
- Maedler PN 17331800
- HTD 5M
- 400 mm effective length
- 80 teeth
- 15 mm width
- price reference: $17.70

Source:
https://maedlernorthamerica.com/partshop/neoprene-timing-belt-htd-5m-width-15mm-lw-400mm-80-teeth-pn-17331800/

Transmission ratio:
    rotor RPM = motor RPM * 15/48
    ratio = 3.2:1 reduction

At 25.6 V nominal and 200 KV, the motor no-load estimate is 5120 RPM.
Ideal shaft speed is therefore about 1600 RPM.
The VESC still enforces the 1500 RPM rotor command limit.

Nominal pulley center distance for the 400 mm belt:
- approximately 118.3 mm
- motor plate must provide at least +/-10 mm center-distance adjustment for belt installation/tension

## Instrumentation

Independent speed:
- Hall or optical tachometer channel independent of VESC commutation telemetry
- target update rate >=20 Hz at 1500 RPM

Vibration:
- MPU6050 / compatible 3-axis accelerometer on bearing-support frame

Electrical:
- use VESC telemetry for bus voltage/current
- preferred independent cross-check: INA226-based bus monitor sized for the imposed <=5 A commissioning current

Temperature:
- contact thermocouples or digital temperature sensors on:
  - left bearing housing
  - right bearing housing
  - motor case
  - VESC heat sink

## Safety hardware

- normally-closed latching emergency-stop
- DC contactor or appropriately rated relay that removes controller battery power
- 10 A fuse maximum during P1
- all exposed terminals covered
- battery remains outside the rotating guard

## Guard material

- 6 mm clear polycarbonate around rotor plane
- source may be local plastics supplier or fabricated enclosure
- do not substitute acrylic

## Fabricated parts

1. Rotor disk:
   - 6061-T6
   - 200.0 mm OD
   - 6.0 mm thick
   - final hole pattern per HUB_AND_ROTOR_DRAWING.md

2. Custom two-flange clamp hub:
   - aluminum 6061-T6
   - symmetrical rotor capture
   - 12 mm shaft bore
   - detailed in HUB_AND_ROTOR_DRAWING.md

3. Motor adjustment plate:
   - slotted mounting plate providing center-distance adjustment around 118.3 mm

## Procurement status

The electrical drive, belt, bearings, battery, shaft, guard material, and sensors are commercially available classes.
The only custom-machined precision components are:
- rotor disk
- rotor clamp-hub pair
- motor adjustment plate

Those are fully dimensioned in this release.
