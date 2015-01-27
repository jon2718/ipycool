class ICoolGenerator(object):

    def get_base_classes(self):
        base_tuple = self.__class__.__bases__
        bases_names = tuple()
        for c in base_tuple:
            bases_names += tuple([c.__name__])
        return bases_names

    def icoolgenerate_for001(self, file):
        base_classes = self.get_base_classes()
        if 'ICoolNameList' in base_classes:
            ICoolNameList.gen_for001(self, file)
            if 'Container' in base_classes:
                Container.gen_for001(self, file)
        else:
            if 'RegularRegion' or 'PseudoRegion' in base_classes:
                Region.gen_begtag(self, file)
                Region.gen_for001(self, file)
                if 'Container' in base_classes:
                    Container.gen_for001(self, file)
                Region.gen_endtag(self, file)

    def gen_begtag(self, file):
        if hasattr(self, 'begtag'):
            file.write(self.begtag)
            file.write('\n')

    def gen_endtag(self, file):
        if hasattr(self, 'endtag'):
            file.write(self.endtag)
            file.write('\n')

class ICoolObject(ICoolGenerator):

    """Generic ICOOL object providing methods for"""

    def __init__(self, kwargs):
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __call__(self, kwargs):
        if self.check_command_params_call(kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __str__(self, return_str):
        command_parameters_dict = self.command_params
        for key in command_parameters_dict:
            if hasattr(self, key):
                return_str += '\n'
                return_str += key
                return_str += ': '
                return_str += str(getattr(self, key))
        return return_str

    def __repr__(self):
        return '[ICool Object]'

    """Checks whether all required command parameters specified in __init__ are provided are valid
    for the command.
    Valid means the parameters are recognized for the command, all required parameters are provided
    and the parameters are the correct type."""

    def __setattr__(self, name, value):
        if self.check_command_param(name):
            object.__setattr__(self, name, value)
        else:
            sys.exit(0)

    def check_command_param(self, command_param):
        """
        Checks whether a parameter specified for command is valid.
        """
        command_parameters_dict = self.get_command_params()
        # Check command parameters are all valid
        try:
            if command_param not in command_parameters_dict:
                raise ie.InvalidCommandParameter(
                    command_param,
                    command_parameters_dict.keys())
        except ie.InvalidCommandParameter as e:
            print e
            return False
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_valid(
            self,
            command_params,
            command_parameters_dict):
        """Returns True if command_params are valid (correspond to the command)
        Otherwise raises an exception and returns False"""
        # command_parameters_dict = self.get_command_params()
        try:
            for key in command_params:
                if key not in command_parameters_dict:
                    raise ie.InvalidCommandParameter(
                        key,
                        command_parameters_dict)
        except ie.InvalidCommandParameter as e:
            print e
            return False
        return True

    def check_all_required_command_params_specified(
            self,
            command_params,
            command_parameters_dict):
        """Returns True if all required command parameters were specified
        Otherwise raises an exception and returns False"""
        # command_parameters_dict = self.get_command_params()
        try:
            for key in command_parameters_dict:
                if self.is_required(key, command_parameters_dict):
                    if key not in command_params:
                        raise ie.MissingCommandParameter(key, command_params)
        except ie.MissingCommandParameter as e:
            print e
            return False
        return True

    def check_command_params_type(self, command_params, command_params_dict):
        """Checks to see whether all required command parameters specified were of the correct type"""
        # command_params_dict = self.get_command_params()
        try:
            for key in command_params:
                if self.check_type(
                        command_params_dict[key]['type'],
                        command_params[key]) is False:
                    raise ie.InvalidType(
                        command_params_dict[key]['type'],
                        command_params[key].__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_param_type(self, name, value):
        """Checks to see whether a particular command parameter of name with value is of the correct type"""
        command_params_dict = self.get_command_params()
        try:
            if self.check_type(
                    command_params_dict[name]['type'],
                    value) is False:
                raise ie.InvalidType(
                    command_params_dict[name]['type'],
                    value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_init(self, command_params):
        """
        Checks whether the parameters specified for command are valid, all required parameters are
        specified and all parameters are of correct type.  If not, raises an exception.
        """
        command_parameters_dict = self.get_command_params()
        check_params = not self.check_command_params_valid(
            command_params,
            command_parameters_dict) or not self.check_all_required_command_params_specified(
            command_params,
            command_parameters_dict) or not self.check_command_params_type(
            command_params,
            command_parameters_dict)

        if check_params:
            return False
        else:
            return True

    def check_command_params_call(self, command_params):
        """
        Checks whether the parameters specified for command are valid and all required parameters exist.
        """
        command_parameters_dict = self.get_command_params()
        return self.check_command_params_valid(command_params, command_parameters_dict) and\
            self.check_command_params_type(
            command_params,
            command_parameters_dict)

    def setall(self, command_params):
        for key in command_params:
            self.__setattr__(key, command_params[key])

    def setdefault(self, command_params):
        command_params_dict = self.get_command_params()
        for key in command_params_dict:
            if key not in command_params:
                self.__setattr__(key, command_params_dict[key]['default'])

    def check_type(self, icool_type, provided_type):
        """Takes provided python object and compares with required icool type name.
        Returns True if the types match and False otherwise.
        """
        provided_type_name = provided_type.__class__.__name__
        print icool_type, provided_type_name
        if icool_type == 'Real':
            if provided_type_name == 'int' or provided_type_name == 'long' or provided_type_name == 'float':
                return True
            else:
                return False

        if icool_type == 'Integer':
            if provided_type_name == 'int' or provided_type_name == 'long':
                return True
            else:
                return False

        if icool_type == 'Logical':
            if provided_type_name == 'bool':
                return True
            else:
                return False

        if icool_type == 'Field':
            if isinstance(provided_type, Field):
                return True
            else:
                return False

        if icool_type == 'Material':
            if isinstance(provided_type, Material):
                return True
            else:
                return False

        if icool_type == 'SubRegion':
            if isinstance(provided_type, SubRegion):
                return True
            else:
                return False

        if icool_type == 'Distribution':
            if isinstance(provided_type, Distribution):
                return True
            else:
                return False

        if icool_type == 'Correlation':
            if isinstance(provided_type, Correlation):
                return True
            else:
                return False

    def get_command_params(self):
        return self.command_params

    def is_required(self, command_param, command_parameters_dict):
        # command_parameters_dict = self.get_command_params()
        if 'req' not in command_parameters_dict[command_param]:
            return True
        else:
            return command_parameters_dict[command_param]['req']

    def gen_parm(self):
        command_params = self.get_command_params()
        parm = [None] * len(command_params)
        for key in command_params:
            pos = int(command_params[key]['pos']) - 1
            val = getattr(self, key)
            parm[pos] = val
        print parm
        return parm

    def for001_str_gen(self, value):
        if value.__class__.__name__ == 'bool':
            if value is True:
                return '.true.'
            else:
                return '.false.'
        else:
            return str(value)

    def get_begtag(self):
        return self.begtag

    def get_endtag(self):
        return self.endtag

    def get_line_splits(self):
        return self.for001_format['line_splits']