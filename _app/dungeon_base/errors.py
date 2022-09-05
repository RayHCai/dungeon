class CommandDoesNotExist(Exception):
    '''
    Errors class for commands that don't exist
    '''

    def __init__(self, command=None, sub_command=None):
        if sub_command:
            self.error_message = f'Sub command {sub_command} does not exist on {command} command. Please run `dungeon {command} --help` for a list of avaliable sub commands.'
        else:
            self.error_message = f'Command {command} does not exist. Please run `dungeon` for a list of avaliable commands.'

        super().__init__(self.error_message)

class DungeonDoesNotExist(Exception):
    '''
    Errors class for dungeons that don't exist
    '''

    def __init__(self):
        super().__init__('Dungeon does not exist. Run `dungeon conceive` to create one.')
