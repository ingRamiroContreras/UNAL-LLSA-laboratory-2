# ERTMS Data Lake ingestion — dl
import json
import datetime


def ingest(event: dict):
    record = {
        'timestamp': datetime.datetime.utcnow().isoformat(),
        'payload': event
    }
    print(json.dumps(record))


if __name__ == '__main__':
    ingest({'train_id': 'T-001', 'position': '48.8566,2.3522', 'speed_kmh': 220})
