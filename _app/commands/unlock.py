import os, shutil, time

from dungeon_base import helpers, errors
from dungeon_base.helpers import DUNGEON_PATH

from . import Commands

class Unlock:
    '''
    Unlock command class
    '''

    description = 'Open current instance of dungeon'

    def clear(self):
        '''
        Private method that deletes all temporary folders
        '''

        for file in os.listdir(os.path.dirname(__file__)):
            if file.startswith('_') and file != '__init__.py' and file != '__pycache__':
                temp_folder_path = os.path.join(os.path.dirname(__file__), file)

                shutil.rmtree(temp_folder_path)

    def m(self):
        '''
        Open mock dungeon instance
        '''

        temp_folder_path = os.path.join(
            os.path.dirname(__file__),
            f'_{helpers.gen_hash()}'
        )

        os.mkdir(temp_folder_path)
        os.startfile(temp_folder_path)

    def run(self, sub_command=None, *args):
        '''
        Base run method for command

        Raises:
            DungeonDoesNotExist: user tries opening a dungeon that does not exist
        '''

        if sub_command is not None:
            if len(sub_command) < 3:
                raise errors.CommandDoesNotExist(
                    command='unlock', 
                    sub_command=sub_command
                )

            sub_command = sub_command[2:] # remove -- from sub command

            if sub_command == 'help':
                Commands().help(obj=self)

                return

            try:
                self.__getattribute__(sub_command)(*args)

                return
            except AttributeError:
                raise errors.CommandDoesNotExist(
                    command='unlock', 
                    sub_command=sub_command
                )

        try:
            if not helpers.login():
                return

            cur_subfolder = os.path.join(DUNGEON_PATH, os.walk(DUNGEON_PATH).__next__()[1][0])

            os.startfile(os.path.join(DUNGEON_PATH, cur_subfolder))
        except StopIteration:
            raise errors.DungeonDoesNotExist()
