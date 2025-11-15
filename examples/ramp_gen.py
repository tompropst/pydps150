import sys
import time

from pydps150.PyDps150 import PyDps150

def format_val(val, unit):
    return f"{val:.2f} {unit}" if val is not None else f"N/A {unit}"

def ramp_voltage(dps, v_min=0.0, v_max=2.0, step=0.1, delay=0.1):
    dps.iset(0.5)
    try:
        while True:
            # Ramp Up
            for voltage in [round(v_min + i * step, 2) for i in range(int((v_max - v_min) / step) + 1)]:
                dps.vset(voltage)
                time.sleep(delay)
                measured_v = dps.vget()
                measured_i = dps.iget()
                print(f"Set: {voltage:.2f} V | Measured: {format_val(measured_v, 'V')}, {format_val(measured_i, 'A')}")
    except KeyboardInterrupt:
        print("⏹️ 終了しました")
        dps.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        port = "/dev/ttyACM0"
    else:
        port = sys.argv[1]

    dps = PyDps150(port=port)
    ramp_voltage(dps)
