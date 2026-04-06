# Onboard Unit (onboard_unit) — ERTMS T5
import time
import random


def read_sensors():
    return {
        'speed_kmh': round(random.uniform(0, 300), 1),
        'position': f'{random.uniform(40, 55):.4f}, {random.uniform(-5, 25):.4f}'
    }


def send_to_ground(data):
    print(f'[OBU onboard_unit] Sending to ground: {data}')


def receive_command(cmd):
    print(f'[OBU onboard_unit] Command: {cmd}')
    if cmd.get('action') == 'BRAKE':
        apply_brake(cmd.get('intensity', 1.0))


def apply_brake(intensity):
    print(f'[OBU onboard_unit] Brake intensity {intensity}')


if __name__ == '__main__':
    while True:
        send_to_ground(read_sensors())
        time.sleep(1)
