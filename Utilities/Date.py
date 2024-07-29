def get_date(add_minutes=False):
    from datetime import datetime
    if add_minutes:
        date = datetime.now().strftime("%d-%m-%Y %H:%M")
    else:
        date = datetime.now().strftime("%d-%m-%Y")
    return date