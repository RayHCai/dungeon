import os

from dungeon_base import helpers, errors
from dungeon_base.helpers import DUNGEON_PATH

class Lock:
    '''
    Lock command class
    '''

    description = 'Manually lock the dungeon.'

    def run(self):
        '''
        Base run method for command

        Raises:
            DungeonDoesNotExist: user tries to lock a dungeon that does not exist
        '''

        try:
            cur_subfolder = os.path.join(DUNGEON_PATH, os.walk(DUNGEON_PATH).__next__()[1][0])
        except StopIteration:
            raise errors.DungeonDoesNotExist()

        new_subfolder = os.path.join(DUNGEON_PATH, helpers.gen_hash())

        os.rename(cur_subfolder, new_subfolder)

        print('Dungeon locked.')
