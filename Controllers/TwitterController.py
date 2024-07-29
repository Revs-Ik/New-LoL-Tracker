from conf import *
from Models.UserModel import User
from ExternalAPIS.RiotAPI import get_user_info

import tweepy, random, os

class TwitterController:
    def __init__(self) -> None:
        self.client = tweepy.Client(BEARER_TOKEN, API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.auth = tweepy.OAuth1UserHandler(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)

    def convert_to_fancy_format(self, input_string):
        output_string = ""
        for char in input_string:
            if char.isdigit():
                # Convert digits to mathematical bold digits
                output_string += chr(ord('𝟬') + int(char))
            elif char.isalpha():
                # Convert letters to mathematical sans-serif bold letters
                offset = ord('𝗔') - ord('A') if char.isupper() else ord('𝗮') - ord('a')
                output_string += chr(ord(char) + offset)
            else:
                # Keep non-alphanumeric characters as they are
                output_string += char

        return output_string

    def new_updates(user: User):
        """ Checks for updates on user's rank """
        json_data = get_user_info(user.summonerId)
        for entry in json_data:
            if entry['queueType'] == 'RANKED_SOLO_5x5':
                lp = entry['leaguePoints'] 
                rank = f"{entry['tier'].upper()} {entry['rank'].upper()}"
                losses = entry['losses']

                return lp, rank, losses
    
    def post_tweet(self, display_name, difference, new_lp, new_rank, winstreak, lost):
        rank_parts = new_rank.split(' ')
        
        if new_rank not in ['MASTER I', 'GRANDMASTER I', 'CHALLENGER I']:
            text = f'{rank_parts[0].capitalize()} {rank_parts[1]} {new_lp} LP'
        else:
            text = f'{rank_parts[0].capitalize()} {new_lp} LP'
            
        formatted_rank = self.convert_to_fancy_format(text)
        emoji_rand = random.choice(LOSE_EMOJIS)
        
        # DODGE
        if (difference == -5 or difference == -15) and not lost:
            formatted_diff = self.convert_to_fancy_format(f'{(difference*-1)} LP')
            message = f'{display_name} dodged and lost {formatted_diff} ❌ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

        # LOSE
        elif difference < 0:
            formatted_diff = self.convert_to_fancy_format(f'{(difference*-1)} LP')

            global demo
            if demo:
                message = f'{display_name} unsurprisingly lost {formatted_diff} ❌ \nGOT DEMOTED TO {formatted_rank} HAHAHAH {emoji_rand}\n'
            else:
                message = f'{display_name} unsurprisingly lost {formatted_diff} ❌ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

        # WIN
        elif difference > 0:
            formatted_diff = self.convert_to_fancy_format(f'{difference} LP')
            emoji_rand = random.choice(WIN_EMOJIS)
            
            global promo
            if promo:
                message = f'{display_name} somehow gained {formatted_diff} ✅\nPROMOTED TO {formatted_rank} GGS {emoji_rand}\n'
            else:
                message = f'{display_name} somehow gained {formatted_diff} ✅ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

        elif difference == 0:
            emoji_rand = random.choice(NOLP_EMOJIS)
            message = f'{display_name} can\'t even lose more lp ❌ \nCurrent rank is {formatted_rank} {emoji_rand}\n'
            
        # ADD WINSTRIAK
        if winstreak > 1 and (difference > 0 or lost):
            parts = message.split('\n')
            message = f'{parts[0]}\n{parts[1]}\n🔥 Winstreak {winstreak} 🔥\n'
        if winstreak < -1 and (difference > 0 or lost):
            parts = message.split('\n')
            message = f'{parts[0]}\n{parts[1]}\n♿ Loss Streak {winstreak*-1} ♿\n'
        
        # Upload media
        #media = self.api.media_upload(os.path.join(IMG_DIR, 'elm_banner.png'))
        # Post tweet
        #tweet = self.client.create_tweet(text=message, media_ids=[media.media_id])
        # Create a reply to the initial tweet
        #self.client.create_tweet(text="kick.com/elmiillor", in_reply_to_tweet_id=tweet.data['id'])
        
        print(f'Tweet Posted:\n{message}\n')