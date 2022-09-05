import os
import shutil
import ctypes
import json
import re

from pathlib import Path
from getpass import getpass

from dungeon_base import helpers, errors

from . import Commands

class Conceive:
    '''
    Conceive command class
    '''

    description = 'Create and manage current dungeon instance'

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

    def _gen_dungeon(self):
        '''
        Prviate method for creating hidden dungeon folder. Creates hidden subfolder within dungeon with random encrypted name
        '''

        dungeon_subfolder_path = os.path.join(
            self.dungeon_path, 
            helpers.gen_hash()
        )

        # make directories

        os.mkdir(self.dungeon_path)
        os.mkdir(dungeon_subfolder_path)

        # mark folders as hidden

        FILE_ATTRIBUTE_HIDDEN = 0x02
        ctypes.windll.kernel32.SetFileAttributesW(self.dungeon_path, FILE_ATTRIBUTE_HIDDEN)
        ctypes.windll.kernel32.SetFileAttributesW(dungeon_subfolder_path, FILE_ATTRIBUTE_HIDDEN)

    def run(self, sub_command=None, *args):
        '''
        Base run method for command

        Args:
            sub_command: sub command to run
            *args: any command parameters

        Raises:
            CommandDoesNotExist: user tries to run a sub command that does not exist
            ValueError: user inputs invalid credidentials
            Exception:
                - any errors that may occur while generating dungeon
        '''

        if sub_command is not None:
            if len(sub_command) < 3:
                raise errors.CommandDoesNotExist(command='conceive', sub_command=sub_command)

            sub_command = sub_command[2:] # remove -- from sub command

            if sub_command == 'help':
                Commands().help(obj=self)

                return

            try:
                self.__getattribute__(sub_command)(*args)

                return
            except AttributeError:
                raise errors.CommandDoesNotExist(command='conceive', sub_command=sub_command)

        if os.path.exists(self.dungeon_path):
            print('Dungeon already exists')
            
            return

        try:
            self._create_user_creds()
        except ValueError as e:
            raise e

        try:
            self._gen_dungeon()

            print('Successfuly built dungeon.')
        except Exception as e:
            raise e

    def _create_user_creds(self):
        '''
        Private method for creating user credidentials

        Raises: 
            ValueError: if user inputs invalid credentials
        '''

        print('Please create your credidentials. These will be used for future access to the dungeon.')

        username = input('Username: ')

        if len(username) == 0:
            raise ValueError('Username must be more than 0 characters')

        email = input('Email: ')
        
        email_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

        if not re.fullmatch(email_regex, email):
            raise ValueError('Must enter a valid email')

        while True:
            password = getpass('Password: ')
            password_retype = getpass('Retype your password: ')

            if password == password_retype:
                if len(password) < 10:
                    print('Password must be at least 10 characters long')

                    continue

                break

            print('Passwords do not match')

        with open(self.user_info_path, 'w') as user_info:
            user_data = {
                'username': username,
                'email': email,
                'password': helpers.gen_hash(base_string=password)
            }

            user_info.write(
                json.dumps(user_data)
            )

    def flush(self, *args):
        '''
        Delete current dungeon instance as well as all files in the dungeon

        Args:
            *args: sub commands
                --wipe: wipe user credidentials
        '''

        if input('Warning: this will wipe ALL files currently in the dungeon. Type y to continue: ') == 'y':
            if not os.path.exists(self.dungeon_path):
                print('Dungeon does not exist. Run dungeon conceive to build one')

                return

            if not helpers.login():
                return

            shutil.rmtree(self.dungeon_path)

            if '--wipe' in args:
                helpers.wipe_user_creds() 

            print('Dungeon flushed')
        else:
            print('Flush aborted')

    def regen(self):
        '''
        Delete current dungeon instance as well as all files in the dungeon and then create a new dungeon instance

        Raises:
            Exception: any errors that may occur while dungeon is being created
        '''

        if input('Warning: this will wipe ALL files currently in the dungeon. Type y to continue: ') == 'y':
            if not os.path.exists(self.dungeon_path):
                print('Dungeon does not exist. Run dungeon conceive to build one')

                return

            if not helpers.login():
                return

            shutil.rmtree(self.dungeon_path)

            try:
                self._gen_dungeon()

                print('Dungeon successfully reconstructed')
            except Exception as e:
                raise e
        else:
            print('Regen aborted')

    def recred(self): #TODO: need verifcation
        '''
        Change user credidentials
        
        Raises:
            ValueError: user inputs invalid credidentials
        '''

        try:
            self._create_user_creds()

            print('Credidentials reset.')
        except ValueError as e:
            raise e
