import re
from time import sleep
from datetime import datetime, timedelta

def GetDate(year, month):
    first_october = datetime(year, month, 1)

    while first_october.weekday() != 2:  
        first_october += timedelta(days=1)

    second_wednesday_october = first_october + timedelta(days=7)

    second_wednesday_october_date = second_wednesday_october.strftime('%d/%m/%Y')

    return second_wednesday_october_date
