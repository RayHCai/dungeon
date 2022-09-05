import os
from pathlib import Path

from dungeon_base import helpers, errors

class Unlock:
    '''
    Unlock command class
    '''

    description = 'Open current instance of dungeon'

    dungeon_path = os.path.join(
        Path(
            os.path.dirname(__file__)
        ).parent, '__thedungeon'
    )

    def run(self):
        '''
        Base run method for command

        Raises:
            DungeonDoesNotExist: user tries opening a dungeon that does not exist
        '''
        
        try:
            if not helpers.login():
                return

            cur_subfolder = os.path.join(self.dungeon_path, os.walk(self.dungeon_path).__next__()[1][0])

            os.startfile(os.path.join(self.dungeon_path, cur_subfolder))
        except StopIteration:
            raise errors.DungeonDoesNotExist()
