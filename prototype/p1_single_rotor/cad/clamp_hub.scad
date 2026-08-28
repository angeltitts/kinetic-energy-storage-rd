// P1 low-energy two-flange rotor hub
// Concept machining reference. Units mm.
$fn=128;

hub_od=60;
hub_t=12;
shaft_d=12.0;
pcd=44;
bolt_d=5.5;
pilot_od=24;
pilot_h=1.5;

module flange(clearance=true){
    difference(){
        union(){
            cylinder(d=hub_od,h=hub_t);
            cylinder(d=pilot_od,h=hub_t+pilot_h);
        }
        translate([0,0,-1]) cylinder(d=shaft_d,h=hub_t+pilot_h+2);
        for(a=[0:60:300]){
            translate([pcd/2*cos(a),pcd/2*sin(a),-1])
                cylinder(d=bolt_d,h=hub_t+pilot_h+2);
        }
        // visual clamp split
        translate([shaft_d/2, -1, -1])
            cube([hub_od/2+2,2,hub_t+pilot_h+2]);
    }
}
flange();
