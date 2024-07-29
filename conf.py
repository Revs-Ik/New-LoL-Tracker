from dotenv import load_dotenv
import json, os

load_dotenv()

# KEYS
API_KEY = os.getenv('X_API_KEY')
API_SECRET = os.getenv('X_API_SECRET')
BEARER_TOKEN = os.getenv('X_BEARER_TOKEN')
ACCESS_TOKEN = os.getenv('X_ACCESS_TOKEN')
ACCESS_TOKEN_SECRET = os.getenv('X_ACCESS_TOKEN_SECRET')
CLIENT_ID = os.getenv('X_CLIENT_ID')
CLIENT_SECRET = os.getenv('X_CLIENT_SECRET')

# PARAM
DATA_FILE   = 'data/usersdata.json'
IMG_DIR     = 'data/img'
USERS       = json.load(open(DATA_FILE, 'r', encoding='utf-8'))

WIN_EMOJIS  = '🤪😎🤑🤓🥸😏🫡😬🥱🤩🥵🥶👌🤙👀'
LOSE_EMOJIS = '😂🤣😅🤓🥸🤡😱🤢🤮🤒🤕💀👺😈🤧🥵🥶🤑'
NOLP_EMOJIS = '🫣🤭🫢🤣💩'
RANKS = ['IRON IV', 'IRON III', 'IRON II', 'IRON I',
         'BRONZE IV', 'BRONZE III', 'BRONZE II', 'BRONZE I',
         'SILVER IV', 'SILVER III', 'SILVER II', 'SILVER I',
         'GOLD IV', 'GOLD III', 'GOLD II', 'GOLD I',
         'PLATINUM IV', 'PLATINUM III', 'PLATINUM II', 'PLATINUM I',
         'EMERALD IV', 'EMERALD III', 'EMERALD II', 'EMERALD I',
         'DIAMOND IV', 'DIAMOND III', 'DIAMOND II', 'DIAMOND I',
         'MASTER I', 'GRANDMASTER I', 'CHALLENGER I'
        ]