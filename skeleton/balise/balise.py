# Balise (balise) — ERTMS T5
BALISE_ID = 'balise'
POSITION_M = 12500


def transmit():
    return {
        'balise_id': BALISE_ID,
        'position_m': POSITION_M,
        'track_id': 'CORRIDOR-A',
        'signal': 'EUROBALISE-STM'
    }


if __name__ == '__main__':
    print('[BALISE]', transmit())
