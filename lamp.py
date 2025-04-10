import matplotlib.pyplot as plt
import time
from PyDps150 import PyDps150


def measure_iv_curve(start=0.0, stop=2.0, step=0.1, iset=0.5):
    dps = PyDps150()
    dps.power_off()
    dps.vset(0.0)
    dps.iset(iset)
    input("\n🔌 豆電球を接続してください。準備ができたら Enter キーを押してください。")
    dps.power_on()

    voltages = []
    currents = []

    v = start
    while v <= stop:
        dps.vset(v)
        time.sleep(0.4)
        measured_v = dps.vget()
        measured_i = dps.iget()
        print(f"Set: {v:.2f} V | Measured: {measured_v:.2f} V, {measured_i:.2f} A")
        voltages.append(measured_v)
        currents.append(measured_i)
        v += step

    dps.vset(0.0)
    dps.power_off()
    dps.close()

    return voltages, currents


def plot_iv_curve(voltages, currents):
    plt.figure(figsize=(8, 5))
    plt.plot(voltages, currents, marker='o')
    plt.title("IV Curve of Incandescent Bulb")
    plt.xlabel("Voltage [V]")
    plt.ylabel("Current [A]")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    voltages, currents = measure_iv_curve()
    plot_iv_curve(voltages, currents)

