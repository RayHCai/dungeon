import sys
import os

from commands import Commands

from dungeon_base import errors

commands_master_obj = Commands()

def gen_command(command_name):
    '''
    Create command object
    
    Args:
        command_name: string

    Returns:
        command object

    Raises:
        CommandDoesNotExist: if command_name does not exist as an attribute on commands_master_obj
    '''

    try:
        return commands_master_obj.__getattribute__(f'gen_{command_name}_command')()
    except AttributeError:
        raise errors.CommandDoesNotExist(command=command_name)

def load_commands():
    '''
    Load all commands
    
    Returns:
        A list of all commands: dictionary array
            {
                path: path to the command python file
                name: name of the command
                description: description of the command
            }
    '''

    commands_directory = os.path.join(
        os.path.dirname(__file__), 'commands'
    )

    commands = {}

    for command in os.listdir(commands_directory):
        if command.startswith('_'): # ignores __pycache__ and __init__.py
            continue

        command_name = command[:-3] # remove .py extension
        
        command_path = os.path.join(
            commands_directory, f'{command_name}.py'
        )

        description = gen_command(command_name).description

        commands[command_name] = {
            'path': command_path,
            'name': command_name,
            'description': description
        }

    return commands

def devise():
    '''
    Entry point from terminal

    Raises:
        CommandDoesNotExist: if user tries to run a command that does not exist
        Exception: any errors that happen while a command is being run
    '''

    commands = load_commands()

    if len(sys.argv) == 1: # base command, displays list of comamnds and descriptions
        print('Commands')

        for command in commands:
            print()

            command_info = commands.get(command)

            print(' dungeon', command, ' ', command_info.get('description'), '\n')

        return

    command_name = sys.argv[1]

    command = commands.get(command_name) # command object

    if command is None:
        raise errors.CommandDoesNotExist(command=command_name)

    command_obj = gen_command(command_name)

    try:
        if len(sys.argv) > 2: # if there are sub commands
            command_parameters = sys.argv[2:]
        else:
            command_parameters = []

        command_obj.run(*command_parameters)
    except Exception as e:
        raise e
