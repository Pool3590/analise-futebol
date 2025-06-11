import requests
from datetime import datetime

API_KEY = "1a7545ed8e3ef9324ecb27676257391a"
BASE_URL = 'https://v3.football.api-sports.io'

headers = {
    'x-apisports-key': API_KEY
}

def get_fixtures_today():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"{BASE_URL}/fixtures?date={today}"
    response = requests.get(url, headers=headers)
    data = response.json()
    return data['response']

def main():
    fixtures = get_fixtures_today()
    for f in fixtures:
        league = f['league']['name']
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']
        print(f"Liga: {league}")
        print(f"Jogo: {home} x {away}")
        print('--------------------------')

if __name__ == "__main__":
    main()
