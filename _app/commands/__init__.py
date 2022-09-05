class Commands:
    '''
    Commands master class
    '''

    def gen_conceive_command(self):
        from . import conceive

        return conceive.Conceive()

    def gen_lock_command(self):
        from . import lock

        return lock.Lock()

    def gen_unlock_command(self):
        from . import unlock

        return unlock.Unlock()

    def help(self, obj):
        '''
        Help sub command for all commands. Prints out a list of all sub commands on command object

        Args:
            obj: command object
        '''
        
        avaliable_sub_commands = []

        for attr in dir(obj):
            if not callable(getattr(obj, attr)) or attr.startswith('_') or attr == 'run': # if it is not a function, is private method, or is the base run method 
                continue

            avaliable_sub_commands.append(attr)

        print(obj.description, '\n\n', 'Sub commands-')

        for sub_command in avaliable_sub_commands:
            print('\n   ', sub_command)
