# GPRS Unit (modem) — ERTMS T5
import time


def read_comm():
    return {
        'communication_message': 'message comm',
        'communication_state': 'OK'
    }


def send_to_ground(data):
    print(f'[GPRS modem] Sending to EVC: {data}')


def receive_command(cmd):
    print(f'[GPRS modem] Command received: {cmd}')
    if cmd.get('action') == 'BRAKE':
        send_command(cmd.get('message', 'unspecified'))


def send_command(message):
    print(f'[GPRS modem] Sending command: {message}')


if __name__ == '__main__':
    while True:
        send_to_ground(read_comm())
        time.sleep(1)
