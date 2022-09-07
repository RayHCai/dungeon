import os
import json
import time
import hashlib
import winshell
import threading
from datetime import datetime
from getpass import getpass
from pathlib import Path

dungeon_path = os.path.join(
    Path(
        os.path.dirname(__file__)
    ).parent, '__thedungeon'
)

user_info_path = os.path.join(
    Path(
        os.path.dirname(__file__)
    ).parent, '_secrets/user_info.json'
)

# TODO: add multi authentication with email, access codes? face req?
def login(): 
    '''
    Helper method to login a user

    Returns:
        whether or not the user has proper credentials to be logged in: boolean
    '''

    username = input('Username: ')
    email = input('Email: ')
    password = getpass('Password: ')

    with open(user_info_path) as user_info_json:
        user_info = json.load(user_info_json)

        _username = user_info.get('username')
        _email = user_info.get('email')
        _password = user_info.get('password')

        hashed_password = gen_hash(base_string=password)

        if _username != username or _email != email or hashed_password != _password:
            print('Access denied, incorrect credidentials. If you wish to reset them, please run dungeon conceive --recred')

            return False

    return True

def gen_hash(base_string=None):
    '''
    Helper method to generate a sha512 hash

    Args:
        base_string?: string

    Returns:
        hashed time or base_string: string
    '''

    if not base_string: # if there is no string specified, hash current time
        base_string = datetime.now().strftime('%Y-%m-%d-%H-%M-%S.%f')

    return hashlib.sha512(
        base_string.encode()
    ).hexdigest()

def wipe_user_creds():
    '''
    Helper method to delete user credentials
    '''

    with open(user_info_path, 'w') as user_info_json:
        user_info_json.write(
            json.dumps({})
        )

def empty_recycle_bin():
    '''
    Helper method to empty recycle bin
    '''
    
    try:
        winshell.recycle_bin().empty(confirm=False, show_progress=False, sound=False)
    except:
        pass
