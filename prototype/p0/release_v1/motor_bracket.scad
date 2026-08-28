// P0 adjustable motor bracket, prototype only
$fn=64;
base_x=65;
base_y=42;
base_z=5;
slot_len=24;
slot_w=5;
motor_d=25.5;
clamp_t=5;

module slot(x,y){
    hull(){
        translate([x-slot_len/2,y, -1]) cylinder(d=slot_w,h=base_z+2);
        translate([x+slot_len/2,y, -1]) cylinder(d=slot_w,h=base_z+2);
    }
}

difference(){
    cube([base_x,base_y,base_z]);
    slot(base_x/2,10);
    slot(base_x/2,32);
}

translate([48,base_y/2,base_z])
rotate([90,0,0])
difference(){
    cylinder(d=motor_d+2*clamp_t,h=12,center=true);
    cylinder(d=motor_d,h=14,center=true);
    translate([-20,0,-10]) cube([40,30,20]);
}
