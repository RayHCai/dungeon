import os
from pathlib import Path

from dungeon_base import helpers, errors

class Lock:
    '''
    Lock command class
    '''

    description = 'Manually lock the dungeon.'

    dungeon_path = os.path.join(
        Path(
            os.path.dirname(__file__)
        ).parent, '__thedungeon'
    )

    def run(self):
        '''
        Base run method for command

        Raises:
            DungeonDoesNotExist: user tries to lock a dungeon that does not exist
        '''

        try:
            cur_subfolder = os.path.join(self.dungeon_path, os.walk(self.dungeon_path).__next__()[1][0])
        except StopIteration:
            raise errors.DungeonDoesNotExist()

        new_subfolder = os.path.join(self.dungeon_path, helpers.gen_hash())

        os.rename(cur_subfolder, new_subfolder)

        print('Dungeon locked.')
