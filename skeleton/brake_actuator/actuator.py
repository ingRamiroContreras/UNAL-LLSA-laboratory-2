# Brake Actuator (brake_actuator) — ERTMS T5


def execute(command):
    action = command.get('action')
    intensity = command.get('intensity', 1.0)
    if action == 'BRAKE':
        print(f'[ACTUATOR brake_actuator] Brake intensity {intensity}')
    elif action == 'RELEASE':
        print(f'[ACTUATOR brake_actuator] Brake released')
    else:
        print(f'[ACTUATOR brake_actuator] Unknown command: {action}')


if __name__ == '__main__':
    execute({'action': 'BRAKE', 'intensity': 0.8})
