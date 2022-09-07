import os
import shutil
from pathlib import Path

from dungeon_base import helpers, errors

from . import Commands

class Seal:
    '''
    Seal command class
    '''

    description = 'Generate temporary folder for transfer. Once closed it will move all files from the temporary folder to the dungeon and lock it.'

    dungeon_path = os.path.join(
        Path(
            os.path.dirname(__file__)
        ).parent, '__thedungeon'
    )

    temp_folder_path = None

    def clear(self):
        '''
        Delete all temporary folders
        '''

        for file in os.listdir(os.path.dirname(__file__)):
            if file.startswith('_') and file != '__init__.py' and file != '__pycache__':
                temp_folder_path = os.path.join(os.path.dirname(__file__), file)

                shutil.rmtree(temp_folder_path)
                
        print('Temporary folders removed')

    def lock(self):
        '''
        Move all files in temporary sub folder to main dungeon

        Raises:
            DungeonDoesNotExist: user tries to access a dungeon that does not exist
        '''

        try:
            dungeon_subfolder_path = os.path.join(self.dungeon_path, os.walk(self.dungeon_path).__next__()[1][0])
        except StopIteration:
            raise errors.DungeonDoesNotExist()

        temp_folder_path = None

        for file in os.listdir(os.path.dirname(__file__)):
            if file.startswith('_') and file != '__init__.py' and file != '__pycache__':
                temp_folder_path = os.path.join(os.path.dirname(__file__), file)

                break

        if temp_folder_path is None:
            print('No temporary folder exists. Run `dungeon seal` to create one.')

            return

        file_errors = []

        for file in os.listdir(temp_folder_path):
            try:
                file_path = os.path.join(temp_folder_path, file)

                shutil.move(file_path, dungeon_subfolder_path)
            except Exception as e:
                file_errors.append(
                    {
                        'file_name': file,
                        'error': str(e)
                    }
                )

        if len(file_errors) == 0:
            shutil.rmtree(temp_folder_path)

            print('Successfuly sealed files')
        else:
            print(f'There was a problem moving these files:')  
            
            for error in file_errors:
                print(f"{error.get('file_name')} -> {error.get('error')}")
            
            print('Run `dungeon seal --lock` once you have resolved these issues')

            os.startfile(temp_folder_path)

    def run(self, sub_command=None, *args):
        '''
        Base run method for command

        Raises:
            DungeonDoesNotExist: user tries to seal files into a dungeon that does not exist
        '''

        if not helpers.login():
            return

        if sub_command is not None:
            if len(sub_command) < 3:
                raise errors.CommandDoesNotExist(command='seal', sub_command=sub_command)

            sub_command = sub_command[2:] # remove -- from sub command

            if sub_command == 'help':
                Commands().help(obj=self)

                return

            try:
                self.__getattribute__(sub_command)(*args)

                return
            except AttributeError:
                raise errors.CommandDoesNotExist(command='seal', sub_command=sub_command)

        if not os.path.exists(self.dungeon_path):
            raise errors.DungeonDoesNotExist()

        temp_folder_path = os.path.join(
            os.path.dirname(__file__),
            f'_{helpers.gen_hash()}'
        )

        os.mkdir(temp_folder_path)

        os.startfile(temp_folder_path)

        print('Subfolder created. Make sure to run `dungeon seal --lock` to move files into the dungeon.')
