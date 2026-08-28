# P1 Test Plan

## Test 0 — inspection
- guard installed
- rotor/hub witness marks applied
- shaft collars secure
- E-stop verified at zero speed
- independent tachometer agrees with controller RPM at hand/slow rotation

## Test 1 — incremental spin
250, 500, 750, 1000, 1250, 1500 RPM.
Hold 30 s each.
Stop immediately for rubbing, growing vibration, visible hub migration, bearing heating, or sensor disagreement >5%.

## Test 2 — coast-down
Spin to 1500 RPM.
Command zero torque.
Log RPM vs time to 300 RPM.
Repeat 5 times.
Coefficient of variation of coast-down time should be <10%.

## Test 3 — regenerative discharge
Spin to 1500 RPM.
Command a conservative regenerative current ramp until 300 RPM.
Measure recovered DC energy.
Repeat 5 times.

Success criterion:
- regeneration is stable and repeatable
- no DC-bus overvoltage
- recovered energy is measurably positive
- no mechanical fault

## Test 4 — 20-cycle durability
20 cycles between 300 and 1500 RPM.
Record:
- E_in
- E_out
- efficiency
- peak vibration
- peak motor/controller/bearing temperatures

## What this prototype decides

If P1 cannot achieve stable charge/discharge and repeatable coast-down at only ~31 J, stop commercial-scale development and fix the drivetrain/control architecture.

If it passes, next prototype is P2: the same single-rotor energy loop with reduced windage and bearing losses, first through an enclosure/vacuum-loss study and later through non-contact bearing work.
