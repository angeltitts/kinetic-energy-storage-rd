# Current Architecture — Gen 6 Segmented Differential Hoop Cell

## Status

Concept architecture after Phase 1–3 analytical screening.

## Core structure

The primary energy store is a stack of many thin, mechanically independent, circumferential high-strength hoops.

The design intentionally separates two counts:

- **structural segmentation count:** potentially tens to hundreds of independent hoops;
- **active drive-zone count:** approximately 3–6 shared electromagnetic zones.

This is intended to preserve graceful-failure segmentation without requiring a separate bearing, inverter, and stator for every hoop.

## Primary design rules

1. No thick monolithic torus.
2. No radial matrix required to carry the full centrifugal load between hoop layers.
3. No assumption that all hoops must share the same angular velocity.
4. Multiple hoops may share a drive zone while remaining structurally independent.
5. Failure containment is based on local anti-cascade isolation, not full-energy blast armor.
6. Complete-system Wh/kg is the optimization metric.
7. The 500 Wh/kg reference case requires approximately 65% fatigue retention of a hypothetical 20 GPa material at SF=1.5 and total non-rotor mass near or below ~0.60 rotor mass.
8. The provisional containment/catcher budget is ~0.15 rotor mass.

## Functional layout

    stationary stator / control structure

      DRIVE ZONE A
        independent hoop set

      local isolation / catcher boundary

      DRIVE ZONE B
        independent hoop set

      local isolation / catcher boundary

      DRIVE ZONE C
        independent hoop set

    shared vacuum enclosure
    shared sensing
    magnetic/HTS suspension remains optional pending later mass-budget validation

## Safety architecture

Expected response hierarchy:

1. detect abnormal vibration/displacement;
2. command regenerative/electromagnetic deceleration where control remains available;
3. confine a local hoop event with nearby catcher/isolation structure;
4. prevent propagation to neighboring hoops/drive zones;
5. shut down the affected module.

The architecture does not assume that an electrical dump will always occur before a sudden hoop failure. Structural segmentation must therefore provide meaningful protection even without warning.

## Current unresolved blockers

- macroscale long-life 20 GPa-class structural material;
- ~2.4 km/s rotordynamics at the 500 Wh/kg gate;
- local failure isolation without cascade;
- containment/catcher <=~0.15 rotor mass;
- entire non-rotor system <=~0.60 rotor mass;
- practical low-loss drive and suspension architecture.

## Current prototype path

- P0: differential hoop dynamics rig
- P1: segmented isolation/capture rig
- P2: low-energy contactless zone-drive rig

The project should not proceed to high-energy rotor testing until these low-energy architectural questions survive experimental validation.