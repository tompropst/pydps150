# PyDps150.py は FNRISI DPS-150 CNC電源装置を制御する Python3 Library です。
ライブラリ `PyDps150` を以下の通り整理し、完成させました：

### クラス: `PyDps150`

#### 初期化
```python
device = PyDps150("/dev/ttyACM0")
```

#### メソッド
- `vset(voltage: float)`：出力電圧設定
- `iset(current: float)`：出力電流設定
- `vget() -> float`：出力電圧取得
- `iget() -> float`：出力電流取得
- `power_on()`：出力開始
- `power_off()`：出力停止
- `close()`：シリアルポートを閉じる

#### 例
```python
dps = PyDps150()
dps.vset(3.3)
dps.iset(1.0)
print("Voltage:", dps.vget())
print("Current:", dps.iget())
dps.close()
```

エラー以外の出力は削除してあり、スクリプト等から静かに利用できます。
