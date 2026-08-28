// P0 three-zone differential hoop assembly mockup
// Low-energy benchtop geometry only; not a high-speed structural design.

$fn = 180;

base_x = 440;
base_y = 440;
base_z = 12;
plate_t = 5;
level_gap = 22;

rotor_specs = [
    [300, 270, 6],
    [240, 210, 6],
    [180, 150, 6]
];

module ring(od, id, h) {
    difference() {
        cylinder(d=od, h=h);
        translate([0,0,-1]) cylinder(d=id, h=h+2);
    }
}

module support_plate(z, window_d=330) {
    translate([-base_x/2, -base_y/2, z])
    difference() {
        cube([base_x, base_y, plate_t]);
        translate([base_x/2, base_y/2, -1])
            cylinder(d=window_d, h=plate_t+2);
    }
}

module motor_placeholder(radius, z) {
    translate([radius + 32, 0, z + 3])
        rotate([0,90,0])
            cylinder(d=28, h=55);
}

color("dimgray")
translate([-base_x/2, -base_y/2, 0])
    cube([base_x, base_y, base_z]);

for (i=[0:2]) {
    z = base_z + 10 + i*level_gap;
    support_plate(z-5, rotor_specs[i][0] + 24);

    color(i==0 ? "deepskyblue" : (i==1 ? "orange" : "limegreen"))
        translate([0,0,z])
            ring(rotor_specs[i][0], rotor_specs[i][1], rotor_specs[i][2]);

    color("silver")
        motor_placeholder(rotor_specs[i][0]/2, z);
}

// Transparent guard envelope
color([0.5,0.8,1.0,0.15])
translate([0,0,base_z + 34])
difference() {
    cylinder(d=380, h=90, center=true);
    cylinder(d=365, h=92, center=true);
}
