// P0 annular rotor generator
// Export one rotor at a time by setting od/id/thickness.

od = 300;       // mm
id = 270;       // mm
thickness = 6;  // mm
index_hole_d = 3;
index_radius = (od + id) / 4;

difference() {
    cylinder(h=thickness, d=od, $fn=240);
    translate([0,0,-1])
        cylinder(h=thickness+2, d=id, $fn=240);

    // Optional index hole for magnet/sensor marker.
    translate([index_radius,0,-1])
        cylinder(h=thickness+2, d=index_hole_d, $fn=48);
}
