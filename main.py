import requests
from datetime import datetime, timedelta

API_KEY = '1a7545ed8e3ef9324ecb27676257391a'  # Sua chave da API-Football
BASE_URL = 'https://v3.football.api-sports.io'
HEADERS = {'x-apisports-key': API_KEY}

ligas_validas = [
    39, 40,   # Inglaterra
    140, 141, # Espanha
    135, 136, # Itália
    78, 79,   # Alemanha
    61, 62,   # França
    71, 72,   # Brasil
    253       # EUA
]

def get_fixtures_today():
    today = datetime.now().strftime('%Y-%m-%d')
    url = f"{BASE_URL}/fixtures?date={today}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    # Verifica se houve erro por limite de requisições
    if 'errors' in data and 'requests' in data['errors']:
        print(f"⚠️ Erro na API: {data['errors']}")
        return None

    return data.get('response', [])

def get_odds_for_match(fixture_id):
    url = f"{BASE_URL}/odds?fixture={fixture_id}"
    response = requests.get(url, headers=HEADERS)
    data = response.json()

    # Verifica erro limite de requisições
    if 'errors' in data and 'requests' in data['errors']:
        print(f"⚠️ Erro na API (odds): {data['errors']}")
        return None

    return data.get('response', [])

def calcular_probabilidade(odd):
    try:
        return round(100 / float(odd), 2)
    except:
        return None

def main():
    todas_partidas = get_fixtures_today()
    if todas_partidas is None:
        print("Não foi possível buscar partidas hoje devido ao limite da API.")
        return

    fixtures = [f for f in todas_partidas if f['league']['id'] in ligas_validas]

    print(f"🔍 Total de partidas encontradas em ligas populares hoje: {len(fixtures)}\n")

    for f in fixtures:
        fixture_id = f['fixture']['id']
        league = f['league']['name']
        home = f['teams']['home']['name']
        away = f['teams']['away']['name']

        print(f"🏟️ {home} x {away} | {league}")

        odds_data = get_odds_for_match(fixture_id)
        if odds_data is None:
            print("   ⚠️ Não foi possível buscar odds devido ao limite da API.\n")
            continue

        odds_encontradas = False

        try:
            for bookmaker in odds_data[0]['bookmakers']:
                nome_casa = bookmaker['name']
                for bet in bookmaker['bets']:
                    if bet['name'] in ['Goals Over/Under', 'Over/Under']:
                        for valor in bet['values']:
                            if valor['value'] in ['Over 1.5', 'Under 1.5', 'Over 2.5', 'Under 2.5']:
                                prob = calcular_probabilidade(valor['odd'])
                                print(f"   🏦 {nome_casa} | {valor['value']}: Odd {valor['odd']} → Prob. {prob}%")
                                odds_encontradas = True
                if odds_encontradas:
                    break
        except Exception as e:
            print("   ❌ Erro ao processar odds:", e)

        if not odds_encontradas:
            print("   ⚠️ Odds de Over/Under 1.5/2.5 não encontradas.")

        print('--------------------------------------')

if __name__ == "__main__":
    main()

