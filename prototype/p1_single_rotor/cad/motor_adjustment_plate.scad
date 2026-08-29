// P1 measured-input motor adjustment plate
// Units: mm. Do not machine until the purchased motor face is measured.

$fn = 96;

plate_x = 120;
plate_y = 90;
plate_z = 6;

// Replace ONLY with as-measured incoming motor values.
motor_bolt_count = 4;
motor_bolt_circle = 38;      // placeholder, intentionally not released as vendor truth
motor_hole_d = 4.5;          // verify purchased motor fastener clearance
center_clearance_d = 16;     // verify purchased motor face/shaft boss

slot_length = 22;
slot_width = 7;
slot_x = 42;
slot_y = 30;

module capsule_slot(length, width, height) {
    hull() {
        translate([-length/2 + width/2, 0, 0]) cylinder(d=width, h=height);
        translate([ length/2 - width/2, 0, 0]) cylinder(d=width, h=height);
    }
}

module motor_pattern() {
    cylinder(d=center_clearance_d, h=plate_z+2);
    for (i=[0:motor_bolt_count-1]) {
        a = 360*i/motor_bolt_count;
        translate([
            motor_bolt_circle/2*cos(a),
            motor_bolt_circle/2*sin(a),
            0
        ]) cylinder(d=motor_hole_d, h=plate_z+2);
    }
}

difference() {
    translate([-plate_x/2, -plate_y/2, 0]) cube([plate_x, plate_y, plate_z]);

    // measured motor face pattern
    translate([0,0,-1]) motor_pattern();

    // base tensioning slots: motion parallel to pulley centerline
    for (sx=[-slot_x, slot_x], sy=[-slot_y, slot_y]) {
        translate([sx, sy, -1])
            rotate([0,0,0])
            capsule_slot(slot_length, slot_width, plate_z+2);
    }
}
