from Models.UserModel import User
from Utilities.Logger import Logger
from conf import *

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

    def check_rank(self, lp_diff, saved_rank, new_rank, winstreak, lost):
        """ Old code reused (sorry) """
        # NO RANK CHANGE (just lp)
        if new_rank == saved_rank:
            # IF LOSE
            if lost:
                if winstreak >= 0:
                    winstreak = -1
                else:
                    winstreak += -1
            # IF WIN
            elif lp_diff > 0:
                if winstreak <= 0:
                    winstreak = 1
                else:
                    winstreak += 1

            return {'difference': lp_diff,
                    'winstreak': winstreak,
                    'promo': False,
                    'demo': False}

        # DEMO/PROMO
        else:
            saved_rank_index = RANKS.index(saved_rank)
            demo, promo = (False, False)
            # DEMO
            if new_rank == RANKS[saved_rank_index-1]:
                if new_rank != 'GRANDMASTER I' and new_rank != 'CHALLENGER I':
                    lp_diff = int(lp_diff) - 100

                demo = True

                if winstreak >= 0:
                    winstreak = -1
                else:
                    winstreak += -1

            # PROMO
            elif new_rank == RANKS[saved_rank_index+1]:
                if new_rank != 'GRANDMASTER I' and new_rank != 'CHALLENGER I':
                    lp_diff = int(lp_diff) + 100

                promo = True

                if winstreak <= 0:
                    winstreak = 1
                else:
                    winstreak += 1

            return {'difference': lp_diff,
                    'winstreak': winstreak,
                    'promo': promo,
                    'demo': demo}

    def post_tweet(self, user: User, updated_user: User):
        difference = updated_user.leaguePoints - user.leaguePoints
        # PLEASE CHANGE THIS (once you have api key)
        if updated_user.trackedQueue == "TEMP_TFT_LoG":

            if updated_user.lastGamePlacement == None:
                raise Exception("Something went wrong. lastGamePlacement is None")

            if difference < 0: lost = True
            elif difference > 0: lost = False

            # old code. Just pass the old variables somehow to obtain the same result (it works so no more modifiying, sorry.)
            rank_json  = self.check_rank(lp_diff=difference,
                                        saved_rank=" ".join([user.tier, user.rank]),
                                        new_rank=" ".join([updated_user.tier, updated_user.rank]),
                                        winstreak=updated_user.winstreak,
                                        lost=lost)

            difference = rank_json["difference"]
            winstreak  = rank_json["winstreak"]
            promo      = rank_json["promo"]
            demo       = rank_json["demo"]

            # !!!!!!!!!! VERY IMPORTANT !!!!!!!!!!
            # We modify the new winstreak of the updated_user here. It will be stored into json by the main later.
            # (I know this shouldnt be done here lol - UPDATE NECESSSARY)
            updated_user.winstreak = winstreak

            if updated_user.tier not in ['MASTER', 'GRANDMASTER', 'CHALLENGER']:
                text = f'{updated_user.tier.capitalize()} {updated_user.rank} {updated_user.leaguePoints} LP'
            else:
                text = f'{updated_user.tier.capitalize()} {updated_user.leaguePoints} LP'

            translated_text = (text.replace("Iron", "Hierro")
                              .replace("Bronze", "Bronce")
                              .replace("Silver", "Plata")
                              .replace("Gold", "Oro")
                              .replace("Platinum", "Platino")
                              .replace("Emerald", "Esmeralda")
                              .replace("Diamond", "Diamante")
                              #.replace("Master", "Maestro")
                              #.replace("Grandmaster", "Gran Maestro")
                              #.replace("Challenger", "Aspirante")
                              )
            
            formatted_rank = self.convert_to_fancy_format(translated_text)
            emoji_rand = random.choice(LOSE_EMOJIS)
            random_img = os.path.join(LOSE_IMG_DIR, random.choice(os.listdir(LOSE_IMG_DIR)))

            # LOSE
            if difference < 0:
                formatted_diff = self.convert_to_fancy_format(f'{(difference*-1)} LP')

                if demo:
                    message = f'{updated_user.displayName} ha quedado Top {updated_user.lastGamePlacement}  -{formatted_diff} ❌ \nDemotea a {formatted_rank}  ‎ F 😔🙏 \n'
                else:
                    message = f'{updated_user.displayName} ha quedado Top {updated_user.lastGamePlacement}  -{formatted_diff} ❌ \nElo actual {formatted_rank} {emoji_rand}\n'

            # WIN
            elif difference > 0:
                formatted_diff = self.convert_to_fancy_format(f'{difference} LP')
                emoji_rand = random.choice(WIN_EMOJIS)
                random_img = os.path.join(WIN_IMG_DIR, random.choice(os.listdir(WIN_IMG_DIR)))

                if promo:
                    message = f'{updated_user.displayName} ha quedado Top {updated_user.lastGamePlacement}  +{formatted_diff} ✅\nPromo a {formatted_rank} GGS {emoji_rand}\n'
                else:
                    message = f'{updated_user.displayName} ha quedado Top {updated_user.lastGamePlacement}  +{formatted_diff} ✅ \nElo actual {formatted_rank} {emoji_rand}\n'

            # 0LP FLOOR LOSE
            elif difference == 0:
                emoji_rand = random.choice(NOLP_EMOJIS)
                message = f'{updated_user.displayName} ha perdido en 0 LP (Top {updated_user.lastGamePlacement}) ❌ \nElo actual {formatted_rank} {emoji_rand}\n'

            # CHECK 3 STARTS CHAMPS
            maxxedLegendaryChamps = []
            for unit in updated_user.lastMatchData["info"]["units"]:
                if unit["rarity"] == 6 and unit["tier"] == 3:
                    maxxedLegendaryChamps.append(f'{unit["id"].split("_")[1]} ⭐⭐⭐')
                    
            if difference > 0:
                message += f'Abusando de {"\nY ".join(maxxedLegendaryChamps)}\n'
            
            # ADD WINSTRIAK
            if winstreak > 1 and (difference > 0 or lost):
                message += f'🔥 Winstreak {winstreak} 🔥\n'

            if winstreak < -1 and (difference > 0 or lost):
                message += f'♿ Loss Streak {winstreak*-1} ♿\n'

            # Upload media
            media = self.api.media_upload(random_img)
            # Post tweet
            tweet = self.client.create_tweet(text=message, media_ids=[media.media_id])
            # Create a reply to the initial tweet
            #self.client.create_tweet(text="kick.com/elmiillor", in_reply_to_tweet_id=tweet.data['id'])

            print(f'Tweet Posted:\n{message}\n')
            Logger().logLine(f'Tweet Posted:\n{message}\n', "activity.log")
            return

        # elm old code
        elif False:
            lost = updated_user.losses - user.losses

            # old code. Just pass the old variables somehow to obtain the same result (it works so no more modifiying, sorry.)
            rank_json  = self.check_rank(lp_diff=difference,
                                        saved_rank=" ".join([user.tier, user.rank]),
                                        new_rank=" ".join([updated_user.tier, updated_user.rank]),
                                        winstreak=updated_user.winstreak,
                                        lost=lost)

            difference = rank_json["difference"]
            winstreak  = rank_json["winstreak"]
            promo      = rank_json["promo"]
            demo       = rank_json["demo"]

            # !!!!!!!!!! VERY IMPORTANT !!!!!!!!!!
            # We modify the new winstreak of the updated_user here. It will be stored into json by the main later.
            # (I know this should be done here lol - UPDATE NECESSSARY)
            updated_user.winstreak = winstreak

            if updated_user.tier not in ['MASTER', 'GRANDMASTER', 'CHALLENGER']:
                text = f'{updated_user.tier.capitalize()} {updated_user.rank} {updated_user.leaguePoints} LP'
            else:
                text = f'{updated_user.tier.capitalize()} {updated_user.leaguePoints} LP'

            formatted_rank = self.convert_to_fancy_format(text)
            emoji_rand = random.choice(LOSE_EMOJIS)

            # DODGE
            if (difference == -5 or difference == -15) and not lost:
                formatted_diff = self.convert_to_fancy_format(f'{(difference*-1)} LP')
                message = f'{updated_user.displayName} dodged and lost {formatted_diff} ❌ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

            # LOSE
            elif difference < 0:
                formatted_diff = self.convert_to_fancy_format(f'{(difference*-1)} LP')

                if demo:
                    message = f'{updated_user.displayName} unsurprisingly lost {formatted_diff} ❌ \nGOT DEMOTED TO {formatted_rank} HAHAHAH {emoji_rand}\n'
                else:
                    message = f'{updated_user.displayName} unsurprisingly lost {formatted_diff} ❌ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

            # WIN
            elif difference > 0:
                formatted_diff = self.convert_to_fancy_format(f'{difference} LP')
                emoji_rand = random.choice(WIN_EMOJIS)

                if promo:
                    message = f'{updated_user.displayName} somehow gained {formatted_diff} ✅\nPROMOTED TO {formatted_rank} GGS {emoji_rand}\n'
                else:
                    message = f'{updated_user.displayName} somehow gained {formatted_diff} ✅ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

            elif difference == 0:
                emoji_rand = random.choice(NOLP_EMOJIS)
                message = f'{updated_user.displayName} can\'t even lose more lp ❌ \nCurrent rank is {formatted_rank} {emoji_rand}\n'

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