import sys
import time

import matplotlib.pyplot as plt
from pydps150.PyDps150 import PyDps150


def measure_led_iv(dps):

    try:
        dps.power_off()
        dps.iset(0.0)  # 最初は電流ゼロ
        dps.vset(2.5)  # 印加電圧を固定
        dps.power_on()
        input("🔌 LEDを接続してください（Enterで開始）")

        voltages = []
        currents = []

        current = 0.0
        step = 0.001  # 1mAステップ
        max_current = 0.02  # 20mA上限

        while current <= max_current:
            dps.iset(current)
            time.sleep(0.3)
            v = dps.vget()
            i = dps.iget()

            if v is not None and i is not None:
                voltages.append(v)
                currents.append(i)
                print(f"Set I = {current:.3f} A | V = {v:.2f} V, I = {i:.3f} A")
            else:
                print(f"⚠️ 応答なし (I = {current:.3f} A)")

            current += step

        dps.iset(0.0)
        dps.vset(0.0)
        dps.power_off()

        # グラフ表示
        plt.plot(voltages, currents, marker='o')
        plt.title("IV Curve of LED")
        plt.xlabel("Voltage [V]")
        plt.ylabel("Current [A]")
        plt.grid(True)
        plt.show()

    finally:
        dps.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        port = "/dev/ttyACM0"
    else:
        port = sys.argv[1]

    dps = PyDps150(port=port)
    measure_led_iv(dps)

