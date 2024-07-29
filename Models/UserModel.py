import json
import os

class User:
    def __init__(self, displayName: str, trackedQueue: str, winstreak: int, leagueId: str, queueType: str, tier: str, rank: str, summonerId: str, leaguePoints: int, wins: int, losses: int, veteran: bool, inactive: bool, freshBlood: bool, hotStreak: bool):
        self.displayName = displayName
        self.trackedQueue = trackedQueue
        self.winstreak = winstreak
        self.leagueId = leagueId
        self.queueType = queueType
        self.tier = tier
        self.rank = rank
        self.summonerId = summonerId
        self.leaguePoints = leaguePoints
        self.wins = wins
        self.losses = losses
        self.veteran = veteran
        self.inactive = inactive
        self.freshBlood = freshBlood
        self.hotStreak = hotStreak

    def win_rate(self):
        total_games = self.wins + self.losses
        if total_games == 0: return 0.00
        win_rate = (self.wins / total_games) * 100
        return round(win_rate, 2)

    def save_to_json(self, file_path):
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

    def __str__(self):
        return (f"User(displayName={self.displayName}, trackedQueue={self.trackedQueue}, winstreak={self.winstreak}, leagueId={self.leagueId}, queueType={self.queueType}, tier={self.tier}, rank={self.rank}, "
                f"summonerId={self.summonerId}, leaguePoints={self.leaguePoints}, wins={self.wins}, losses={self.losses}, "
                f"veteran={self.veteran}, inactive={self.inactive}, freshBlood={self.freshBlood}, hotStreak={self.hotStreak})")

# Example usage
if __name__ == '__main__':
    # We get this from riot api
    user_data = {'leagueId': '63812ea2-cfef-387b-9ca9-870b7ee60fa6', 'queueType': 'RANKED_SOLO_5x5', 'tier': 'MASTER', 'rank': 'I', 'summonerId': 'vq_yPe_cYJcv62pP1HGRMK0JTLfPQZPqwCGXTFDRZbbVQBJx', 'leaguePoints': 458, 'wins': 131, 'losses': 105, 'veteran': True, 'inactive': False, 'freshBlood': False, 'hotStreak': True}
    
    # Create a User instance from the data
    user = User(displayName="TESTUSER", trackedQueue="RANKED_SOLO_5x5", winstreak=0, **user_data)

    # Save the user data to a JSON file
    file_path = 'data/usersdata.json'
    user.save_to_json(file_path)

    # Print the User instance
    print(user)

    # Print the win rate
    print(f"Win Rate: {user.win_rate()}%")
