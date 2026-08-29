// P0 three-zone differential hoop assembly envelope
// Low-energy benchtop geometry only; not a high-speed structural design.
//
// This model is constrained to the Manufacturing Release v1 envelope:
// - 450 x 450 x 10 mm base
// - 300/270, 240/210, 180/150 x 6 mm polycarbonate rotors
// - >=18 mm clear axial gap between rotating surfaces
// - >=25 mm radial guard clearance from the largest rotor
//
// Bearing bolt patterns and rotor-to-bearing carrier details remain field-fit to
// the selected low-speed commercial bearings and are intentionally not implied
// by this envelope model.

$fn = 180;

base_x = 450;
base_y = 450;
base_z = 10;
plate_t = 5;
rotor_t = 6;
minimum_surface_gap = 18;
nominal_surface_gap = 24;
level_pitch = rotor_t + nominal_surface_gap; // 30 mm center/bottom-plane pitch

guard_id = 380;
guard_wall = 3;
guard_od = guard_id + 2 * guard_wall;
guard_height = 145;

rotor_specs = [
    [300, 270, rotor_t],
    [240, 210, rotor_t],
    [180, 150, rotor_t]
];

module ring(od, id, h) {
    difference() {
        cylinder(d=od, h=h);
        translate([0,0,-1]) cylinder(d=id, h=h+2);
    }
}

module support_plate(z, window_d=330) {
    // Stationary envelope plate only. The selected bearing/carrier must bridge
    // this plate to the rotor without entering the neighboring swept volume.
    translate([-base_x/2, -base_y/2, z])
    difference() {
        cube([base_x, base_y, plate_t]);
        translate([base_x/2, base_y/2, -1])
            cylinder(d=window_d, h=plate_t+2);
    }
}

module motor_placeholder(radius, z) {
    // 25 mm-class gearmotor envelope with a small friction-wheel allowance.
    translate([radius + 18, 0, z + rotor_t/2])
        rotate([0,90,0])
            cylinder(d=28, h=55, center=true);
}

color("dimgray")
translate([-base_x/2, -base_y/2, 0])
    cube([base_x, base_y, base_z]);

first_rotor_z = base_z + 20;

for (i=[0:2]) {
    z = first_rotor_z + i*level_pitch;

    // Keep stationary support structure below its rotor plane. Exact bearing
    // geometry is procurement-dependent and is not frozen by this file.
    support_plate(z - plate_t - 3, rotor_specs[i][0] + 24);

    color(i==0 ? "deepskyblue" : (i==1 ? "orange" : "limegreen"))
        translate([0,0,z])
            ring(rotor_specs[i][0], rotor_specs[i][1], rotor_specs[i][2]);

    color("silver")
        motor_placeholder(rotor_specs[i][0]/2, z);
}

// Transparent 3 mm-wall guard. 380 mm ID gives 40 mm radial clearance to the
// 300 mm OD largest rotor, exceeding the 25 mm release minimum.
color([0.5,0.8,1.0,0.15])
translate([0,0,base_z + guard_height/2])
difference() {
    cylinder(d=guard_od, h=guard_height, center=true);
    cylinder(d=guard_id, h=guard_height+2, center=true);
}
