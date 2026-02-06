from datetime import datetime, date
from math import isfinite
from time import strftime, localtime

# Проверка корректности даты в профиле
def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, "%d.%m.%Y")
        return True
    except ValueError:
        return False

def get_true_date(date_str: str) -> date:
    return datetime.strptime(date_str, "%d.%m.%Y").date()
    
# Берём нынешнюю дату
def date_now():
    time = strftime("%d/%m/%y",localtime())
    return time

def validate_num(num: str) -> bool:
    try:
        x = float(num)
        return x >= 0 and isfinite(x)
    except ValueError:
        return False