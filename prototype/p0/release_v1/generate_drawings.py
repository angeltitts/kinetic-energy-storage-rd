from pathlib import Path
import math

ROTORS=[("A",300,270),("B",240,210),("C",180,150)]

def circle(cx,cy,r,stroke="black",width=0.3):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{stroke}" stroke-width="{width}"/>'

def make_svg(name,od,id_):
    margin=20
    size=od+2*margin
    c=size/2
    svg=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}mm" height="{size}mm" viewBox="0 0 {size} {size}">']
    svg.append(circle(c,c,od/2))
    svg.append(circle(c,c,id_/2))
    svg.append(f'<line x1="{c-od/2}" y1="{c}" x2="{c+od/2}" y2="{c}" stroke="gray" stroke-width="0.2"/>')
    svg.append(f'<line x1="{c}" y1="{c-od/2}" x2="{c}" y2="{c+od/2}" stroke="gray" stroke-width="0.2"/>')
    svg.append(f'<text x="10" y="12" font-size="5">Rotor {name}: OD {od} mm / ID {id_} mm / thickness 6 mm</text>')
    svg.append('</svg>')
    return "\n".join(svg)

def main():
    out=Path(__file__).resolve().parent/"drawings"
    out.mkdir(exist_ok=True)
    for name,od,id_ in ROTORS:
        (out/f"rotor_{name}_1to1.svg").write_text(make_svg(name,od,id_),encoding="utf-8")
    print(out)

if __name__=="__main__":
    main()
