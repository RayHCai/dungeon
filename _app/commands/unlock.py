import os

from dungeon_base import helpers, errors
from dungeon_base.helpers import DUNGEON_PATH

class Unlock:
    '''
    Unlock command class
    '''

    description = 'Open current instance of dungeon'

    def run(self):
        '''
        Base run method for command

        Raises:
            DungeonDoesNotExist: user tries opening a dungeon that does not exist
        '''
        
        try:
            if not helpers.login():
                return

            cur_subfolder = os.path.join(DUNGEON_PATH, os.walk(DUNGEON_PATH).__next__()[1][0])

            os.startfile(os.path.join(DUNGEON_PATH, cur_subfolder))
        except StopIteration:
            raise errors.DungeonDoesNotExist()
