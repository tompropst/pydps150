import sys
import time

import matplotlib.pyplot as plt
from pydps150.PyDps150 import PyDps150

def main(dps):
    # 測定パラメータ
    duration = 5.0      # 測定時間 [秒]
    interval = 0.1      # 測定間隔 [秒]
    steps = int(duration / interval)

    # DPS 初期化と設定
    dps.vset(0.0)
    dps.iset(0.5)
    input("豆電球を接続してください。Enterで開始 > ")

    # 電圧印加
    dps.vset(2.0)

    # 計測開始
    times = []
    currents = []
    start = time.time()

    for i in range(steps + 1):
        now = time.time()
        t = now - start
        times.append(t)

        current = dps.iget()
        currents.append(current if current is not None else 0.0)

        sleep_target = start + (i + 1) * interval
    #    time.sleep(max(0, sleep_target - time.time()))

    # 電圧OFF
    dps.vset(0.0)
    dps.close()

    # グラフ表示
    plt.plot(times, currents, marker='o')
    plt.title("Current Response Over Time (2V Step)")
    plt.xlabel("Time [s]")
    plt.ylabel("Current [A]")
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        port = "/dev/ttyACM0"
    else:
        port = sys.argv[1]

    dps = PyDps150(port=port)
    main(dps)
