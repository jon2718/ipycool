import ICoolObject


class Container(ICoolObject):

    """Abstract class container for other commands.
    """

    def __init__(self, enclosed_commands=None):
        if enclosed_commands is None:
            self.enclosed_commands = []
        else:
            if self.check_allowed_enclosed_commands(enclosed_commands):
                self.enclosed_commands = enclosed_commands

    def __setattr__(self, name, value):
        # command_parameters_dict = self.command_params
        if name == 'enclosed_commands':
            object.__setattr__(self, name, value)
        else:
            if not self.check_command_param(name):
                return False
            else:
                if not self.check_command_param_type(name, value):
                    return False
                else:
                    object.__setattr__(self, name, value)
                    return True

    def __str__(self):
        ret_str = ''
        for command in self.enclosed_commands:
            ret_str += str(command)
        return ret_str

    def add_enclosed_command(self, command):
        if self.check_allowed_enclosed_command(command) is False:
            sys.exit(0)
        else:
            self.enclosed_commands.append(command)

    def insert_enclosed_command(self, command, insert_point):
        if self.check_allowed_command(command) is False:
            sys.exit(0)
        else:
            self.enclosed_commands.insert(insert_point, command)

    def remove_enclosed_command(self, delete_point):
        del self.enclosed_commands[delete_point]

    def check_allowed_enclosed_command(self, command):
        try:
            if command.__class__.__name__ not in self.allowed_enclosed_commands:
                raise ie.ContainerCommandError(
                    command,
                    self.allowed_enclosed_commands)
        except ie.ContainerCommandError as e:
            print e
            return False
        return True

    def check_allowed_enclosed_commands(self, enclosed_commands):
        pass

    def gen_for001(self, file):
        for command in self.enclosed_commands:
            print 'Command is: ', command
            if hasattr(command, 'gen_for001'):
                command.gen_for001(file)
            else:
                file.write(self.for001_str_gen(command))


class ICoolNameList(ICoolObject):

    def gen_for001(self, file):
        name = self.__class__.__name__.lower()
        file.write('&')
        file.write(name)
        file.write(' ')
        count = 0
        items_per_line = 5
        for key in self.command_params:
            if hasattr(self, key):
                file.write(str(key))
                file.write('=')
                file.write(self.for001_str_gen(getattr(self, key)))
                file.write(' ')
                count = count + 1
                if count % items_per_line == 0:
                    file.write('\n')
        file.write('/')
        file.write('\n')


class ICoolNameListContainer(ICoolNameList, Container):

    def gen_for001(self, file):
        ICoolNameList.gen_for001(self, file)
        Container.gen_for001(self, file)

