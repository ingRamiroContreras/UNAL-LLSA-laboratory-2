# GPS (gps_galileo) — ERTMS T5
GPS_ID = 'gps_galileo'
LATITUDE = '-121212121'
LONGITUDE = '-3434343434'


def transmit():
    return {
        'gps_id': GPS_ID,
        'latitude': LATITUDE,
        'longitude': LONGITUDE
    }


if __name__ == '__main__':
    print('[GPS]', transmit())
