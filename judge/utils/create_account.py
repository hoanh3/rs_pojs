import requests
import random
import json

url = 'http://localhost:8000/accounts/register/'

NAME_SET = [
    "Ava", 
    "Ben", 
    "Cal", 
    "Dan", 
    "Eve", 
    "Finn", 
    "Gus", 
    "Hal", 
    "Ivy", 
    "Jade", 
    "Kai", 
    "Lee", 
    "Max", 
    "Nate", 
    "Owen", 
    "Pax", 
    "Quinn", 
    "Ray", 
    "Sam", 
    "Tess", 
    "Una", 
    "Vera", 
    "Wren", 
    "Xan", 
    "Yale", 
    "Zane", 
    "Ash", 
    "Bliss", 
    "Cruz", 
    "Dove", 
    "Elan", 
    "Flint", 
    "Gage", 
    "Hale", 
    "Indie", 
    "Jazz", 
    "Knox", 
    "Lux", 
    "Mars", 
    "Noe", 
    "Oak", 
    "Poe", 
    "Quill", 
    "Rey", 
    "Sage", 
    "Tex", 
    "Vaughn", 
    "Wolf", 
    "Zeke"
]

POSTFIX_USERNAME = [
    "111", 
    "123", 
    "222", 
    "321", 
    "456", 
    "654", 
    "999", 
    "777", 
    "555", 
    "101", 
    "202", 
    "303", 
    "404", 
    "505", 
    "606", 
    "707", 
    "808", 
    "909", 
    "1111", 
    "1234"
]

STORE_COMBINATION = set()

def get_random_username():
    for i in range(len(NAME_SET)):
        for j in range(len(POSTFIX_USERNAME)):
            username = NAME_SET[i] + POSTFIX_USERNAME[j]
            if username not in STORE_COMBINATION:
                STORE_COMBINATION.add(username)

def get_middleware_key():
    INPUT_KEY = "<input type='hidden' name='csrfmiddlewaretoken' value='"
    INDEX_KEY = 12536
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        input_key_string = html_content[INDEX_KEY:12900]
        start_index_key = input_key_string.find(" value='")
        end_index_key = input_key_string.find("' />")
        return input_key_string[start_index_key+8:end_index_key]
    else:
        return None

def reg_acc_count(username):
    token = get_middleware_key()
    data = {
        "csrfmiddlewaretoken": token,
        "username": username,
        "email": f"{username}@gmail.com",
        "password1": "M@i270303",
        "password2": "M@i270303",
        "timezone": "Asia/Bangkok",
        "language": 8
    }
    
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Host": "localhost:8000",
        "Origin": "http://localhost:8000",
        "Cookie": "django_language=vi; csrftoken=" + token
    }
    
    p = requests.post(url=url, data=data, headers=headers)
    
with open("username.json", "r") as f:
    usernames = json.load(f)

for i in range(2, 20):
    reg_acc_count(usernames[i])