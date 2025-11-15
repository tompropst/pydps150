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

def make_power_off_packet():
    return bytes([0xF1, 0xB1, 0xDB, 0x00, 0xDB])  # 出力Off

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

            # OE 交互に送信
            for i in range(10):
                send_packet(ser, "出力Off", make_power_off_packet())
                time.sleep(1)
                send_packet(ser, "出力On", make_power_on_packet())
                time.sleep(1)

            print("✅ 終了しました")

    except serial.SerialException as e:
        print(f"❌ シリアルポートエラー: {e}")

if __name__ == "__main__":
    main()

