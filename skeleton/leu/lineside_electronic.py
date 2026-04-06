# Lineside Electronic (leu) — ERTMS T5
LINE_ID = 'leu'
IXL_STATE = 'CLEAR'


def transmit():
    return {
        'line_id': LINE_ID,
        'ixl_state': IXL_STATE,
        'track_id': 'CORRIDOR-A',
        'signal': 'EUROBALISE-IDENTIFIER'
    }


if __name__ == '__main__':
    print('[LINESIDE ELECTRONIC]', transmit())
