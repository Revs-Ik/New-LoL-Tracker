from Models.UserModel import User
from Controllers.TwitterController import TwitterController
from Utilities.Logger import Logger
from conf import USERS

import traceback, time

def main():
    twitterController = TwitterController()
    logger = Logger()

    while True:
        
        try:
            for i, user_dic in enumerate(USERS):
                print("-> Checking Updates for user:", user_dic["displayName"])
                user = User(**user_dic)
                updated_user = user.check_updates()

                if (user.leaguePoints != updated_user.leaguePoints or
                    user.losses       != updated_user.losses):
                    
                    twitterController.post_tweet(user, updated_user)
                    
                    updated_user.save_to_json()
                    USERS[i] = updated_user.to_dict()
        
        except Exception as e:
            logger.logLine(message=f"{str(e)}\n Traceback: {traceback.format_exc()}", logFile="error.log")
            
        time.sleep(400)

if __name__ == "__main__":
    main()