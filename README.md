# PyDps150

DPS-150 Programmable Power Supply Controller via Python  
DPS-150をPythonから制御するためのシンプルなライブラリです。

## Overview / 概要

This library provides basic control functions for the FNIRSI DPS-150 USB programmable power supply, such as voltage/current setting and measurement.  
本ライブラリは、FNIRSI DPS-150 USBプログラマブル電源の電圧・電流設定および測定をPythonから行うためのものです。

It is based on reverse-engineering of the USB protocol and works via PySerial.  
USBプロトコルの逆解析に基づき、PySerialを使用して通信します。

## Features / 特徴

- Set voltage and current limits / 電圧・電流制限の設定
- Read actual output voltage and current / 実出力の電圧・電流の取得
- Triangle wave generation (ramp test) / 三角波生成（ランプテスト）
- LED IV curve measurement / LEDのIV特性測定
- Motor inrush current observation / モーター突入電流の観察

## Requirements / 必要環境

- Python 3.7+
- PySerial
- Matplotlib (for graphing scripts)

```bash
pip install pyserial matplotlib
```

## Usage / 使用方法

```python
from PyDps150 import PyDps150

dps = PyDps150()
dps.vset(3.3)
dps.iset(1.0)
dps.vget()  # Returns current voltage
dps.iget()  # Returns current current
dps.close()
```

See `ramp_gen.py`, `led.py`, etc. for measurement examples.  
`ramp_gen.py` や `led.py` に使用例があります。

## Notes / 注意

- KeyLock is required before setting values. This is handled by the library internally.  
  設定値を送るにはKeyLockが必要ですが、ライブラリが自動的に処理します。
- Output ON/OFF control may produce audible POP noise on some loads.  
  一部の負荷では、出力ON/OFF時にPOPノイズが発生する場合があります。

## License

MIT License

---

This project is maintained by [fanfanlab](https://gitlab.com/fanfanlab)
```

