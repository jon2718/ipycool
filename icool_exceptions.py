class Error(Exception):
    """Base class for ICOOL input exceptions."""
    pass


class InputError(Error):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """
    def __init__(self, expr, msg):
        self.expr = expr
        self.msg = msg

    def __str__(self):
        string = self.msg + ' ' + self.expr
        return repr(string)


class IncorrectType(InputError):
    """Exception raised for incorrect type in the input."""
    def __init__(self, expr, expected_type, actual_type):
        InputError.__init__(self, expr, 'Incorrect type.')
        self.expected_type = expected_type
        self.actual_type = actual_type

    def __str__(self):
        msg = "Incorrect type.  Expected " + self.expected_type + " but instead got " + self.actual_type
        return repr(msg)


class UnknownCommand(InputError):
    """Exception raised for unknown type in the input."""

    def __init__(self, expr, command, namelist):
        InputError.__init__(self, expr, 'Unknown command.')
        self.command = command
        self.namelist = namelist

    def __str__(self):
        msg = 'Unknown command: ' + self.command +' in namelist: '+ self.namelist
        return repr(msg)
          

class IncorrectNamelistObject(InputError):   
      """Exception raised for unknown type in the input."""
      def __init__(self, expr, namelist, type):
          InputError.__init__(self, expr, 'Incorrect Namelist object.')
          self.namelist=namelist
          self.type=type
          
      def __str__(self):
          msg='Incorrect Namelist object. Expected: '+self.type+' but received: ' +self.namelist.__class__.__name__
          return repr(msg)


class IncorrectObjectCommand(InputError):
    """Exception raised for attempt to add incorrect command to an object."""
    def __init__(self, expr, object, command):
        self.object=object
        self.command=command
        
    def __str__(self):
        msg='Command: '+self.command+' is not supported in object: '+self.object
        return repr(msg)
 

class InputArgumentsError(InputError):
    """Exception raised for incorrect type in the input."""
    def __init__(self, expr, input_dict, actual_dict):
        InputError.__init__(self, expr, 'Input arguments error.')
        self.input_dict=input_dict
        self.actual_dict=actual_dict
        
    def __str__(self):
        received=""
        for key in sorted(self.input_dict.keys()):
            received+=str(key)
            received+=' '
        expected=""
        for key in sorted(self.actual_dict.keys()):
            expected+=str(key)
            expected+=' '
            
        msg='Input arguments error.\nReceived: \n'+received+'\nExpected: \n'+expected
        return msg
        
class FieldError(InputError):
    pass