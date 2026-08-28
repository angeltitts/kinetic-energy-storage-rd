# Phase 3 Result — Segmented Containment

## Why Phase 2 creates a containment paradox

At the representative 500 Wh/kg threshold case, rotor specific energy is ~802 Wh/kg (~2.89 MJ/kg rotor), while the provisional containment budget is only ~0.15 kg per kg of rotor.

If a containment shell had to absorb the **entire rotor energy** after an instantaneous full-rotor failure, it would require an effective catcher specific-energy-absorption capability of:

    2.89 MJ/kg_rotor / 0.15 kg_catcher/kg_rotor = 19.3 MJ/kg_catcher

That is such an aggressive requirement that full-energy monolithic burst containment should be considered incompatible with the current 500 Wh/kg mass budget unless future evidence shows otherwise.

## Architectural escape: segmentation

The thin-hoop architecture offers a different safety strategy.

If the rotor is divided into N mechanically independent hoops, and a failure can be prevented from cascading into neighboring hoops, a single failed hoop contains approximately 1/N of total rotor energy.

Therefore the key safety problem changes from:

> contain the full rotor energy

to:

> guarantee that a local hoop failure remains local.

This makes **cascade prevention** the central containment mechanism.

## Required segmentation at containment ratio = 0.15

The table below is purely parametric. Catcher SEA is an assumed effective system-level energy-absorption number, not a claim about a particular material.

| Assumed effective catcher SEA | Required hoops if 1 fails | if 2 fail together | if 5 cascade | if 10 cascade |
|---:|---:|---:|---:|---:|
| 0.2 MJ/kg | 97 | 193 | 482 | 963 |
| 0.5 MJ/kg | 39 | 78 | 193 | 386 |
| 1.0 MJ/kg | 20 | 39 | 97 | 193 |
| 2.0 MJ/kg | 10 | 20 | 49 | 97 |
| 5.0 MJ/kg | 4 | 8 | 20 | 39 |

## New design insight

A large number of **structurally independent hoops** can be useful even if the machine uses only a small number of active drive zones.

This resolves the earlier conflict between:

- many hoops are desirable for graceful failure;
- hundreds of individually actuated rotors would create excessive stator/control/bearing overhead.

### Revised architecture

Use:

- many thin independent structural hoops for energy segmentation;
- only ~3–6 electromagnetic drive/control zones;
- hoops inside each zone are not radially bonded into one thick composite body;
- local catcher geometry is designed so a failed hoop cannot easily strike and trigger adjacent hoops;
- drive/control hardware is shared by a zone rather than duplicated per hoop.

Conceptually:

    DRIVE ZONE A
      hoop
      hoop
      hoop
      hoop

    isolation gap / catcher feature

    DRIVE ZONE B
      hoop
      hoop
      hoop
      hoop

    isolation gap / catcher feature

    DRIVE ZONE C
      hoop
      hoop
      hoop

## Critical qualification

Segmentation does **not** make the full rotor safe by itself.

It only helps if common-cause cascade is demonstrably unlikely.

The central failure modes now become:

- one hoop fragment striking neighboring hoops;
- local heating or magnetic disturbance triggering multiple hoops;
- control instability affecting an entire drive zone;
- bearing or housing failure causing common-mode contact;
- vacuum contamination or debris producing a cascade.

## Working prototype implication

P0 remains a three-hoop dynamics rig.

P1 should not immediately chase high speed. Instead it should add a **multi-hoop passive isolation/capture experiment at low stored energy** and verify that deliberately released local rotor energy can be trapped without destabilizing neighboring hoops.

This is a safer and more informative path than trying to prove full-energy containment.

## Current verdict

**The containment problem has not been solved, but it has been reframed into a potentially testable architecture.**

The strongest working prototype idea is now:

> a small number of independently driven concentric zones containing many mechanically independent thin hoops, with local anti-cascade catcher/isolation structures.

## Next kill question

> Can local hoop failure be prevented from propagating into neighboring hoops with catcher/isolation mass that still fits the <=0.15 rotor-mass containment budget?

If not, the 500 Wh/kg reference architecture likely fails on safety-system mass even if the CNT material target is achieved.