import serial
import struct
import time

def calc_crc(data_bytes):
    return sum(data_bytes) & 0xFF

def float_to_bytes(value):
    return list(struct.pack('<f', value))

def make_wrapped_command(sub_cmd, float_value):
    data = [sub_cmd] + float_to_bytes(float_value)
    packet_wo_crc = [0xB1] + data
    crc = calc_crc(data)
    return bytes([0xF1] + packet_wo_crc + [crc])

def make_keylock_packet():
    return bytes([0xF1, 0xC1, 0x00, 0x01, 0x01, 0x02])  # 固定形式 KeyLock

def make_power_on_packet():
    return bytes([0xF1, 0xB1, 0xDB, 0x01, 0xDC])  # 出力ON

def send_packet(ser, label, cmd_bytes):
    print(f"送信: {label} → {cmd_bytes.hex()}")
    ser.write(cmd_bytes)
    time.sleep(0.3)
    if ser.in_waiting:
        resp = ser.read(ser.in_waiting)
        print(f"✅ 応答: {resp.hex()}")
    else:
        print("⚠️ 応答なし（Timeout）")

def main():
    port = "/dev/ttyACM0"
    try:
        with serial.Serial(port, 115200, timeout=1) as ser:
            print(f"✅ ポート {port} を開きました")

            # 初期化 KeyLock と 出力ON
            send_packet(ser, "KeyLock (初期化)", make_keylock_packet())
            send_packet(ser, "出力ON", make_power_on_packet())

            # KeyLock 交互に送信
            for i in range(5):
                val = 3.3 if i % 2 else 5.0
                label = f"KeyLock({val:.2f})"
                cmd = make_wrapped_command(0xC1, val)
                send_packet(ser, label, cmd)
                time.sleep(1)

            print("✅ 終了しました")

    except serial.SerialException as e:
        print(f"❌ シリアルポートエラー: {e}")

if __name__ == "__main__":
    main()

