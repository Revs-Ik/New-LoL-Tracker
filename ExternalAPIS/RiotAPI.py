from dotenv import load_dotenv
import requests, os

load_dotenv()

api_key = os.getenv('RIOT_API_KEY')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
    "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
    "Origin": "https://developer.riotgames.com",
    "X-Riot-Token": api_key
}

def get_user_id(user_name, tag='EUW', server='europe', region='euw1'):
    api_url = f'https://{server}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{user_name}/{tag}'
    r = requests.get(api_url, headers=headers)
    puuid = r.json()['puuid']
    
    api_url = f'https://{region}.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puuid}'
    r = requests.get(api_url, headers=headers)
    return r.json()['id']

def get_user_info(summoner_id, region='euw1'):
    api_url = f'https://{region}.api.riotgames.com/lol/league/v4/entries/by-summoner/{summoner_id}'
    r = requests.get(api_url, headers=headers)
    return r.json()

if __name__ == '__main__':
    user_id = get_user_id(user_name='elmillor intacc', tag='GORDO')
    print(get_user_info(user_id))
