from __future__ import annotations
import argparse, csv, time
from pathlib import Path
import serial

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--port", required=True)
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--seconds", type=float, default=600)
    ap.add_argument("--out", default="results/p0_acceptance_log.csv")
    args=ap.parse_args()

    out=Path(args.out); out.parent.mkdir(parents=True, exist_ok=True)
    end=time.time()+args.seconds
    with serial.Serial(args.port,args.baud,timeout=1) as ser, out.open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f)
        w.writerow(["host_time","device_line"])
        while time.time()<end:
            line=ser.readline().decode(errors="replace").strip()
            if line:
                w.writerow([time.time(),line])
                print(line)
    print(f"Wrote {out}")

if __name__=="__main__":
    main()
