from Models.UserModel import User
from Controllers.TwitterController import TwitterController
from conf import USERS

import time

def main():
    twitter = TwitterController()
    
    while True:
        for user_dic in USERS:
            user = User()
            
            twitter.post_tweet()
            
        time.sleep(60)

if __name__ == "__main__":
    main()