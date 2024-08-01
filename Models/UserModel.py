from ExternalAPIS.RiotAPI import get_user_info
from conf import DATA_FILE

import json, os

class User:
    def __init__(self, displayName: str, trackedQueue: str, winstreak: int,  queueType: str, tier: str, rank: str, summonerId: str, leaguePoints: int, leagueId: str = None, wins: int = None, losses: int = None, veteran: bool = None, inactive: bool = None, freshBlood: bool = None, hotStreak: bool = None, lastGamePlacement: int = None):
        self.displayName = displayName # own variable
        self.trackedQueue = trackedQueue # own variable
        self.winstreak = winstreak # own variable
        self.leagueId = leagueId # riot api variable
        self.queueType = queueType # riot api variable
        self.tier = tier # riot api variable
        self.rank = rank # riot api variable
        self.summonerId = summonerId # riot api variable
        self.leaguePoints = leaguePoints # riot api variable
        self.wins = wins # riot api variable
        self.losses = losses # riot api variable
        self.veteran = veteran # riot api variable
        self.inactive = inactive # riot api variable
        self.freshBlood = freshBlood # riot api variable
        self.hotStreak = hotStreak # riot api variable
        self.lastGamePlacement = lastGamePlacement # nullable?

    def check_updates(self) -> 'User':
        """ Returns updated User object without modifiying the original. """
        # temporal until we get aproved tft api key
        if self.trackedQueue == "TEMP_TFT_LoG":
            import requests, time
            from bs4 import BeautifulSoup
            
            headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
            r = requests.get("https://www.leagueofgraphs.com/tft/summoner/euw/GSNS+Manute-MNT", headers=headers)
            soup = BeautifulSoup(r.text, "html.parser")
            
            combined_rank = soup.find("div", {"class":"leagueTier"}).text.strip().split(" ")
            leaguePoints = int(soup.find("span", {"class":"leaguePoints"}).text.strip())
            if leaguePoints != self.trackedQueue:
                time.sleep(360)
                r = requests.get("https://www.leagueofgraphs.com/tft/summoner/euw/GSNS+Manute-MNT", headers=headers)
                soup = BeautifulSoup(r.text, "html.parser")
                
            combined_rank = soup.find("div", {"class":"leagueTier"}).text.strip().split(" ")
            tier      = combined_rank[0].upper()
            rank      = combined_rank[1].upper()
            leaguePoints = int(soup.find("span", {"class":"leaguePoints"}).text.strip())
            queueType = "TEMP_TFT_LoG"
            lastGamePlacement = int(soup.find("span", {"class":"placement"}).text.strip())

            return User(
                    displayName=self.displayName,
                    trackedQueue=self.trackedQueue,
                    winstreak=self.winstreak,
                    queueType=queueType,
                    tier=tier,
                    rank=rank,
                    summonerId=self.summonerId,
                    leaguePoints=leaguePoints,
                    lastGamePlacement=lastGamePlacement,
                )
            

        # This surely works for RANKED_5X5 but might not work for tft
        json_data = get_user_info(self.summonerId)
        for entry in json_data:
            if entry['queueType'] == self.trackedQueue:
                # create a new user object mantaining (displayName, trackedQueue, winstreak) which are not provided
                # by riot api. The other variables are found in the json_data  
                # TAKE INTO ACCOUNT THAT THIS SHALL RETURN A NEW USER OBJECT WITHOUT MODIFIYING THE CURRENT.
                return User(
                    displayName=self.displayName,
                    trackedQueue=self.trackedQueue,
                    winstreak=self.winstreak,
                    leagueId=entry['leagueId'],
                    queueType=entry['queueType'],
                    tier=entry['tier'],
                    rank=entry['rank'],
                    summonerId=entry['summonerId'],
                    leaguePoints=entry['leaguePoints'],
                    wins=entry['wins'],
                    losses=entry['losses'],
                    veteran=entry['veteran'],
                    inactive=entry['inactive'],
                    freshBlood=entry['freshBlood'],
                    hotStreak=entry['hotStreak']
                )
                
        return self
    
    def win_rate(self):
        total_games = self.wins + self.losses
        if total_games == 0: return 0.00
        win_rate = (self.wins / total_games) * 100
        return round(win_rate, 2)

    def save_to_json(self, file_path=DATA_FILE):
        user_data = self.__dict__
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Read the existing data
            with open(file_path, 'r') as file:
                try:
                    users_list = json.load(file)
                except json.JSONDecodeError:
                    users_list = []
        else:
            users_list = []

        # Check if the user already exists in the list
        user_exists = False
        for i, user in enumerate(users_list):
            if user['summonerId'] == self.summonerId:
                users_list[i] = user_data
                user_exists = True
                break

        if not user_exists:
            # Append the new user data to the list
            users_list.append(user_data)

        # Write the updated list back to the file
        with open(file_path, 'w') as file:
            json.dump(users_list, file, indent=4)

    def to_dict(self):
        """ Convert the User object to a dictionary. """
        return self.__dict__
    
    def __str__(self):
        return (f"User(displayName={self.displayName}, trackedQueue={self.trackedQueue}, winstreak={self.winstreak}, leagueId={self.leagueId}, queueType={self.queueType}, tier={self.tier}, rank={self.rank}, "
                f"summonerId={self.summonerId}, leaguePoints={self.leaguePoints}, wins={self.wins}, losses={self.losses}, "
                f"veteran={self.veteran}, inactive={self.inactive}, freshBlood={self.freshBlood}, hotStreak={self.hotStreak})")
