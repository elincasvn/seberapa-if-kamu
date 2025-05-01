
import json

def get_soal(path='assets/soal.json'):
    with open(path, 'r') as f:
        return json.load(f)
