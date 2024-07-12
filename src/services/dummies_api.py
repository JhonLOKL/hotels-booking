import requests
from decouple import config

def hotels_dummies_request():
    url = config('HOTELS_DUMMIES_URL')

    try:
        response = requests.post(url)
        if response.status_code == 201:
            return('Request hotels dummies successful:', response.json())
        else:
            print('Request hotels dummies failed with status code:', response.status_code)
            print('Response:', response.text)
    except requests.exceptions.RequestException as e:
        print('Request exception in hotels dummies:', e)

def bedrooms_dummies_request():
    url = config('BEDROOMS_DUMMIES_URL')

    try:
        response = requests.post(url)
        if response.status_code == 201:
            return('Request bedrooms dummies successful:', response.json())
        else:
            print('Request bedrooms dummies failed with status code:', response.status_code)
            print('Response:', response.text)
    except requests.exceptions.RequestException as e:
        print('Request exception in bedrooms dummies:', e)




