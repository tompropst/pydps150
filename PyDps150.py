import serial
import time
import struct


def float_to_bytes(fval):
    return list(struct.pack('<f', fval))


def bytes_to_float(b):
    return struct.unpack('<f', bytes(b))[0]


def calc_crc(packet_wo_crc):
    crc_data = packet_wo_crc[2:]  # cmdから末尾まで
    crc = sum(crc_data) & 0xFF
    return crc


def make_packet(cmd, data_bytes):
    packet_wo_crc = [0xF1, 0xB1, cmd, len(data_bytes)] + data_bytes
    crc = calc_crc(packet_wo_crc)
    return bytes(packet_wo_crc + [crc])


def send_packet(ser, packet):
    ser.write(packet)
    time.sleep(0.3)
    if ser.in_waiting:
        return ser.read(ser.in_waiting)
    return b''


class PyDps150:
    def __init__(self, port="/dev/ttyACM0", baudrate=115200):
        self.ser = serial.Serial(port, baudrate, timeout=1)
        self.initialize()

    def initialize(self):
        packet = bytes([0xF1, 0xC1, 0x00, 0x01, 0x01, 0x02])
        send_packet(self.ser, packet)

    def vset(self, voltage):
        packet = make_packet(0xC1, float_to_bytes(voltage))
        send_packet(self.ser, packet)

    def iset(self, current):
        packet = make_packet(0xC2, float_to_bytes(current))
        send_packet(self.ser, packet)

    def vget(self):
        volts, _ = self._read_vi()
        return volts

    def iget(self):
        _, amps = self._read_vi()
        return amps

    def _read_vi(self, retries=10):
        packet = bytes([0xFA, 0xA1, 0xC3, 0x01, 0x00, 0xC4])
        for _ in range(retries):
            resp = send_packet(self.ser, packet)
            if b'\xf0\xa1\xc3\x0c' in resp:
                idx = resp.index(b'\xf0\xa1\xc3\x0c') + 4
                try:
                    volts = bytes_to_float(resp[idx:idx+4])
                    amps = bytes_to_float(resp[idx+4:idx+8])
                    return volts, amps
                except Exception:
                    continue
            time.sleep(0.1)  # 少し待ってから再試行
        return None, None

    def close(self):
        if self.ser:
            self.ser.close()

    def power_on(self):
        packet = bytes([0xF1, 0xB1, 0xDB, 0x01, 0xDC])  # 出力ON
        send_packet(self.ser, packet)

    def power_off(self):
        packet = bytes([0xF1, 0xB1, 0xDB, 0x00, 0xDB])  # 出力Off
        send_packet(self.ser, packet)


