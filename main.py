import requests
import json

PLAYER_ID = '327729645'

def fetch_match(player_id):
    url = f'https://api.opendota.com/api/players/{player_id}/matches'
    headers = {"Accept": "application/json"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception("API request failed with status code: {}".format(response.status_code))
    
    return response.json()

if __name__ == "__main__":
    try:
        matches = fetch_match(PLAYER_ID)
        [match.__setitem__('duration', match['duration'] // 60) for match in matches if 'duration' in match]
        print(json.dumps(matches[:5], indent=2))
    except Exception as e:
        print(f"Error fetching matches: {e}")