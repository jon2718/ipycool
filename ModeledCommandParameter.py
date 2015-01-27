from ICoolObject import *


class ModeledCommandParameter(ICoolObject):

    def __init__(self, kwargs):
        """
        Checks to see whether all required parameters are specified.  If not, raises exception and exits.
        """
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)
        else:
            if self.check_no_model():
                return
            else:
                setattr(
                    self,
                    self.get_model_descriptor_name(),
                    self.get_model_name_in_dict(kwargs))
                del kwargs[self.get_model_descriptor_name()]
                self.setall(kwargs)

    def __call__(self, kwargs):
        if self.check_command_params_call(kwargs) is False:
            sys.exit(0)
        else:
            if not self.get_model_descriptor_name() in kwargs.keys():
                ICoolObject.__call__(self, kwargs)
            else:
                setattr(
                    self,
                    self.get_model_descriptor_name(),
                    self.get_model_name_in_dict(kwargs))
                del kwargs[self.get_model_descriptor_name()]
                self.setall(kwargs)

    def __setattr__(self, name, value):
        # Check whether the attribute being set is the model
        if name == self.get_model_descriptor_name():
            if self.check_valid_model(value) is False:
                return
            new_model = False
            # Check whether this is a new model (i.e. model was previously
            # defined)
            if hasattr(self, self.get_model_descriptor_name()):
                new_model = True
                # Delete all attributes of the current model
                print 'Resetting model to ', value
                self.reset_model()
            object.__setattr__(self, self.get_model_descriptor_name(), value)
            # If new model, set all attributes of new model to 0.
            if new_model is True:
                self.set_and_init_params_for_model(value)
            return
        try:
            if self.check_command_param(name):
                if self.check_command_param_type(name, value):
                    object.__setattr__(self, name, value)
            else:
                raise ie.SetAttributeError('', self, name)
        except ie.InvalidType as e:
            print e
        except ie.SetAttributeError as e:
            print e

    def __str__(self):
        desc = 'ModeledCommandParameter\n'
        for key in self.get_model_dict(
            getattr(
                self,
                self.get_model_descriptor_name())):
            desc = desc + key + ': ' + str(getattr(self, key)) + '\n'
        return desc

    def set_keyword_args_model_specified(self, kwargs):
        setattr(
            self,
            self.get_model_descriptor_name(),
            kwargs[
                self.get_model_descriptor_name()])
        for key in kwargs:
            if not key == self.get_model_descriptor_name():
                setattr(self, key, kwargs[key])

    def set_keyword_args_model_not_specified(self, kwargs):
        for key in kwargs:
            object.__setattr__(self, key, kwargs[key])

    def reset_model(self):
        for key in self.get_model_parms_dict():
            if hasattr(self, key):
                delattr(self, key)

    def set_and_init_params_for_model(self, model):
        for key in self.get_model_dict(model):
            if key is not self.get_model_descriptor_name():
                setattr(self, key, 0)

    def check_command_params_init(self, command_params):
        """
        Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError.
        If model is not specified, raises ModelNotSpecifiedError.
        Initialization of a model (e.g., Accel, SOL, etc. requires all keywords specified)
        """
        if self.check_no_model():
            return True
        if not self.check_model_specified(command_params):
            return False
        else:
            if not self.check_valid_model(
                    self.get_model_name_in_dict(command_params)):
                return False
            else:
                command_params_dict = self.get_command_params_for_specified_input_model(
                    command_params)
                if not self.check_command_params_valid(command_params, command_params_dict) \
                    or not self.check_all_required_command_params_specified(command_params, command_params_dict) \
                        or not self.check_command_params_type(command_params, command_params_dict):
                            return False
                else:
                    return True

    def check_command_params_call(self, command_params):
        """
        Checks to see whether new model specified in call.
        If so, checks that the parameters specified correspond to that model and raises an exception if they dont.
        Does NOT require all parameters specified for new model.  Unspecified parameters are set to 0.
        If model is not specified, checks whether the parameters specified correspond to the current model and
        raises an exception otherwise.
        """
        if not self.get_model_descriptor_name() in command_params.keys():
            command_params_dict = self.get_model_parms_dict()
            if not self.check_command_params_valid(command_params, command_params_dict) \
                or not self.check_command_params_type(command_params, command_params_dict):
                    return False
            else:
                return True
        else:
            return self.check_command_params_init(command_params)

    def check_valid_model(self, model):
        """
        Checks whether model specified is valid.
        If model is not valid, raises an exception and returns False.  Otherwise returns True.
        """
        try:
            if not str(model) in self.get_model_names():
                raise ie.InvalidModel(str(model), self.get_model_names())
        except ie.InvalidModel as e:
            print e
            return False
        return True

    def check_partial_keywords_for_current_model(self, input_dict):
        """
        Checks whether the keywords specified for a current model correspond to that model.
        """
        actual_dict = self.get_model_dict(
            getattr(
                self,
                self.get_model_descriptor_name()))
        for key in input_dict:
            if key not in actual_dict:
                raise ie.InputArgumentsError(
                    'Input Arguments Error',
                    input_dict,
                    actual_dict)
        return True

    def check_partial_keywords_for_new_model(self, input_dict):
        """
        Checks whether the keywords specified for a new model correspond to that model.
        """
        model = input_dict[self.get_model_descriptor_name()]
        actual_dict = self.get_model_dict(model)
        for key in input_dict:
            if key not in actual_dict:
                raise ie.InputArgumentsError(
                    'Input Arguments Error',
                    input_dict,
                    actual_dict)
        return True

    def check_model_specified(self, input_dict):
        """
        Check whether the user specified a model in specifying parameters to Init or Call.
        if so, returns True.  Otherwise, raises an exception and returns False.
        """
        try:
            if not self.get_model_descriptor_name() in input_dict.keys():
                raise ie.ModelNotSpecified(self.get_model_names())
        except ie.ModelNotSpecified as e:
            print e
            return False
        return True

    def check_no_model(self):
        if self.get_model_descriptor_name() is None:
            return True
        else:
            return False
    # Helper functions
    ##################################################

    def get_model_descriptor(self):
        """Returns the model descriptor dictionary"""
        return self.models['model_descriptor']

    def get_model_descriptor_name(self):
        """
        The model descriptor name is an alias name for the term 'model', which is specified for each descendent class.
        Returns the model descriptor name.
        """
        return self.get_model_descriptor()['name']

    def get_current_model_name(self):
        """Returns the name of the current model"""
        return getattr(self, self.get_model_descriptor_name())

    def get_model_parms_dict(self):
        """
        Returns the parameter dictionary for the current model.
        """
        if self.get_model_descriptor_name() is None:
            return {}
        else:
            return self.get_model_dict(self.get_current_model_name())

    def get_model_dict(self, model):
        """
        Returns the parameter dictionary for model name.
        """
        return self.models[str(model)]['parms']

    def get_num_params(self):
        """
        Returns the number of parameters for model.
        """
        return self.get_model_descriptor()['num_parms']

    def get_icool_model_name(self):
        """Check to see whether there is an alternate icool_model_name from the common name.
        If so return that.  Otherwise, just return the common name."""
        if 'icool_model_name' not in self.models[
                str(self.get_current_model_name())]:
            return self.get_current_model_name()
        else:
            return self.models[str(self.get_current_model_name())][
                'icool_model_name']

    def get_model_names(self):
        """Returns a list of all model names"""
        ret_list = self.models.keys()
        pos = ret_list.index('model_descriptor')
        del ret_list[pos]
        return ret_list

    def get_model_name_in_dict(self, dict):
        """Returns the model name in a provided dictionary if it exists.  Otherwise returns None"""
        if self.get_model_descriptor_name() not in dict:
            return None
        else:
            return dict[self.get_model_descriptor_name()]

    def get_command_params(self):
        return self.get_model_parms_dict()

    def get_command_params_for_specified_input_model(
            self,
            input_command_params):
        specified_model = input_command_params[
            self.get_model_descriptor_name()]
        return self.get_model_dict(specified_model)

    def get_line_splits(self):
        return self.models['model_descriptor']['for001_format']['line_splits']

    ##################################################

    def set_model_parameters(self):
        parms_dict = self.get_model_parms_dict()
        high_pos = 0
        for key in parms_dict:
            if key['pos'] > high_pos:
                high_pos = key['pos']
        self.parms = [0] * high_pos

    def gen_parm(self):
        num_parms = self.get_num_params()
        command_params = self.get_command_params()
        parm = [0] * num_parms
        for key in command_params:
            pos = int(command_params[key]['pos']) - 1
            if key == self.get_model_descriptor_name():
                val = self.get_icool_model_name()
                print 'Using icool name', val
            else:
                val = getattr(self, key)
            parm[pos] = val
        print parm
        return parm

    def gen_for001(self, file):
        if hasattr(self, 'begtag'):
            print 'Writing begtag'
            # file.write('\n')
            file.write(self.get_begtag())
            file.write('\n')
        parm = self.gen_parm()
        splits = self.get_line_splits()
        count = 0
        split_num = 0
        cur_split = splits[split_num]
        for i in parm:
            if count == cur_split:
                file.write('\n')
                count = 0
                split_num = split_num + 1
                cur_split = splits[split_num]
            file.write(str(i))
            file.write(' ')
            count = count + 1
        file.write('\n')
        if hasattr(self, 'endtag'):
            print 'Writing endtag'
            file.write('\n')
            file.write(self.get_endtag())
            file.write('\n')