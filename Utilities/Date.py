from datetime import datetime

def get_date(add_minutes=False):
    if add_minutes:
        date = datetime.now().strftime("%d-%m-%Y %H:%M")
    else:
        date = datetime.now().strftime("%d-%m-%Y")
    return date