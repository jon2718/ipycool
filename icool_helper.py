
def valid_command(command_dict, command, value, namelist):
 """Checks whether command is valid in the following respects:
        (1) It is a valid variable for a namelist;
        (2) The type assigned to the variable is the correct type.
"""
    try:
        if command in command_dict.keys():
            dictionary_entry = command_dict[command]
            command_type = dictionary_entry['type']
            try:
                if check_type(command_type, value.__class__.__name__):
                    return 0
                else:
                    raise ie.IncorrectType('Incorrect type', command_type, value.__class__.__name__)
            except ie.IncorrectType as e:
                 print e
                 return -1   
        else:
            raise ie.UnknownVariable('Unknown variable', command, namelist)
    except ie.UnknownVariable as e:
        print e
        return -1
        
def check_input_args(title, cont, bmt, ints, nhs, nsc, nzh, nrh, nem, ncv, sec, name, metadata):
    try:
        if cont!=None and cont.__class__.__name__!='Cont':
            raise ie.NamelistObjectTypeError('Namelist object type error', cont, 'Cont')
        if sec!=None and sec.__class__.__name__!='Section':
             raise ie.NamelistObjectTypeError('Namelist object type error', sec, 'Section')   
    except ie.NamelistoObjectTypeError as e:
        print e
        return -1
        
def check_type(icool_type, provided_type):
    if icool_type=='Real':      
        if provided_type=='int' or provided_type=='long' or provided_type=='float':
            return True
        else:
            return False
    
    if icool_type=='Integer':
        if provided_type=='int' or provided_type=='long':
            return True
        else:
            return False
    
    if icool_type=='Logical':
        if provided_type=='bool':
            return True
        else:
            return False
 
 # Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError
 # If model is not specified, raises ModelNotSpecifiedError
def check_keyword_args(input_dict, cls):
    models=cls.models
    try:
       # print sorted(input_dict.keys())
       # print sorted(actual_dict.keys())
       if not check_model_specified(input_dict):
       		actual_dict={'Unknown':0}
       		raise ie.InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
       model=input_dict['model']
       actual_dict=cls.models[str(model)][1]
       if sorted(input_dict.keys())!=sorted(actual_dict.keys()):
           raise ie.InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
    except ie.InputArgumentsError as e:
        print e
        return -1

# Checks whether the keywords specified for a current model correspond to that model.
def check_partial_keywords_for_current_model(input_dict, cls):
	actual_dict=(cls, cls.model)
	for key in input_dict:
		if not key in cls.actual:
			raise ie.InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
	return True

# Checks whether the keywords specified for a new model correspond to that model.
def check_partial_keywords_for_new_model(input_dict, cls):
	model=input_dict['model']
	actual_dict=get_model_dict(cls, model)
	for key in input_dict:
		if not key in cls.actual:
			raise ie.InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
	return True


def check_model_specified(input_dict):
	if 'model' in input_dict.keys():
		return True
	else:
		return False

def get_model_dict(cls, model):
	models=cls.models
	return models[str(model)][1]