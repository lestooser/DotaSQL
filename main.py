import requests
import json
from datetime import datetime

PLAYER_ID = '327729645'

def fetch_match(player_id):
    url = f'https://api.opendota.com/api/players/{player_id}/matches'
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("API request failed with status code: {}".format(response.status_code))
    return response.json()

def format_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def matches_formating(matches):
    for match in matches:
        if 'duration' in match:
            match['duration'] = match['duration'] // 60  # Convert seconds to minutes
        if 'start_time' in match:
            match['start_time'] = format_timestamp(match['start_time'])

if __name__ == "__main__":
    try:
        matches = fetch_match(PLAYER_ID)
        matches_formating(matches)
        print(json.dumps(matches[:5], indent=2))
    except Exception as e:
        print(f"Error fetching matches: {e}")