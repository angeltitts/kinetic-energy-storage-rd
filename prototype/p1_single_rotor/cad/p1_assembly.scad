// P1 single-rotor low-energy prototype
// Manufacturing envelope only. Units: mm.
// NOT for operation above the released 1500 RPM / ~31 J command point.

$fn = 160;

base_x = 400;
base_y = 300;
base_z = 12;

rotor_d = 200;
rotor_t = 6;
shaft_d = 12;

bearing_center_spacing = 170;
bearing_block_w = 36;
bearing_block_l = 55;
bearing_block_h = 30;

guard_inner_w = 310;
guard_inner_l = 220;
guard_wall = 6;
guard_h = 170;

rotor_z = 105;

module rotor() {
    color("silver")
    translate([0,0,rotor_z])
    rotate([90,0,0])
    difference() {
        cylinder(d=rotor_d,h=rotor_t,center=true);
        cylinder(d=shaft_d+0.3,h=rotor_t+2,center=true);
    }
}

module shaft() {
    color("gray")
    translate([0,0,rotor_z])
    rotate([0,90,0])
    cylinder(d=shaft_d,h=260,center=true);
}

module bearing(x) {
    color("dimgray")
    translate([x-bearing_block_l/2,-bearing_block_w/2,base_z])
    cube([bearing_block_l,bearing_block_w,bearing_block_h]);
}

module guard() {
    color([0.4,0.75,1.0,0.18])
    translate([-guard_inner_w/2-guard_wall,
               -guard_inner_l/2-guard_wall,
               base_z+5])
    difference() {
        cube([guard_inner_w+2*guard_wall,
              guard_inner_l+2*guard_wall,
              guard_h]);
        translate([guard_wall,guard_wall,guard_wall])
        cube([guard_inner_w,
              guard_inner_l,
              guard_h]);
    }
}

module motor_placeholder() {
    color("black")
    translate([135,-25,65])
    rotate([0,90,0])
    cylinder(d=50,h=55,center=true);
}

color("lightgray")
translate([-base_x/2,-base_y/2,0])
cube([base_x,base_y,base_z]);

bearing(-bearing_center_spacing/2);
bearing(bearing_center_spacing/2);
shaft();
rotor();
motor_placeholder();
guard();
