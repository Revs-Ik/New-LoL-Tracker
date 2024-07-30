from Models.UserModel import User
from Controllers.TwitterController import TwitterController
from conf import USERS

import time

def main():
    twitter = TwitterController()
    
    while True:
        for i, user_dic in enumerate(USERS):
            print("-> Starting")
            user = User(**user_dic)
            updated_user = user.check_updates()

            if (user.leaguePoints != updated_user.leaguePoints or
                user.losses       != updated_user.losses):
                
                twitter.post_tweet(user, updated_user)
                
                updated_user.save_to_json()
                USERS[i] = updated_user.to_dict()
                
        time.sleep(10)

if __name__ == "__main__":
    main()