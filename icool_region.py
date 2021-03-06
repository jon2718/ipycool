# -*- coding: utf-8 -*-
import sys
import icool_exceptions as ie

"""Nomenclature:

An ICOOl input file consists of:
1. Problem title
2. General control variables
3. Beam generation variables
4. Physics interactions control variables
5. Histogram definition variables
6. Scatterplot definition variables
7. Z-history definition variables
8. R-history definition variables
9. Emittance plane definition variables
10. Covariance plane definition variables
11. Region definition variables.
** Note that region definition variables are referred to in the ICOOL Manual and
herein as commands.

This program will use of following object definitions:
Namelists.  Namelists in the for001.dat file are preceded by an '&' 
sign (e.g., &cont).

Namelists include:
CONT: Control Variables
BMT: Beam Generation Variables
INTS: Phyiscs Interactions Control Variables
NHS: Histogram Definition Variables
NSC: Scatterplot definition Variables
NZH: Z-History Definition Variables
NRH: R-History Definition Variables
NEM: Emittance Plane Definition Variables
NCV: Covariance Plane Definition Variables


Namelist variables:
Each of the above namelists is associated with a respective set of variables.

Commands:
Commands comprise both Regular Region Commands and Pseudoregion Commands

Regular Region Commands:
SECTION
BEGS
REPEAT
CELL
SREGION
ENDREPEAT
ENDCELL
ENDSECTION

Psuedoregion Commands:
APERTURE
CUTV
DENP
DENS
DISP
DUMMY
DVAR
EDGE
GRID
OUTPUT
RESET
RKICK
ROTATE
TAPER
TILT
TRANSPORT
BACKGROUND
BFIELD
ENDB
!
&

Command parameters:
Each regular and pseduoregion command is respectively associated with a set of command parameters.
"""
from IPython.core.magic_arguments import (argument, magic_arguments,
    parse_argstring)
from IPython.core.magic import (register_line_magic, register_cell_magic,
                                register_line_cell_magic)

#@register_line_magic
@magic_arguments()
@argument('-o', '--option', help='An optional argument.')
@argument('arg', type=int, help='An integer positional argument.')
def ipycool(self, arg):
    """ A really cool ipycool magic command.

    """
    args = parse_argstring(ipycool, arg)


class ICoolGen(object):
    """Generate ICOOL for001.dat
    Takes an ICoolInput object and generates an ICOOL for001.dat file.
    """

    def __init__(self, icool_input, path='.'):
        self.file = path + '/' + 'for001.dat'
        self.icool_input = icool_input

    def gen(self):
        f = open(self.file, 'w')
        self.icool_input.gen(f)
        f.close()

    def cr(f):
        f.write('\n')

    def sp(f):
        f.write(" ")

    def list_line(self, f, list):
        for item in list:
            f.write(item)
            self.sp()


class ICoolInput(object):
    """This is the actual generated ICoolInput from command objects
    Command objects include:
    Title, Cont, Bmt, Ints, Nhs, Nsc, Nzh, Nrh, Nem, Ncv and region command objects.
    Region command objects are the superclass of all region command objects and are
    subclassed into RegularRegion and PsuedoRegion command objects.

    RegularRegion command objects include: Section, Repeat, Cell and SRegion.
    Section, Begs, Repeat and Cell will typically contain other allowed region command objects
    such as SRegions as permitted by ICool.

    PseudoRegion command objects include:
        Aperture, Cutv, Denp, Dens, Disp, Dummy, Dvar, Edge, Grid, Output, Refp, Ref2, Reset, Rkick,
        Rotate, Taper, Tilt, Transport, Background, Bfield, ! and &

    title is a problem title object.
    cont is a control variables object.
    bmt is a beam generation variables object.
    ints is a physics interactions control variables object.
    nhs is a histogram defintion variables object.
    nsc is a scatterplot definition variables object.
    nzh is a z-history defintion variables object.
    nrh is a r-history defintion variables object.
    nem is an emittance plane definition variables object.
    ncv is a covariance plane definition variables object.
    sec is a region definition variables object, which contains all region definitions.
    """

    def __init__(
        self, title=None, cont=None, bmt=None, ints=None,
        nhs=None, nsc=None, nzh=None, nrh=None, nem=None, ncv=None,
        section=None, name=None, metadata=None
    ):

        if ie.check_input_args(
            title, cont, bmt, ints, nhs, nsc, nzh, nrh, nem,
            ncv, section, name, metadata
        ) == -1:
            sys.exit(0)
        self.title = title
        self.cont = cont
        self.bmt = bmt
        self.ints = ints
        self.nhs = nhs
        self.nsc = nsc
        self.nzh = nzh
        self.nrh = nrh
        self.nem = nem
        self.ncv = ncv
        self.section = section
        self.name = name
        self.metadata = metadata
# What is the minimum required set of commands?

    def __str__(self):
        return self.title.__str__()+self.section.__str__()

    def add_title(self, title):
        self.title = title

    def add_cont(self, cont):
        self.cont = cont

    def add_sec(self, sec):
        self.sec = sec

    def gen(self, file):
        if self.title is not None:
            self.title.gen(file)
        if self.cont is not None:
            self.cont.gen(file)
        if self.bmt is not None:
            self.bmt.gen(file)
        if self.ints is not None:
            self.ints.gen(file)
        if self.nhs is not None:
            self.nhs.gen(file)
        if self.nsc is not None:
            self.nsc.gen(file)
        if self.nzh is not None:
            self.nzh.gen(file)
        if self.nrh is not None:
            self.nrh.gen(file)
        if self.nem is not None:
            self.nem.gen(file)
        if self.ncv is not None:
            self.ncv.gen(file)
        if self.sec is not None:
            self.sec.gen(file)


class Title(object):

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return 'Problem Title: ' + self.title + '\n'

    def __repr__(self):
        return 'Problem Title: ' + self.title + '\n'

    def gen(self, file):
        file.write(self.title)


class ICoolType(object):
    def check_variables_type(self, variables):
        """Checks to see whether all variables specified were of the correct type"""
        variables_dict = self.variables
        try:
            for key in variables:
                if self.check_type(variables_dict[key]['type'], variables[key]) is False:
                    raise ie.InvalidType(variables_dict[key]['type'], variables[key].__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_variable_type(self, name, value):
        """Checks to see whether a particular variable of name with value is of the correct type"""
        variables_dict = self.variables
        try:
            if self.check_type(variables_dict[name]['type'], value) is False:
                raise ie.InvalidType(variables_dict[name]['type'], value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

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

        if icool_type == 'Distribution':
            if isinstance(provided_type, Distribution):
                return True
            else:
                return False


class ICoolVariablesSet(object):
    """Variables Sets comprise:
    CONT
    BMT
    INTS
    NHS
    NSC
    NZH
    NRH
    NEM
    NCV
    """
    def __init__(self, kwargs):
        if self.check_variables_init(kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __call__(self, **kwargs):
        if self.check_variables_call(self, kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __str__(self):
        return '[ICoolVariablesSet.]'

    def __repr__(self):
        return '[ICoolVariablesSet.]'

    def __setattr__(self, name, value):
        if self.check_variable(name) and self.check_variable_type(name, value):
            object.__setattr__(self, name, value)
        else:
            sys.exit(0)

    def check_variable(self, variable):
        """
        Checks whether a parameter specified for command is valid.
        """
        variables_dict = self.variables
        #Check command parameters are all valid
        try:
            if not variable in variables_dict:
                raise ie.UnknownVariable(variable, variables_dict.keys())
        except ie.UnknownVariable as e:
            print e
            return False
        return True

    def check_variables_valid(self, variables):
        """Returns True if command_params are valid (correspond to the command)
        Otherwise raises an exception and returns False"""
        variables_dict = self.variables
        try:
            for key in variables:
                if not key in variables_dict:
                    raise ie.UnknownVariable(key, variables_dict)
        except ie.UnknownVariable as e:
            print e
            return False
        return True

    def check_variables_type(self, variables):
        """Checks to see whether all variables specified were of the correct type"""
        variables_dict = self.variables
        try:
            for key in variables:
                if self.check_type(variables_dict[key]['type'], variables[key]) is False:
                    raise ie.InvalidType(variables_dict[key]['type'], variables[key].__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_variable_type(self, name, value):
        """Checks to see whether a particular variable of name with value is of the correct type"""
        variables_dict = self.variables
        try:
            if self.check_type(variables_dict[name]['type'], value) is False:
                raise ie.InvalidType(variables_dict[name]['type'], value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_all_required_variables_specified(self, variables):
        """Returns True if all required variables were specified
        Otherwise raises an exception and returns False"""
        variables_dict = self.variables
        try:
            for key in variables_dict:
                if variables_dict[key]['req'] is True:
                    if not key in variables:
                        raise ie.MissingCommandParameter(key, variables)
        except ie.MissingCommandParameter as e:
            print e
            return False
        return True
    
    def check_variables_init(self, variables):
        """
        Checks whether the variables specified for a VariablesSet are valid,
        and all variables are of correct type.  If not, raises an exception.
        If all variables are valid, sets the variables.
        """
        if not self.check_variables_valid(variables)\
                or not self.check_variables_type(variables)\
                or not self.check_all_required_variables_specified(variables):
            return False

        #Now set the command parameters
        for key in variables:
            self.__setattr__(key, variables[key])
        return True

    def check_variables_call(self, variables):
        """
        Checks whether the parameters specified for command are valid and all required parameters exist.
        """
        variables_dict = self.variables
        #Check command parameters are all valid
        try:
            for key in variables:
                if not key in variables_dict:
                    raise ie.UnknownVariable(key, variables_dict.keys())
        except ie.UnknownVariable as e:
            print e
            return False
        return True

    def setall(self, variables):
        for key in variables:
            self.__setattr__(key, variables[key])

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

        if icool_type == 'Distribution':
            if isinstance(provided_type, Distribution):
                return True
            else:
                return False


class Cont(ICoolVariablesSet):
    variables = {
        'betaperp':  {'default': None,
                      'desc': '(R) beta value to use in calculating amplitude variable A^2',
                      'type': 'Real',
                      'req': False},

        'bgen':     {'default': True,
                     'desc': '(L) if .true.=>generate initial beam particles, otherwise read input from FOR003.DAT '
                     '(true)',
                     'type': 'Logical',
                     'req': False},

        'bunchcut': {'default': 1E6,
                     'desc': '(R) maximum time difference allowed between a particle and the reference particle [s] '
                     '(1E6)',
                     'type': 'Real'},

        'bzfldprd': {'default': None,
                     'desc': '(R) Bz for solenoid at location of production plane (0.) This is used for output to '
                     'file for009.dat and for canonical angular momentum correction.',
                     'type': 'Real'},

        'dectrk':   {'default': False,
                     'desc': '(L) if .true. => continue tracking daughter particle following decay.',
                     'type': 'Logical'},

        'diagref':  {'default': False,
                     'desc': '(L) if .true. => continue tracking daughter particle following decay.',
                     'type': 'Logical'},

        'epsf':     {'default': 0.05,
                     'desc': '(R) desired tolerance on fractional field variation, energy loss, and multiple '
                     'scattering per step',
                     'type': 'Real'},

        'bzfldprd': {'default': None,
                     'desc': '(R) Bz for solenoid at location of production plane (0.) This is used for output to '
                     'file for009.dat and for canonical angular '
                     'momentum correction.',
                     'type': 'Real'},

        'dectrk':   {'default': False,
                     'desc': '(L) if .true. => continue tracking daughter particle following decay',
                     'type': 'Logical'},

        'diagref':  {'default': False,
                     'desc': '(L) if .true. => continue tracking daughter particle following decay',
                     'type': 'Logical'},

        'epsf':     {'default': 0.05,
                     'desc': '(R) desired tolerance on fractional field variation, energy loss, and multiple '
                     'scattering per step',
                     'type': 'Real'},

        'epsreq':   {'default': None,
                     'desc': '(R) required tolerance on error in tracking parameters (1E-3) This parameter is '
                     'only used if varstep = true',
                     'type': 'Real'},

        'epsstep':  {'default': 1E-6,
                     'desc': '(R) desired tolerance in spatial stepping to reach each destination plane [m]',
                     'type': 'Real'},

        'ffcr':     {'default': False,
                     'desc': '(L) if .true. => inserts form feed and carriage returns in the output log file so there '
                     'are two plots per page starting at the top of a page',
                     'type': 'Logical'},

        'forcerp':  {'default': True,
                     'desc': '(L) if .true. => set x, y, Px, and Py for reference particle to 0 for each new REFP '
                     'command and for each ACCEL region with phasemodel=4.',
                     'type': 'Logical'},

        'fsav':     {'default': None,
                     'desc': '(L) if .true. => store particle info at plane IZFILE into file FOR004.DAT. (false). '
                     'It is possible to get the initial distribution of particles that get a given error flag be '
                     'setting the plane=IFAIL . It is possible to get the initial distribution of particles that '
                     'successfully make it to the end of the simulation by setting the plane= -1.',
                     'type': 'Logical'},

        'fsavset':  {'default': False,
                     'type': '(L) if .true. => modify data stored using FSAV in FOR004.DAT to have z=0 and '
                     'times relative to reference particle at plane IZFILE.',
                     'type': 'Logical'},

        'f9dp':     {'default': None,
                     'desc': '(I) number of digits after the decimal point for floating point variables in FOR009.DAT '
                     '{4,6,8,10,12,14,16,17} (4) F9DP=17 gives 16 digits after the decimal point and 3 digits in the '
                     'exponent',
                     'type': 'Integer'},

        'goodtrack': {'default': True,
                      'desc': '(L) if .true. and BGEN=.false. => only accepts input data from file FOR003.DAT if '
                      'IPFLG=0.; if .false. => resets IPFLG of bad input tracks to 0 (this allows processing a '
                      'file of bad tracks for diagnostic purposes)',
                      'type': 'Logical'},

        'izfile':    {'default': None,
                      'desc': '(I) z-plane where particle info is desired when using FSAV. Use 1 to store beam at '
                      'production. Saves initial particle properties for bad tracks if IZFILE=IFAIL #.  Saves initial '
                      'particle properties for tracks that get to the end of the simulation if IZFILE=-1.  IZFILE '
                      'should point to the end of a REGION or to an APERTURE , ROTATE or TRANSPORT pseudoregion '
                      'command.',
                      'type': 'Integer'},

        'magconf':    {'default': 0,
                       'desc': '(I) if 19 < MAGCONF=mn < 100 => reads in file FOR0mn.DAT, which contains data on '
                       'solenoidal magnets. Used with SHEET, model 4.',
                       'type': 'Integer'},

        'mapdef':     {'default': 0,
                       'desc': '(I) if 19 < MAPDEF=mn < 100 => reads in file FOR0mn.DAT, which contains data on how '
                       'to set up field grid. Used with SHEET, model 4.',
                       'type': 'Integer'},

        'neighbor':   {'default': False,
                       'desc': "(L) if .true. => include fields from previous and following regions when calculating "
                       "field.  This parameter can be used with soft-edge fields when the magnitude of the "
                       "field doesn't fall to 0 at the region boundary. A maximum of 100 region can be used "
                       "with this feature.",
                       'type': 'Logical'},

        'neutrino':    {'default': 0,
                        'desc': '(I) if 19 < NEUTRINO=mn < 100 => writes out file FOR0mn.DAT, which contains '
                        'neutrino production data. See section 5.2 for the format.',
                        'type': 'Integer'},

        'nnudk':       {'default': 1,
                        'desc': '(I) # of neutrinos to produce at each muon, pion and kaon decay.',
                        'type': 'Integer'},

        'npart':       {'default': None,
                        'desc': '(I) # of particles in simulation. The first 300,000 particles are stored in memory. '
                        'Larger numbers are allowed in principle since ICOOL writes the excess particle '
                        'information to disc. However, there can be a large space and speed penalty in doing '
                        'so.',
                        'type': 'Integer'},

        'nprnt':        {'default': -1,
                         'desc': ' Number of diagnostic events to print out to log file.',
                         'type': 'Integer'},

        'npskip':       {'default': 0,
                         'desc': 'Number of input particles in external beam file to skip before processing starts',
                         'type': 'Integer'},

        'nsections':    {'default': 1,
                         'desc': '(I) # of times to repeat basic cooling section (1).  This parameter can be used to '
                         'repeat all the commands between the SECTION and ENDSECTION commands in the problem '
                         'definition. If a REFP command immediately follows the SECTION command, it is not '
                         'repeated',
                         'type': 'Integer'},

        'ntuple':        {'default': False,
                          'desc': '(L) if .true. => store information about each particle after every region in file '
                          'FOR009.DAT. This variable is forced to be false if RTUPLE= true.(false)}',
                          'type': 'Logical'},

        'nuthmin':      {'default': 0,
                         'desc': '(R) Minimum polar angle to write neutrino production data to file. [radians]',
                         'type': 'Real'},

        'nuthmax':      {'default': 3.14,
                         'desc': 'Maximum polar angle to write neutrino production data to file. [radians]',
                         'type': 'Real'},

        'output1':      {'default': False,
                         'desc': 'if .true. => write particle information at production (plane 1) to the '
                         'postprocessor output file for009.dat.',
                         'type': 'Logical'},
      
        'phantom':     {'default': False,
                        'desc': 'if .true. => force particle to keep initial transverse coordinates after every '
                                '(L) if .true. => force particle to keep initial transverse coordinates after '
                                'every step. This is useful for making magnetic field maps. (false)',
                        'type': 'Logical'},
                                   
        'phasemodel':   {'default': 1,
                         'desc': 'PHASEMODEL (I) controls how the phase is determined in rf cavities. (1) '
                                 '1: takes phase directly from ACCEL command [degrees] '
                                 '2 - 6: takes phase model from REFP command '
                                 '7: reads phases in from file FOR0mn.DAT, where RFPHASE=mn. See sec. 5.1.},',
                         'type': 'Integer'},

        'prlevel': {},
                
        'prnmax': {},
                
        'pzmintrk': {},
                
        'rfdiag': {},
                
        'rfphase': {},
        
        'rnseed': {},
        
        'rtuple': {},
        
        'rtuplen': {},
        
        'run_env': {},
        
        'scalestep': {},
        
        'spin': {},

        'spinmatter': {},
                
        'spintrk': {},
                
        'stepmax': {},
                
        'stepmin': {},
                
        'steprk': {}, 
        
        'summary': {},
                
        'termout':{},
                
        'timelim': {},
                
        'varstep': {}
    }

    def __init__(self, **kwargs):
        if self.check_variables_init(kwargs) is False:
            sys.exit(0)


    def __str__(self):
        defined_cont = display_commands(cont_commands)
        return 'Control variables: \n'

    def __repr__(self):
        return '[Control variables: ]'

    def gen(self, file):
        file.write("\n")
        file.write("&cont")
        file.write("\n")
        for key, value in self.cont_commands.items():
            file.write(key)
            file.write('=')
            file.write(str(value))
            file.write("\n")
        file.write("/")



class Bmt(ICoolVariablesSet):
    variables = {
        'nbeamtyp':  {'desc': '# of beam types, e.g., particles of different masses.',
                      'type': 'Integer',
                      'default': 1,
                      'req': True},

        'bmalt':   {'desc': 'if true => flip sign of alternate particles when BGEN = true.',
                    'type': 'Logical',
                    'default': False,
                    'req': False},

        'beamtype_list':   {'desc': 'List of distribution objects',
                    'type': 'List[Distribution]',
                    'default':  None,
                    'req': False},

        'correlation_list': {'desc': 'List of Correlation objects',
                           'type': 'List[Correlation]',
                           'default': None,
                           'req': False},
        }

    def __init__(self, **kwargs):
        if self.check_variables_init(kwargs) is False:
            sys.exit(0)

    def add_beamtype(self, beamtype):
        self.beamtype_list.append(beamtype)

    def add_beamtypes(self, beamtype_list):
        for beamtype in beamtype_list:
            self.beamtype_list.append(beamtype)

    def add_correlation(self, correlation):
        self.correlation_list.append(correlation)

    def add_correlations(self, correlation_list):
        for correlation in correlation_list:
            self.correlation_list.append(correlation)


class Ints(ICoolVariablesSet):
    def __init__(self, **kwargs):
        pass


class Region(object):
    def __init__(self, kwargs):
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __call__(self, **kwargs):
        if self.check_command_params_call(self, kwargs) is False:
            sys.exit(0)
        else:
            self.setall(kwargs)

    def __str__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __repr__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    """Checks whether all required command parameters specified in __init__ are provided are valid
    for Region command.
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
        command_parameters_dict = self.command_params
        #Check command parameters are all valid
        try:
            if not command_param in command_parameters_dict:
                raise ie.InvalidCommandParameter(command_param, command_parameters_dict.keys())
        except ie.InvalidCommandParameter as e:
            print e
            return False
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_valid(self, command_params):
        """Returns True if command_params are valid (correspond to the command)
        Otherwise raises an exception and returns False"""
        command_parameters_dict = self.command_params
        try:
            for key in command_params:
                if not key in command_parameters_dict:
                    raise ie.InvalidCommandParameter(key, command_parameters_dict)
        except ie.InvalidCommandParameter as e:
            print e
            return False
        return True

    def check_all_required_command_params_specified(self, command_params):
        """Returns True if all required command parameters were specified
        Otherwise raises an exception and returns False"""
        command_parameters_dict = self.command_params
        try:
            for key in command_parameters_dict:
                if command_parameters_dict[key]['req'] is True:
                    if not key in command_params:
                        raise ie.MissingCommandParameter(key, command_params)
        except ie.MissingCommandParameter as e:
            print e
            return False
        return True

    def check_command_params_type(self, command_params):
        """Checks to see whether all required command parameters specified were of the correct type"""
        command_params_dict = self.command_params
        try:
            for key in command_params:
                if self.check_type(command_params_dict[key]['type'], command_params[key]) is False:
                    raise ie.InvalidType(command_params_dict[key]['type'], command_params[key].__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_param_type(self, name, value):
        """Checks to see whether a particular command parameter of name with value is of the correct type"""
        command_params_dict = self.command_params
        try:
            if self.check_type(command_params_dict[name]['type'], value) is False:
                raise ie.InvalidType(command_params_dict[name]['type'], value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def check_command_params_init(self, command_params):
        """
        Checks whether the parameters specified for command are valid, all required parameters are
        specified and all parameters are of correct type.  If not, raises an exception.
        """
        check_params = not self.check_command_params_valid(command_params)\
            or not self.check_all_required_command_params_specified(command_params)\
                or not self.check_command_params_type(command_params)

        if check_params:
            return False
        
        #if not self.check_command_params_valid(command_params)
        #    or not self.check_all_required_command_params_specified(command_params)\
         #       or not self.check_command_params_type(command_params):
         #           return False

        #Now set the command parameters
        for key in command_params:
            self.__setattr__(key, command_params[key])
        return True

    def check_command_params_call(self, cls, command_params):
        """
        Checks whether the parameters specified for command are valid and all required parameters exist.
        """
        command_parameters_dict = cls.command_params
        #Check command parameters are all valid
        try:
            for key in command_params:
                if not key in command_parameters_dict:
                    raise ie.InvalidCommandParameter(key, command_parameters_dict.keys())
        except ie.InvalidCommandParameter as e:
            print e
            return False
        return True

    def setall(self, command_params):
        for key in command_params:
            self.__setattr__(key, command_params[key])

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


class RegularRegion(Region):
    """
    RegularRegion commands include: SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,
    and ENDCELL.
    """
    def __init__(self, kwargs):
        Region.__init__(self, kwargs)

    def __str__(self):
        return '[A RegularRegion can be either a SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,\
or ENDCELL.]'

    def __repr__(self):
        return '[A RegularRegion can be either a SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,\
                or ENDCELL.]'


class PseudoRegion(Region):
    """
    PseudoRegion commands include: APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID
    OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &
    """
    def __init__(self, name=None, metadata=None):
        Region.__init__(self, name, metadata)

    def __str__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'

    def __repr__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'


class Container(object):
    """Abstract class container for other commands.
    """
    def __init__(self, enclosed_commands=None):
        if enclosed_commands is None:
            self.enclosed_commands = []
        else:
            if self.check_allowed_enclosed_commands(enclosed_commands):
                self.enclosed_commands = enclosed_commands

    def __setattr__(self, name, value):
        #command_parameters_dict = self.command_params
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
                raise ie.ContainerCommandError(command, self.allowed_enclosed_commands)
        except ie.ContainerCommandError as e:
            print e
            return False
        return True

    def check_allowed_enclosed_commands(self, enclosed_commands):
        pass


class Section(RegularRegion, Container):
    """
    SECTION Start of cooling section region definition.
    The data must end with an ENDSECTION.   It can enclose any number of other commands.
    If it is desired to repeat the section definitions, the control variable NSECTIONS should be
    set >1 and a BEGS command is used to define where to start repeating.
    """

    allowed_enclosed_commands = [
        'Begs', 'Repeat', 'Cell', 'Background', 'SRegion', 'Aperture', 'Cutv', 'Dens', 'Disp', 'Dummy', 'DVar',
        'Edge', 'Output', 'Refp', 'Ref2', 'Reset', 'RKick', 'Rotate', 'Tilt', 'Transport', 'Comment'
        'Repeat'
        ]

    command_params = {}

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return 'Section\n'

    def __repr__(self):
        return 'Section\n'

    #def gen(self, file):
    #    region.gen('SECTION')

    def gen(self, file):
        file.write('\n')
        file.write('SECTION')
        for command in self.commands:
            command.gen(file)
        file.write('\n')
        file.write('ENDSECTION')


class Begs(RegularRegion):
    def __init__(self):
        RegularRegion.__init(self, None, None)

    def gen(self, file):
        pass


class Repeat(RegularRegion, Container):
    """
    Start of a repeating group of region commands; the data must end with an ENDREPEAT
    command. This can be used to repeat regions inside a cell. The repeat loop can enclose any
    number of {SREGION, APERTURE, DENS, DISP, DUMMY, DVAR, EDGE, OUTPUT, REFP, REF2, RESET, RKICK,
    ROTATE, TILT, TRANSPORT} commands. Repeat sections cannot be nested in other repeat sections.
    (see parameters below)
    """
    command_params = {
        'nrep':  {'desc': '# of times to repeat following region commands',
                  'type': 'Integer',
                  'req': True}
        }

    allowed_enclosed_commands = [
        'SRegion', 'Aperture', 'Dens', 'Disp', 'Dummy', 'Dvar', 'Edge', 'Output', 'Refp',
        'Ref2', 'Reset', 'Rkick', 'Rotate', 'Tilt', 'Transport'
    ]

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return 'Repeat\n'

    def __repr__(self):
        return 'Repeat\n'

    def gen(self, file):
        pass


class Background(PseudoRegion):
    def __init__(self, name=None, metadata=None):
        PseudoRegion.__init__(self, name, metadata)


class Bfield(PseudoRegion):
    def __init__(self, name=None, metadata=None):
        PseudoRegion.__init__(self, name, metadata)


class Edge(PseudoRegion):
    """EDGE Fringe field and other kicks for hard-edged field models
    1) edge type (A4) {SOL, DIP, HDIP, DIP3, QUAD, SQUA, SEX, BSOL, FACE}

    2.1) model # (I) {1}
    2.2-5) p1, p2, p3,p4 (R) model-dependent parameters

    Edge type = SOL
    p1: BS [T]
    If the main solenoid field is B, use p1=-B for the entrance edge and p1=+B for the exit edge.

    Edge type = DIP
    p1: BY [T]

    Edge type = HDIP
    p1: BX [T]

    Edge type = DIP3
    p1: rotation angle [deg]
    p2: BY0 [T]
    p3: flag 1:in 2:out

    Edge type = QUAD
    p1: gradient [T/m]

    Edge type = SQUA
    p1: gradient [T/m]

    Edge type = SEX
    p1: b2 [T/m2] (cf. C. Wang & L. Teng, MC 207)

    Edge type = BSOL
    p1: BS [T]
    p2: BY [T]
    p3: 0 for entrance face, 1 for exit face

    Edge type = FACE
    This gives vertical focusing from rotated pole faces.
    p1: pole face angle [deg]
    p2: radius of curvature of reference particle [m]
    p3: if not 0 => correct kick by factor 1/(1+delta)
    p4: if not 0 ==> apply horizontal focus with strength = (-vertical strength)
    If a FACE command is used before and after a sector dipole (DIP), you can approximate a rectangular dipole field.
    The DIP, HDIP, QUAD, SQUA, SEX and BSOL edge types use Scott Berg's HRDEND routine to find the change in transverse
    position and transverse momentum due to the fringe field.
    """

    def __init__(self, edge_type, model, model_parameters_list, name=None, metadata=None):
        PseudoRegion.__init__(self, name, metadata)
        self.edge_type = edge_type
        self.model = model
        self.model_parameters = model_parameters


class Cell(RegularRegion, Container):
    """CELL Start of a repeating group of region commands; the data must end with an ENDCELL command.
    The cell loop can enclose any number of commands under REPEAT plus REPEAT and ENDREPEAT commands.
    It has an associated cell field, which is superimposed on the individual region fields. Cell sections cannot
    be nested in other cell sections. (see parameters below)
    """
    allowed_enclosed_commands = [
        'SRegion', 'Aperture', 'Dens', 'Disp', 'Dummy', 'DVar', 'Edge', 'Output',
        'Refp', 'Ref2', 'Reset', 'RKick', 'Rotate', 'Tilt', 'Transport', 'Repeat'
        ]

    command_params = {
        'ncells':  {'desc': 'Number of times to repeat this command in this cell block',
                    'type': 'Integer',
                    'req': True},

        'flip':      {'desc': 'if .true. => flip cell field for alternate cells',
                      'type': 'Logical',
                      'req': False},


        'field':      {'desc': 'Field object',
                       'type': 'Field',
                       'req': True},

        }

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)
        Container.__init__(self)

    def __setattr__(self, name, value):
        Container.__setattr__(self, name, value)

    def __str__(self):
        return 'Cell\n'

    def __repr__(self):
        return 'Cell\n'

    def gen(self, file):
        region.gen('CELL')


class SRegion(RegularRegion):
    """
    SREGION - Start of new s-region. Describes field and material properties.

    Parameters:
    1.1) SLEN (R) Length of this s region [m]
    1.2) NRREG (I) # of radial subregions of this s region {1-4}
    1.3) ZSTEP (R) step for tracking particles [m]
    Note that for fixed-stepping the program may modify this value slightly to get
    an integral number of steps in the region.

    The following parameters are repeated for each r subregion:
    2.1) IRREG (I) r-region number
    2.2) RLOW (R) Inner radius of this r subregion[m]
    2.3) RHIGH (R) Outer radius of this r subregion[m]

    3) FTAG (A4) Tag identifying field in this r subregion
    (See specific field type below)

    4) FPARM (R) 15 parameters describing field (see specific field type below)
    These 15 parameters must be on one input line.

    5) MTAG (2A4) Tag identifying material composition in this r subregion
    The wedge geometry can accept a second MTAG parameter.
    The first material refers to the interior of the wedge.
    The second material, if present, refers to the exterior of the wedge.
    If a second MTAG parameter is not present, vacuum is assumed. (see specific material type below)

    6) MGEOM (A6) Tag identifying material geometry in this r subregion.
    (see specific material type below)

    7) GPARM (R) 10 Parameters describing material geometry.
    These 10 parameters must be on one input line (see specific material type below)
    """

    allowed_enclosed_commands = None

    command_params = {
        'slen':  {'desc': 'Length of this s region [m]',
                  'doc': '',
                  'type': 'Real',
                  'req': True},

        'nrreg':   {'desc': '# of radial subregions of this s region {1-4}',
                    'doc': '',
                    'type': 'Int',
                    'min': 1,
                    'max': 4,
                    'req': True},

        'zstep':   {'desc': 'Step for tracking particles [m]',
                    'doc': '',
                    'type': 'Real',
                    'req': True},

        'subregion_list': {'desc': 'List of SubRegion objects',
                           'doc': '',
                           'type': 'List[SubRegion]',
                           'req': False},
        }

    def __init__(self, **kwargs):
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)

    def __str__(self):
        ret_str = 'SRegion:\n'+'slen='+str(self.slen) + '\n' + 'nrreg=' + str(self.nrreg) + '\n' + \
               'zstep=' + str(self.zstep)
        for element in self.subregions:
            ret_str += element
        return ret_str

    def __repr__(self):
        return 'SRegion:\n '+'slen='+str(self.slen)+'\n'+'nrreg='+str(self.nrreg)+'\n'+'zstep='+str(self.zstep)

    def __setattr__(self, name, value):
        Region.__setattr__(self, name, value)

    def add_subregion(self, subregion):
        try:
            if self.check_type('SubRegion', subregion):
                if not hasattr(self, 'subregion_list'):
                    self.subregion_list = []
                self.subregion_list.append(subregion)
            else:
                raise ie.InvalidType('SubRegion', subregion.__class__.__name__)
        except ie.InvalidType as e:
            print e
               

    def add_subregions(self, subregion_list):
        for subregion in subregion_list:
            self.subregion_list.append(subregion)

    def gen(self, file):
        file.write('\n')
        file.write('SREGION')
        file.write('\n')
        file.write(self.slen)
        file.write(' ')
        file.write(self.nrreg)
        file.write(' ')
        file.write(self.zstep)
        file.write('\n')
        for subregion in self.subregions:
            subregion.gen(file)


class SubRegion(Region):
    """
    A SubRegion is a:
    (1) IRREG r-region number;
    (2) RLOW Innter radius of this r subregion;
    (3) RHIGH Outer radius of this r subregion;
    (4) Field object; and
    (5) Material object.
    """

    command_params = {
        'irreg':  {'desc': 'R-Region Number',
                   'type': 'Integer',
                   'req': True},

        'rlow':   {'desc': 'Inner radius of this r subregion',
                   'type': 'Real',
                   'req': True},

        'rhigh':   {'desc': 'Outer radius of this r subregion',
                    'type': 'Real',
                    'req': True},

        'field':   {'desc': 'Field object',
                    'type': 'Field',
                    'req': True},

        'material': {'desc': 'Material object',
                     'type': 'Material',
                     'req': True}
        }

    def __init__(self, **kwargs):
        if self.check_command_params_init(kwargs) is False:
            sys.exit(0)

    def __str__(self):
        return 'SubRegion:\n'+'irreg='+str(self.irreg) + '\n' + 'rlow=' + str(self.rlow) + '\n' + \
            'rhigh=' + str(self.rhigh) + '\n' + 'Field=' + str(self.field) + '\n' + 'Material=' + str(self.material)

    def __repr__(self):
        return 'SubRegion:\n'+'irreg='+str(self.irreg) + '\n' + 'rlow=' + str(self.rlow) + '\n' + \
            'rhigh=' + str(self.rhigh) + '\n' + 'Field=' + str(self.field) + '\n' + 'Material=' + str(self.material)

    def __setattr__(self, name, value):
        Region.__setattr__(self, name, value)


class ModeledCommandParameter(ICoolType):

    def __init__(self, kwargs):
        """
        Checks to see whether all required parameters are specified.  If not, raises exception and exits.
        """
        if self.check_model_keyword_args(kwargs) is False:
            sys.exit(0)
        self.set_keyword_args_model_specified(kwargs)

    def __call__(self, kwargs):
        """
        Checks to see whether new model specified in call.
        If so, checks that the parameters specified correspond to that model and raises an exception if they dont.
        Does NOT require all parameters specified for new model.  Unspecified parameters are set to 0.
        If model is not specified, checks whether the parameters specified correspond to the current model and
        raises an exception otherwise.
        """
        if self.check_model_specified(kwargs) is True:
            if self.check_partial_keywords_for_new_model(kwargs) is False:
                sys.exit(0)
            self.set_keyword_args_model_specified(kwargs)
            return
        """Model not specified"""
        if self.check_partial_keywords_for_current_model(kwargs) is False:
                sys.exit(0)
        self.set_keyword_args_model_not_specified(kwargs)

    def __setattr__(self, name, value):
        #Check whether the attribute being set is the model
        if name == self.get_model_descriptor_name():
            if self.check_valid_model(value) is False:
                return
            new_model = False
            #Check whether this is a new model (i.e. model was previously defined)
            if hasattr(self, self.get_model_descriptor_name()):
                new_model = True
                #Delete all attributes of the current model
                print 'Resetting model to ', value
                for key in self.get_model_dict(getattr(self, self.get_model_descriptor_name())):
                    if hasattr(self, key):
                        delattr(self, key)
            object.__setattr__(self, self.get_model_descriptor_name(), value)
            #If new model, set all attributes of new model to 0.
            if new_model is True:
                for key in self.get_model_dict(value):
                    if key is not self.get_model_descriptor_name():
                        setattr(self, key, 0)
            return
        try:
            if self.check_keyword_in_model(name):
                if self.check_model_variable_type(name, value):
                    object.__setattr__(self, name, value)
            else:
                raise ie.SetAttributeError('', self, name)
        except ie.InvalidType as e:
            print e
        except ie.SetAttributeError as e:
            print e

    def __str__(self):
        desc = 'ModeledCommandParameter\n'
        for key in self.get_model_dict(getattr(self, self.get_model_descriptor_name())):
            desc = desc + key + ': ' + str(getattr(self, key)) + '\n'
        return desc

    def set_keyword_args_model_specified(self, kwargs):
        setattr(self, self.get_model_descriptor_name(), kwargs[self.get_model_descriptor_name()])
        for key in kwargs:
            if not key == self.get_model_descriptor_name():
                setattr(self, key, kwargs[key])

    def set_keyword_args_model_not_specified(self, kwargs):
        for key in kwargs:
            object.__setattr__(self, key, kwargs[key])

    def reset_model(self):
        for key in self.get_model_dict(self.model):
            if hasattr(self, key):
                delattr(self, key)

    def check_model_keyword_args(self, input_dict):
        """
        Checks if ALL keywords for a model are specified.  If not, raises InputArgumentsError.
        If model is not specified, raises ModelNotSpecifiedError.
        Initialization of a model (e.g., Accel, SOL, etc. requires all keywords specified)
        """
        try:
            if not self.check_model_specified(input_dict):
                actual_dict = {'Unknown': 0}
                raise ie.InputArgumentsError('Model most be specified', input_dict, actual_dict)
            model = input_dict[self.get_model_descriptor_name()]
            if not str(model) in self.models.keys():
                raise ie.InvalidCommandParameter(str(model), self.models.keys())
            actual_dict = self.models[str(model)]['parms']
            if sorted(input_dict.keys()) != sorted(actual_dict.keys()):
                raise ie.InputArgumentsError('Model parameter specification error', input_dict, actual_dict)
        except ie.InputArgumentsError as e:
            print e
            return False
        except ie.InvalidCommandParameter as e:
            print e
            return False
        return True

    def check_valid_model(self, model):
        """
        Checks whether model specified is valid.
        If model is not valid, raises an exception and returns False.  Otherwise returns True.
        """
        try:
            if not str(model) in self.models.keys():
                raise ie.InvalidModel(str(model), self.models.keys())
        except ie.InvalidModel as e:
            print e
            return False
        return True

    def check_keyword_in_model(self, keyword):
        """
        Checks if given keyword specified is in the model associated with self.  If not, raises InputArgumentsError
        """
        if keyword in self.get_model_dict(getattr(self, self.get_model_descriptor_name())):
            return True
        else:
            return False

    def check_partial_keywords_for_current_model(self, input_dict):
        """
        Checks whether the keywords specified for a current model correspond to that model.
        """
        actual_dict = self.get_model_dict(getattr(self, self.get_model_descriptor_name()))
        for key in input_dict:
            if not key in actual_dict:
                raise ie.InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
        return True

    def check_partial_keywords_for_new_model(self, input_dict):
        """
        Checks whether the keywords specified for a new model correspond to that model.
        """
        model = input_dict[self.get_model_descriptor_name()]
        actual_dict = self.get_model_dict(model)
        for key in input_dict:
            if not key in actual_dict:
                raise ie.InputArgumentsError('Input Arguments Error', input_dict, actual_dict)
        return True

    def check_model_specified(self, input_dict):
        """
        Check whether the user specified a model in specifying parameters to Init or Call.
        if so, returns True.  Otherwise, returns False.
        """
        if self.get_model_descriptor_name() in input_dict.keys():
            return True
        else:
            return False

    def get_model_parms_dict(self):
        """
        Returns the parameter dictionary for the current model.
        """
        return self.get_model_dict(getattr(self, self.get_model_descriptor_name()))

    def get_model_dict(self, model):
        return self.models[str(model)]['parms']

    def get_model_descriptor_name(self):
        """
        The model descriptor name is an alias name for the term 'model', which is specified for each descendent class.
        Returns the model descriptor name.
        """
        return self.models['model_descriptor']['name']

    def check_model_variable_type(self, name, value):
        """Checks to see whether a particular variable for a model of name with value is of the correct type"""
        parms_dict = self.get_model_parms_dict()
        try:
            if self.check_type(parms_dict[name]['type'], value) is False:
                raise ie.InvalidType(parms_dict[name]['type'], value.__class__.__name__)
        except ie.InvalidType as e:
            print e
            return False
        return True

    def get_icool_model_name(self):
        return self.models[getattr(self, self.get_model_descriptor_name())]['icool_model_name']

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

        if icool_type == 'String':
            if isinstance(provided_type, str):
                return True
            else:
                return False
    
    def set_model_parameters(self):
        parms_dict = self.get_model_parms_dict()
        high_pos = 0
        for key in parms_dict:
            if key['pos'] > high_pos:
                high_pos = key['pos']
        self.parms = [0]*high_pos


class Distribution(ModeledCommandParameter):
    """
    A Distribution is a:
    (1) partnum (particle number);
    (2) bmtype Innter radius of this r subregion;
    (3) fracbt (R) fraction of beam of this type {0-1} The sum of all fracbt(i) should =1.0
    (4) bdistyp (I) beam distribution type {1:Gaussian 2:uniform circular segment}
    (5-16) 12 Parameters for bdistyp
    """

    models = {

        'model_descriptor': {'desc': 'Distribution type',
                             'name': 'bmdistyp',
                             'num_parms': 16},

        'gaussian':
        {'desc': 'Gaussian beam distribution',
         'doc': '',
         'parms':
                 {'partnum': {'pos': 1, 'type': 'Int', 'doc': '', 'min': 1, 'max': 5},
                  'bmtype': {'pos': 2, 'type': 'Int', 'doc': '', 'min': 1, 'max': 7},
                  'fractbt': {'pos': 3, 'type': 'Real', 'doc': '', 'min': 0, 'max': 1},
                  'bdistyp': {'pos': 4, 'type': 'String', 'doc': ''},
                  'x_mean': {'pos': 5, 'type': 'Real', 'doc': ''},
                  'y_mean': {'pos': 6, 'type': 'Real', 'doc': ''},
                  'z_mean': {'pos': 7, 'type': 'Real', 'doc': ''},
                  'px_mean': {'pos': 8, 'type': 'Real', 'doc': ''},
                  'py_mean': {'pos': 9, 'type': 'Real', 'doc': ''},
                  'pz_mean': {'pos': 10, 'type': 'Real', 'doc': ''},
                  'x_std': {'pos': 11, 'type': 'Real', 'doc': ''},
                  'y_std': {'pos': 12, 'type': 'Real', 'doc': ''},
                  'z_std': {'pos': 13, 'type': 'Real', 'doc': ''},
                  'px_std': {'pos': 14, 'type': 'Real', 'doc': ''},
                  'py_std': {'pos': 15, 'type': 'Real', 'doc': ''},
                  'pz_std': {'pos': 16, 'type': 'Real', 'doc': ''}}},

        'uniform':
        {'desc': 'Uniform circular segment beam distribution',
         'doc': '',
         'parms':
                 {'partnum': {'pos': 1, 'type': 'Int', 'doc': '', 'min': 1, 'max': 5},
                  'bmtype': {'pos': 2, 'type': 'Int', 'doc': '', 'min': 1, 'max': 7},
                  'fractbt': {'pos': 3, 'type': 'Real', 'doc': '', 'min': 0, 'max': 1},
                  'bdistyp': {'pos': 4, 'type': 'String', 'doc': ''},
                  'r_low': {'pos': 5, 'type': 'Real', 'doc': ''},
                  'r_high': {'pos': 6, 'type': 'Real', 'doc': ''},
                  'phi_low': {'pos': 7, 'type': 'Real', 'doc': ''},
                  'phi_high': {'pos': 8, 'type': 'Real', 'doc': ''},
                  'z_low': {'pos': 9, 'type': 'Real', 'doc': ''},
                  'z_high': {'pos': 10, 'type': 'Real', 'doc': ''},
                  'pr_low': {'pos': 11, 'type': 'Real', 'doc': ''},
                  'pr_high': {'pos': 12, 'type': 'Real', 'doc': ''},
                  'pphi_low': {'pos': 13, 'type': 'Real', 'doc': ''},
                  'pphi_high': {'pos': 14, 'type': 'Real', 'doc': ''},
                  'pz_low': {'pos': 15, 'type': 'Real', 'doc': ''},
                  'pz_high': {'pos': 16, 'type': 'Real', 'doc': ''}}},

        }

    def __init__(self, **kwargs):
        ModeledCommandParameter.__init__(self, kwargs)
    
    def __call__(self, **kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return self.dist + ':' + 'Distribution:' + ModeledCommandParameter.__str__(self)


class Correlation(ModeledCommandParameter):
    """
    A Correlation is a:
    (1) CORRTYP (I) correlation type
    (2) CORR1(i) (R) correlation parameter 1
    (3) CORR2(i) (R) correlation parameter 2
    (4) CORR3(i) (R) correlation parameter 3
    """
    models = {

        'model_descriptor': {'desc': 'Correlation type',
                             'name': 'corrtyp',
                             'num_parms': 4},

        'ang_mom':
        {'desc': 'Angular momentum appropriate for constant solenoid field',
         'doc': '',
         'icool_model_name': 1,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'sol_field': {'pos': 2, 'type': 'Real', 'doc': ''}}},

        'palmer':
        {'desc': 'Palmer amplitude correlation',
         'doc': '',
         'icool_model_name': 2,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'strength': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'beta_eff': {'pos': 3, 'type': 'Real', 'doc': ''}}},

        'rf_bucket_ellipse':
        {'desc': 'Rf bucket, small amplitude ellipse',
         'doc': '',
         'icool_model_name': 3,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'e_peak': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'phase': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'freq': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'rf_bucket_small_separatrix':
        {'desc': 'Rf bucket, small amplitude separatrix',
         'doc': '',
         'icool_model_name': 4,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'e_peak': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'phase': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'freq': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'rf_bucket_large_separatrix':
        {'desc': 'Rf bucket, small amplitude separatrix',
         'doc': '',
         'icool_model_name': 5,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'Real', 'doc': ''},
                  'e_peak': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'phase': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'freq': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'twiss_px':
        {'desc': 'Twiss parameters in x Px',
         'doc': '',
         'icool_model_name': 6,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'alpha': {'pos': 2, 'type': 'Real', 'doc': ''},
                  'beta': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'epsilon': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'twiss_py':
        {'desc': 'Twiss parameters in x Px',
         'doc': 'The spread in y and Py in the beam definition are ignored. '
                'For Gaussian distributions epsilon is the rms geometrical '
                'emittance. For uniform distributions it specifies the limiting ellipse.',
         'icool_model_name': 7,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'Real', 'doc': ''},
                  'alpha': {'pos': 2, 'type': 'Real', 'doc': 'Twiss alpha parameter [m]'},
                  'beta': {'pos': 3, 'type': 'Real', 'doc': 'Twiss beta parameter [m]'},
                  'epsilon': {'pos': 4, 'type': 'Real', 'doc': 'Twiss epsilon parameter [m]'}}},

        'equal_sol':
        {'desc': 'Equal time in solenoid.',
         'doc':  'Set up with pz and σPz such that βz > βo. '
                 'Set up initial pt = 0. This correlation determines the pt '
                 'for a given pz that gives all the initial particles the same βo. '
                 'If parameter 3 is 0, the azimuthal angle is chosen randomly.',
         'icool_model_name': 9,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'Real', 'doc': ''},
                  'axial_beta': {'pos': 2, 'type': 'Real', 'doc': 'desired axial beta (=v/c) value βo'},
                  'az_ang_mom': {'pos': 3, 'type': 'Real', 'doc': 'azimuthal angle of transverse momentum [deg]'}}},

        'balbekov':
        {'desc': 'Balbekov version of amplitude-energy.',
         'doc':  '',
         'icool_model_name': 10,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'eref': {'pos': 2, 'type': 'Real', 'doc': 'Eref [GeV]'},
                  'babs': {'pos': 3, 'type': 'Real', 'doc': 'Babs [ T ]'},
                  'sigma_e:': {'pos': 4, 'type': 'Real', 'doc': 'σE [GeV]'}}},

        'dispersion':
        {'desc': 'Dispersion',
         'doc':  '',
         'icool_model_name': 11,
         'parms':
                 {'corrtyp': {'pos': 1, 'type': 'String', 'doc': ''},
                  'value': {'pos': 2, 'type': 'Real', 'doc': '[m or rad]'},
                  'pref': {'pos': 3, 'type': 'Real', 'doc': '[GeV/c]'},
                  'type': {'pos': 4, 'type': 'Real', 'doc': 'Type flag.  x, y, x_prime, y_prime'}}},


        }

    def __init__(self, **kwargs):
        ModeledCommandParameter.__init__(self, kwargs)
    
    def __call__(self, **kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return self.corrtyp + ':' + 'Correlation:' + ModeledCommandParameter.__str__(self)


class BeamType(ICoolVariablesSet):
    """
    A BeamType is a:
    PARTNUM (I) particle number
    BMTYPE (I) beam type {magnitude = mass code; sign = charge}
        1: e
        2: μ
        3: π
        4: K
        5: p
        6: d
        7: He3
        8: Li7
    FRACBT (R) fraction of beam of this type {0-1} The sum of all fracbt(i) should =1.0
    """
    variables = {
        'partnum':  {'default': None,
                     'desc': 'Particle number',
                     'type': 'Integer',
                     'req': True},

        'bmtype':   {'default': None,
                     'desc': 'beam type {magnitude = mass code; sign = charge}: 1: e, 2: μ, 3: π, 4: K, 5: p.'
                     '6: d, 7: He3, 8: Li7',
                     'type': 'Integer',
                     'req': True},

        'fractbt': {'default': None,
                    'desc': 'Fraction of beam of this type {0-1} The sum of all fracbt(i) should =1.0',
                    'type': 'Real',
                    'req': True},
        'bdistyp': {'default': None,
                    'desc': 'Beam distribution type {1:Gaussian 2:uniform circular segment}',
                    'type': 'Distribution',
                    'req': True}}

    def __init__(self, **kwargs):
        if self.check_variables_init(kwargs) is False:
            sys.exit(0)

    def __str__(self):
        return 'BeamType: \n'

    def __repr__(self):
        return '[BeamType: ]'


class Field(ModeledCommandParameter):
    """
    A Field is a:
    FTAG - A tag identifying the field.  Valid FTAGS are:
    ACCEL, BLOCK, BROD, BSOL, COIL, DIP, EFLD, FOFO, HDIP, HELI(X), HORN, KICK, QUAD,
    ROD, SEX, SHEE(T), SOL, SQUA, STUS, WIG

    FPARM - 15 parameters describing the field.  The first parameter is the model.
    """
    def __init__(self, ftag, kwargs):
        ModeledCommandParameter.__init__(self, kwargs)
        self.ftag = ftag

    def __call__(self, kwargs):
        ModeledCommandParameter.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'fparm':
            object.__setattr__(self, name, value)
        else:
            ModeledCommandParameter.__setattr__(self, name, value)

    def __str__(self):
        return self.ftag #+ ':' + 'Field:' + ModeledCommandParameter.__str__(self)

    def gen_fparm(self):
        self.fparm = [0] * 10
        cur_model = self.get_model_dict(self.model)
        for key in cur_model:
            pos = int(cur_model[key]['pos'])-1
            if key == self.get_model_descriptor_name():
                val = self.get_icool_model_name()
            else:
                val = getattr(self, key)
            self.fparm[pos] = val
        print self.fparm

    def gen(self, file):
        file.write('\n')
        file.write(self.ftag)
        file.write('\n')
        for s in self.fparm:
            file.write(s)
            file.write(" ")


class Material(ModeledCommandParameter):
    """
    A Material is a:
    (1) MTAG (A) material composition tag
    (2) MGEOM (A) material geometry tag
    (3-12) GPARM (R) 10 parameters that describe the geometry of the material

    Enter MTAG in upper case.
    Valid MTAG'S are:

    VAC vacuum (i.e., no material)
    GH gaseous hydrogen
    GHE gaseous helium
    LH liquid hydrogen
    LHE liquid helium
    LI BE B C AL TI FE CU W HG PB (elements)
    LIH lithium hydride
    CH2 polyethylene
    SS stainless steel (alloy 304)

    Valid MGEOM's are:

    NONE use for vacuum
    10*0.

    CBLOCK cylindrical block
    10*0.
    ...

    """
    materials = {
        'vac': {'desc': 'Vacuum (no material)'},
        'gh':  {'desc': 'Gaseous hydrogen'},
        'ghe': {'desc': 'Gaseous helium'},
        'lh':  {'desc': 'Liquid hydrogen'},
        'lhe': {'desc': 'Liquid helium'},
        'Li':  {'desc': 'Lithium'},
        'Be':  {'desc': 'Berylliyum'},
        'B':   {'desc': 'Boron'},
        'C':   {'desc': 'Carbon'},
        'Al':  {'desc': 'Aluminum'},
        'Ti':  {'desc': 'Titanium'},
        'Fe':  {'desc': 'Iron'},
        'Cu':  {'desc': 'Copper'},
        'W':   {'desc': 'Tungsten'},
        'Hg':  {'desc:': 'Mercury'},
        'Pb':  {'desc:': 'Lead'}
        }
    
    models = {

        'model_descriptor': {'desc': 'Geometry',
                             'name': 'geom',
                             'num_parms': 12},
        'vac':
        {'desc': 'Vacuum',
         'doc': 'Vacuum region.  Specify vacuum for mtag.  Geom will be set to NONE.',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''}}},

        'cblock':
        {'desc': 'Cylindrical block',
         'doc': 'Cylindrical block',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''}}},

         'aspw':
        {'desc': 'Azimuthally Symmetric Polynomial Wedge absorber region',
         'doc': 'Edge shape given by '
                'r(dz) = a0 + a1*dz + a2*dz^2 + a3*dz^3 in the 1st quadrant and '
                'where dz is measured from the wedge center. '
                '1 z position of wedge center in region [m] '
                '2 z offset from wedge center to edge of absorber [m] '
                '3 a0 [m] '
                '4 a1 '
                '5 a2 [m^(-1)] '
                '6 a3 [m^(-2)]',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'zpos': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'zoff': {'pos': 4, 'type': 'Real', 'doc': ''},
                  'a0': {'pos': 5, 'type': 'Real', 'doc': ''},
                  'a1': {'pos': 6, 'type': 'Real', 'doc': ''},
                  'a2': {'pos': 7, 'type': 'Real', 'doc': ''},
                  'a3': {'pos': 8, 'type': 'Real', 'doc': ''}}},

         'asrw':
        {'desc': 'Azimuthally Symmetric Polynomial Wedge absorber region',
         'doc': 'Edge shape given by '
                'r(dz) = a0 + a1*dz + a2*dz^2 + a3*dz^3 in the 1st quadrant and '
                'where dz is measured from the wedge center. '
                '1 z position of wedge center in region [m] '
                '2 z offset from wedge center to edge of absorber [m] '
                '3 a0 [m] '
                '4 a1 '
                '5 a2 [m^(-1)] '
                '6 a3 [m^(-2)]',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'zpos': {'pos': 3, 'type': 'Real', 'doc': ''},
                  'zoff': {'pos': 4, 'type': 'Real', 'doc': ''},
                  'a0': {'pos': 5, 'type': 'Real', 'doc': ''},
                  'a1': {'pos': 6, 'type': 'Real', 'doc': ''},
                  'a2': {'pos': 7, 'type': 'Real', 'doc': ''},
                  'a3': {'pos': 8, 'type': 'Real', 'doc': ''}}},


        'hwin':
        {'desc': 'Hemispherical absorber end region',
         'doc': '1 end flag {-1: entrance, +1: exit} '
                '2 inner radius of window[m] '
                '3 window thickness [m] '
                '4 axial offset of center of spherical window from start of end region [m]',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'end_flag': {'pos': 3, 'type': 'Real', 'doc': 'End flag {-1: entrance, +1: exit}'},
                  'in_rad': {'pos': 4, 'type': 'Real', 'doc': 'Inner radius of window'},
                  'thick': {'pos': 5, 'type': 'Real', 'doc': 'Thickness of window'},
                  'offset': {'pos': 6, 'type': 'Real', 'doc': 'Axial offset of center of spherical '
                             'window from start of end region [m]'}}},

        'nia':
        {'desc': 'Non-isosceles absorber',
         'doc': '1 zV distance of wedge “center” from start of region [m] '
                '2 z0 distance from center to left edge [m] '
                '3 z1 distance from center to right edge [m] '
                '4 θ0 polar angle from vertex of left edge [deg] '
                '5 φ0 azimuthal angle of left face [deg] '
                '6 θ1 polar angle from vertex of right edge [deg] '
                '7 φ1 azimuthal angle of right face [deg]',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'zv': {'pos': 3, 'type': 'Real', 'doc': 'Distance of wedge “center” from start of region [m]'},
                  'z0': {'pos': 4, 'type': 'Real', 'doc': 'Distance from center to left edge [m] '},
                  'z1': {'pos': 5, 'type': 'Real', 'doc': 'Distance from center to right edge [m]}'},
                  'θ0': {'pos': 6, 'type': 'Real', 'doc': 'Polar angle from vertex of left edge [deg]'},
                  'φ0': {'pos': 7, 'type': 'Real', 'doc': 'Azimuthal angle of left face [deg]'},
                  'θ1': {'pos': 8, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                  'φ1': {'pos': 9, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'}}},
                             
        'pwedge':
        {'desc': 'Asymmetric polynomial wedge absorber region',
         'doc': 'Imagine the wedge lying with its narrow end along the x axis. The wedge is symmetric about the '
                'x-y plane. The edge shape is given by dz(x) = a0 + a1*x + a2*x^2 + a3*x^3 '
                'where dz is measured from the x axis.',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'init_vertex': {'pos': 3, 'type': 'Real', 'doc': 'Initial position of the vertex along '
                                  'the x axis [m]'},
                  'z_wedge_vertex': {'pos': 4, 'type': 'Real', 'doc': 'z position of wedge vertex [m] '},
                  'az': {'pos': 5, 'type': 'Real', 'doc': 'Azimuthal angle of vector pointing to vertex in plane '
                         'of wedge w.r.t. +ve x-axis [deg]'},
                  'width': {'pos': 6, 'type': 'Real', 'doc': 'Total width of wedge in dispersion direction [m]'},
                  'height': {'pos': 7, 'type': 'Real', 'doc': 'Total height of wedge in non-dispersion direction [m]'},
                  'a0': {'pos': 8, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                  'a1': {'pos': 9, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'},
                  'a2': {'pos': 10, 'type': 'Real', 'doc': 'Polar angle from vertex of right edge [deg] '},
                  'a3': {'pos': 11, 'type': 'Real', 'doc': 'Azimuthal angle of right face [deg]'}}},

        'ring':
        {'desc': 'Annular ring of material',
         'doc': 'This is functionally equivalent to defining a region with two radial subregions, the first of '
                 'which has vacuum as the material type. However, the boundary crossing algorithm used for RING is '
                 'more sophisticated and should give more accurate simulations.',
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'inner': {'pos': 3, 'type': 'Real', 'doc': 'Inner radius (R) [m]'},
                  'outer': {'pos': 4, 'type': 'Real', 'doc': 'Outer radius (R) [m]'}}},

        'wedge':
        {'desc': 'Asymmetric wedge absorber region',
         'doc': 'We begin with an isosceles triangle, sitting on its base, vertex at the top. '
         'The base-to-vertex distance is W. The full opening angle at the vertex is A. Using '
         'two of these triangles as sides, we construct a prism-shaped wedge. The distance from '
         'one triangular side to the other is H. The shape and size of the wedge are now established. '
         'We define the vertex line of the wedge to be the line connecting the vertices of its two '
         'triangular sides.  Next, we place the wedge in the right-handed ICOOL coordinate system. '
         'The beam travels in the +Z direction. Looking downstream along the beamline (+Z into the page), '
         '+X is horizontal and to the left, and +Y is up.  Assume the initial position of the wedge is as '
         'follows: The vertex line of the wedge is vertical and lies along the Y axis, extending from Y = -H/2 '
         'to Y = +H/2. The wedge extends to the right in the direction of -X, such that it is symmetric about '
         "the XY plane. (Note that it is also symmetric about the XZ plane.) From the beam's point of view, "
         'particles passing on the +X side of the Y axis will not encounter the wedge, while particles passing '
         'on the -X side of the Y axis see a rectangle of height H and width W, centered in the Y direction, with '
         'Z thickness proportional to -X.  '
         'By setting parameter U to a non-zero value, the user may specify that the wedge is to be '
         'translated in the X direction. If U>0, the wedge is moved (without rotation) in the +X direction. '
         'For example, if U = W/2, then the wedge is centered in the X direction; its vertex is at X = W/2 '
         'and its base is at X = -W/2. Note that the wedge is still symmetric about both the XY plane and '
         'the XZ plane. '
         'Next, the wedge may be rotated about the Z axis by angle PHI. Looking downstream in the beam '
         'direction, positive rotations are clockwise and negative rotations are counter-clockwise. For '
         'example, setting PHI to 90 degrees rotates the wedge about the Z axis so that its vertex line is '
         'parallel to the X axis and on top, while its base is parallel to the XZ plane and at the bottom. In '
         'general this rotation breaks the symmetry about the XZ plane, but the symmetry about the XY '
         'plane is maintained. '
         'Finally, the wedge is translated in the Z direction by a distance Zv, so that its XY symmetry plane '
         'lies a distance Zv downstream of the start of the region. Usually Zv should be at least large '
         'enough so that the entire volume of the wedge lies within its region, i.e. Zv .ge. W tan (A/2), the '
         'maximum Z half-thickness of the wedge. As well, the region usually should be long enough to '
         'contain the entire volume of the wedge, i.e. RegionLength .ge. Zv + W tan (A/2). Wedges that do '
         'lie completely within their region retain their symmetry about the XY plane Z=Zv.  '
         'If portions of a wedge lie outside their region in Z, then the volume of the wedge lying outside '
         'the region is ignored when propagating particles through the wedge. Such a wedge will grow in '
         'thickness until it reaches the region boundary, but will not extend beyond it. In such cases, '
         'wedges may lose their symmetry about the XY plane Z=Zv.'
         'Wedges may be defined such that they extend outside the radial boundaries of the radial '
         'subregion within which they are defined. However, any portion of the wedge volume lying inside the inner '
         'radial boundary or outside the outer radial boundary is ignored when propagating particles through '
         'the wedge. For example, if the user intends that an entire radial subregion of circular cross-section be '
         'filled with a wedge, then it is clear that the corners of the wedge must extend outside the radial region, '
         "but particles passing outside the wedge's radial subregion will not see the wedge at all.  "
         'In short, we may say that although it is permitted (and sometimes essential) to define a wedge to '
         'be larger than its subregion, for the purposes of particle propagation the wedge is always trimmed at the '
         "region's Z boundaries and the subregion's radial boundaries. Any volume within the region and subregion "
         'that is not occupied by the material specified for the wedge is assumed to be vacuum.'
         '------------------------------------------------------------------------------------------------------------'
         'Example 1: Within a region 0.4 meters long in Z, within a radial subregion extending from the Z axis out '
         'to a radius of 0.3 meters, a wedge is to fill the X<0 (right) half of the 0.3 meter aperture of the '
         'subregion, and increase in Z thickness proportional to -X, such that it is 0.2 meters thick at the '
         'rightmost point in the subregion (X=-0.3, Y=0).  The wedge is to be 0.2 meters thick at a point 0.3 '
         'meters from its vertex. The half-thickness is 0.1 meters, the half-opening angle is '
         'atan (0.1/0.3) = 18.4 degrees, so the full opening angle of the wedge A is 36.8 degrees. The width '
         '(X extent) of the wedge must be 0.3 meters, and the height (Y extent) of the wedge must be 0.6 meters. '
         'Two corners of the wedge extend well beyond the subregion, but they will be ignored during particle '
         'propagation. The wedge does not need to be translated in X (U = 0) nor does it need to be rotated '
         'about the Z axis (PHI = 0). For convenience we center the wedge (in Z) within its region, '
         'so Zv = 0.2 meters. Since the maximum half-thickness of the wedge is only 0.1 meters, the wedge '
         'does not extend beyond (or even up to) the Z boundaries of the region. The volume within the region '
         'and subregion but outside the wedge is assumed to be vacuum.'
         '------------------------------------------------------------------------------------------------------------'
         'Example 2: In the same region and subregion, we need a wedge with the same opening angle, '
         'but filling the entire aperture of the subregion, thickness gradient in the +Y direction, thickness = '
         '0 at the lowest point in the subregion (X=0, Y=-0.3).'
         'The wedge must now have H = W = 0.6 meters so it can fill the entire aperture of the subregion.'
         'From its initial position, it must first be translated 0.3 meters in the +X direction (U = 0.3) to '
         "center it in the subregion's aperture, and then (from the perspective of someone looking "
         'downstream along the beam) rotated counterclockwise 90 degrees (PHI = -90.) so that the Z '
         'thickness increases proportionally to +Y. Since the wedge has the same opening angle as before '
         'but has twice the width, its maximum Z thickness is now 0.4 meters, just barely fitting between '
         'the Z boundaries of the region if Zv = 0.2 meters. All four corners of the wedge now extend '
         "outside the radial subregion's outer boundary, but they will be ignored during particle "
         'propagation.” {S.B.}'
         'The wedge geometry can accept a second MTAG parameter in the SREGION construct. The first material '
         'refers to the interior of the wedge. The second material, if present, refers to the exterior of the wedge. '
         'If a second MTAG parameter is not present, vacuum is assumed.',
         
         'parms':
                 {'mtag': {'pos': 1, 'type': 'String', 'doc': ''},
                  'geom': {'pos': 2, 'type': 'String', 'doc': ''},
                  'vert_ang': {'pos': 3, 'type': 'Real', 'doc': 'Full angle at vertex, α (or A) [degrees]'
                                  'the x axis [m]'},
                  'vert_init': {'pos': 4, 'type': 'Real', 'doc': 'Initial position of the vertex along '
                                'the x axis, U [m]'},
                  'vert_z': {'pos': 5, 'type': 'Real', 'doc': 'Z position of wedge vertex, Zv [m]'},
                  'vert_az': {'pos': 6, 'type': 'Real', 'doc': 'azimuthal angle φ of vector pointing to vertex '
                              'in plane of wedge w.r.t. +ve x-axis [deg]'},
                  'width': {'pos': 7, 'type': 'Real', 'doc': 'Total width of wedge in dispersion direction, w [m]'},
                  'height': {'pos': 8, 'type': 'Real', 'doc': 'Total height of wedge in non-dispersion direction, '
                             'h [m]'}}}
}


    def __init__(self, **kwargs):
        ModeledCommandParameter.__init__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'mparm':
            object.__setattr__(self, name, value)
        else:
            ModeledCommandParameter.__setattr__(self, name, value)

    

    def gen_mparm(self):
        self.mparm = [0] * 12
        cur_model = self.get_model_dict(self.geom)
        for key in cur_model:
            pos = int(cur_model[key]['pos'])-1
            val = getattr(self, key)
            self.mparm[pos] = val
        print self.mparm

    def gen(self, file):
        file.write('\n')
        file.write(self.mtag)
        file.write('\n')
        file.write(self.mgeom)
        file.write('\n')
        for s in mparm:
            file.write(s)
            file.write(" ")


class Accel(Field):
    """ACCE(L) linear accelerator fields
    1 Model
    1: EZ only with no transverse variation
    2: cylindrical TM01p pillbox resonator
    3: traveling wave cavity
    4: approximate fields for symmetric circular-nosed cavity
    5: user-supplied azimuthally-symmetric TM mode (SuperFish) RF field
    6: induction linac model - waveform from user-supplied polynomial coefficients
    7: induction linac model - internally generated waveform
    8: induction linac model - waveform from user-supplied file
    9: sector-shaped pillbox cavity (circular cross section)
    10: variable {frequency, gradient} pillbox cavity
    11: straight pillbox or SuperFish cavity in dipole region
    12: sector-shaped pillbox cavity (rectangular cross section)
    13: open cell standing wave cavity

    The initial phase parameter can be used for any PHASEMODEL and ACCEL models 1-5.

    For model = 1
    2 frequency [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}
    5 parameter to approximate a rectangular cavity in cylindrical geometry.
    if set to radius of curvature rho, then E_z is scaled by 1-x/rho, where x is the horizontal
    distance from the reference circle.
    6 (not used)
    7 (not used)
    8 mode
    0 : time-independent
    1: sinusoidal time variation

    For model = 2
    2 frequency f [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 parameter to approximate a rectangular cavity in cylindrical geometry; if set to radius of
    curvature rho, then the field components are scaled by 1-x/rho, where x is the horizontal
    distance from the reference circle.
    6 x offset of cavity [m]
    7 y offset of cavity [m]
    8 longitudinal mode p {0,1}
    For mode = 0 Rcav = 0.383 * lambda
    For mode = 1 Rcav = 2.405 / {(2pi f)^2 - (pi/SLEN)^2)}^(1/2)

    For model = 3
    2 frequency f [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 (not used)
    6 (not used)
    7 (not used)
    8 phase velocity of RF wave B_omega. {0<B_omega<1}

    For model = 4
    2 frequency [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 (not used)
    6 (not used)
    7 (not used)
    8 total length of cavity [m]
    9 total gap [m]
    10 radius of drift tube [m]
    11 radius of nose piece [m]

    For model = 5
    2 frequency[MHz]
    4 phase shift [deg] {0-360}.
    8 file ## of azimuthally symmetric RF input file (see below) {20-99}
    9 field strength normalization factor [MV/m] This multiplies the value in the SuperFish file.
    10 radial cutoff for cavity [m]
    11 axial distance from start of region to centerline of cavity [m]
    12 axial symmetry through center of cavity
    0: symmetric
    1: not symmetric
    The contents of the user-supplied file FOR0##.DAT has the same format as the Parmela output of
    the SuperFish postprocessor SF07.
    1.1 zmin Start of axial grid [cm]
    1.2 zmax End of axial grid [cm]
    1.3 Nz # of z grid points {<251}
    2 frequency [MHz]
    3.1 rmin Start of radial grid [cm]
    3.2 rmax End of radial grid [cm]
    3.3 Nr # of r grid points {<151}
    for ir=1,Nr
    for iz=1,Nz
    4.1 Ez axial electric field [MV/m]
    4.2 Er radial electric field [MV/m]
    4.3 E magnitude of electric field [MV/m]
    4.4 Hphi azimuthal magnetic field [A/m]
    next iz
    next ir
    The grids should extend beyond the region where tracking will occur.

    For model = 6
    2 time offset from start of voltage pulse[s]
    3 accelerator gap [m]
    4 time reset parameter (see below)
    5 V0 term in polynomial expansion of voltage pulse [V ]
    6 V1 term in polynomial expansion of voltage pulse [V / mu_ss]
    7 V2 term in polynomial expansion of voltage pulse [V / mu_s^2]
    8 V3 term in polynomial expansion of voltage pulse [V / mu_s^3]
    9 V4 term in polynomial expansion of voltage pulse [V / mu_s^4]
    10 V5 term in polynomial expansion of voltage pulse[V / mu_s^5]
    11 V6 term in polynomial expansion of voltage pulse[V / mu_s^6]
    12 V7 term in polynomial expansion of voltage pulse[V / mu_s^7]
    13 V8 term in polynomial expansion of voltage pulse[V / mu_s^8]

    This model generates an EZ field across the accelerator gap. The field is time
    dependent, but does not depend on z or r. The radial electric field and azimuthal
    magnetic fields are assumed to be negligible. When the time reset parameter is 1,
    the start time for the voltage pulse is determined from the time the reference particle
    entered the cell. The user can adjust this time using parameter #2 above. Subsequent cells
    should use parameter #4 set to 0 to sample later portions of the same voltage pulse.
    A new pulse shape can be started at any time by setting parameter #4 back to 1.

    For model = 7
    2 number of gaps
    3 starting voltage [GV]
    4 voltage swing [GV]
    5 time offset [s]
    6 target kinetic energy [GeV]
    7 pulse duration [s]
    8 parameter to adjust slope at end of voltage pulse
    9 number of bins in voltage pulse
    10 gap length [m]
    11 file # of output diagnostic file {20-99} (Set this <20 for no diagnostic output.)
    12 kill particle flag (Set=1 to eliminate non-useful particles)
    13 restart flag (Set =1 to restart calculation)
    This model, based on a routine by Charles Kim, uses the local E-t phase space to create a voltage
    waveform that attempts to flatten out the kinetic energy along the pulse. The diagnostic file contains
    the following information:
    Region number
    Time bin, n
    t(n)
    V(n)
    EK(n)
    wt1(n) total event weight in this bin
    wt2(n) event weight inside the chosen energy range
    sigEK(n)
    Vstart
    Vend

    For model = 8
    2 time offset from start of voltage pulse[s]
    3 accelerator gap [m]
    4 time reset parameter [s](see below)
    5 file number of waveform input (see format below) {20-99}
    6 polynomial interpolation order, 1=> linear, 2=>quadratic, etc. {1-3}
    7 file # for output diagnostic file (see format below){20-99}
    8 time increment between diagnostic outputs to file [s]
    This model generates an EZ field across the accelerator gap. The field is time
    dependent, but does not depend on z or r. The radial electric field and azimuthal
    magnetic fields are assumed to be negligible. The gap parameter is used to convert
    the voltage profile into an electric field. The field is applied everywhere in the region.
    When the time reset parameter is 1, the start time for the voltage pulse is determined
    from the time the reference particle entered the cell. The user can adjust this time using
    parameter #2 above. Subsequent cells can use parameter #4 set to 0 to sample later portions of
    the same voltage pulse. A new pulse shape can be started at any time by setting parameter #4
    back to 1.
    The contents of the waveform input file FOR0##.DAT is
    1) number of points N {1-100}
    This is followed by N pairs
    2) t(i) V(i) [s] [V]
    An output diagnostic file is initialized for an induction linac region where the time reset
    parameter=1 and parameter 7 above is in the range {20-99}. Output occurs when the elapsed
    time from the previous output exceeds the increment given in parameter 8. Output continues for
    subsequent induction linac regions provided parameter 7 remains in the specified range. The
    contents of the file are
    1) column id header
    2) region particle z t Ez

    For model = 9
    2 frequency f[MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.

    For model = 10
    2 (not used)
    3 (not used)
    4 phase shift [deg] {0-360}.
    5 number of wavelengths separating the two reference particles
    6 reset parameter (see below)
    7 Total length L of buncher [m]
    8 g0 [MV/m]
    9 g1 [MV/m]
    10 g2 [MV/m]
    11 (not used)
    12 phase model
    0: 0-crossing time set by tREFP
    1: 0-crossing time set by (1/2) * (tREFP + t REF2)
    This model uses a TM010 mode pillbox cavity. It can only be used with REFP and REF2
    defined and phasemodel=2,3,4. The cavity frequency is set using the number of wavelengths
    (parameter 5) and the time difference between the two reference particles. When the reset
    parameter is 1, the starting location of the buncher is determined from the current position
    of the reference particle. Subsequent ACCEL commands should use parameter #6 set to 0 to
    sample later portions of the gradient waveform, which is given by
    G = g0 + g1*(z/L) + g2*(z/L)^2
    A new pulse shape can be started at any time by setting parameter #6 back to 1.

    For model = 11
    2 frequency f [MHz]
    3 gradient on-axis at center of gap for a pillbox cavity [MV/m]
    4 phase shift [deg] {0-360}.
    5 radial offset of center of cavity from reference trajectory [m]
    6 axial length of cavity [m] If this entered as 0, the program computes the largest pillbox
    cavity that fits in the sector shaped region
    7 cavity type
    0: pillbox
    1: SuperFish
    8 file ## of azimuthally symmetric SuperFish RF input file (see model 5) {20-99}
    9 SuperFish field normalization [MV/m] This multiplies the value in the SuperFish file.
    10 SuperFish radial cut off [m]
    11 axial displacement of center of SuperFish cavity from start of the region [m]
    12 SuperFish axial symmetry
    0: symmetric
    1: not symmetric

    For model = 12
    2 frequency f[MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 radial offset of center of cavity from reference trajectory [m]
    6 cavity width [m]
    7 cavity height [m]

    For model = 13
    2 frequency f [MHz]
    3 gradient on-axis at center of gap [MV/m]
    4 phase shift [deg] {0-360}.
    5 flag for hard edge focusing
        0: both entrance and exit focusing
        1: exit focusing only
        2: entrance focusing only
        3: no edge focusing

"""
    models = {

        'model_descriptor': {'desc': 'Name of model parameter descriptor',
                             'name': 'model'},

        'ez': {'desc': 'Ez only with no transverse variation',
               'doc': '',
               'icool_model_name': 1,
               'parms':
                       {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                        'freq': {'pos': 2, 'type': 'Real', 'doc': 'Frequency [MHz]'},
                        'grad': {'pos': 3, 'type': 'Real', 'doc': 'Gradient on-axis at center of gap [MV/m]'},
                        'phase': {'pos': 4, 'type': 'Real', 'doc': 'Phase shift [deg] {0-360}.'},
                        'rect_cyn': {'pos': 5, 'type': 'Real', 'doc': 'Parameter to approximate a rectangular cavity '
                                     'in cylindrical geometry; if set to radius of curvature ρ, then EZ is scaled by '
                                     '1-x/ ρ, where x is the horizontal distance from the reference circle.'},
                        'mode': {'pos': 8, 'type': 'Int', 'doc': '0 : Time-independent 1: sinusoidal time '
                                 'variation'}}},

        'cyn_pill': {'desc': 'Cylindrical TM01p pillbox',
                     'doc': '',
                     'icool_model_name': 2,
                     'parms':
                             {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                              'freq': {'pos': 2, 'type': 'Real', 'doc': ''},
                              'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                              'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                              'rect_cyn': {'pos': 5, 'type': 'Real', 'doc': ''},
                              'longitudinal_mode': {'pos': 8, 'type': 'Real', 'doc': ''}}},

        'trav': {'desc': 'Traveling wave cavity',
                 'doc': '',
                 'icool_model_name': 3,
                 'parms':
                         {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                          'freq': {'pos': 2, 'type': 'Real', 'doc': ''},
                          'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                          'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                          'rect_cyn': {'pos': 5, 'type': 'Real', 'doc': ''},
                          'x_offset': {'pos': 6, 'type': 'Real', 'doc': ''},
                          'y_offset': {'pos': 7, 'type': 'Real', 'doc': ''},
                          'phase_velocity': {'pos': 8, 'type': 'Real', 'doc': ''}}},

        'circ_nose': {'desc': 'Approximate fields for symmetric circular-nosed cavity',
                      'doc': '',
                      'icool_model_name': 4,
                      'parms':
                              {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                               'freq': {'pos': 2, 'type': 'Real', 'doc': ''},
                               'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                               'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                               'length': {'pos': 8, 'type': 'Real', 'doc': ''},
                               'gap': {'pos': 9, 'type': 'Real', 'doc': ''},
                               'drift_tube_radius': {'pos': 10, 'type': 'Real', 'doc': ''},
                               'nose_radius': {'pos': 11, 'type': 'Real', 'doc': ''}}},

        'az_tm': {'desc': 'User-supplied azimuthally-symmetric TM mode (SuperFish)',
                  'doc': '',
                  'icool_model_name': 5,
                  'parms':
                          {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                           'freq': {'pos': 2,  'type': 'Real', 'doc': ''},
                           'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                           'file_no': {'pos': 8, 'type': 'Real', 'doc': ''},
                           'field_strength_norm': {'pos': 9, 'type': 'Real', 'doc': ''},
                           'rad_cut': {'pos': 10, 'type': 'Real', 'doc': ''},
                           'axial_dist': {'pos': 11, 'type': 'Real', 'doc': ''},
                           'daxial_sym': {'pos': 12, 'type': 'Real', 'doc': ''}}},

        'ilpoly': {'desc': 'Induction linac model - waveform from user-supplied polynomial coefficients',
                   'doc': '',
                   'icool_model_name': 6,
                   'parms':
                          {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                           'time_offset': {'pos': 2,  'type': 'Real', 'doc': ''},
                           'gap': {'pos': 3, 'type': 'Real', 'doc': ''},
                           'time_reset': {'pos': 4, 'type': 'Real', 'doc': ''},
                           'v0': {'pos': 5, 'type': 'Real', 'doc': ''},
                           'v1': {'pos': 6, 'type': 'Real', 'doc': ''},
                           'v2': {'pos': 7, 'type': 'Real', 'doc': ''},
                           'v3': {'pos': 8, 'type': 'Real', 'doc': ''},
                           'v4': {'pos': 9, 'type': 'Real', 'doc': ''},
                           'v5': {'pos': 10, 'type': 'Real', 'doc': ''},
                           'v6': {'pos': 11, 'type': 'Real', 'doc': ''},
                           'v7': {'pos': 12, 'type': 'Real', 'doc': ''},
                           'v8': {'pos': 13, 'type': 'Real', 'doc': ''}}},

        'ilgen': {'desc': 'Induction linac model - waveform from internally generated waveform',
                  'doc': '',
                  'icool_model_name': 7,
                  'parms':
                          {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                           'num_gaps': {'pos': 2,  'type': 'Real', 'doc': ''},
                           'start_volt': {'pos': 3, 'type': 'Real', 'doc': ''},
                           'volt_swing': {'pos': 4, 'type': 'Real', 'doc': ''},
                           'time_offset': {'pos': 5, 'type': 'Real', 'doc': ''},
                           'kin': {'pos': 6, 'type': 'Real', 'doc': ''},
                           'pulse_dur': {'pos': 7, 'type': 'Real', 'doc': ''},
                           'slope': {'pos': 8, 'type': 'Real', 'doc': ''},
                           'bins': {'pos': 9, 'type': 'Real', 'doc': ''},
                           'gap_len': {'pos': 10, 'type': 'Real', 'doc': ''},
                           'file_num': {'pos': 11, 'type': 'Real', 'doc': ''},
                           'kill': {'pos': 12, 'type': 'Real', 'doc': ''},
                           'restart': {'pos': 13, 'type': 'Real', 'doc': ''}}},

        'ilfile': {'desc': 'Induction linac model - Waveform from user-supplied file',
                   'doc': '',
                   'icool_model_name': 8,
                   'parms':
                          {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                           'time_offset': {'pos': 2,  'type': 'Real', 'doc': ''},
                           'gap': {'pos': 3, 'type': 'Real', 'doc': ''},
                           'time_reset': {'pos': 4, 'type': 'Real', 'doc': ''},
                           'file_num_wav': {'pos': 5, 'type': 'Real', 'doc': ''},
                           'poly_order': {'pos': 6, 'type': 'Real', 'doc': ''},
                           'file_num_out': {'pos': 7, 'type': 'Real', 'doc': ''},
                           'time_inc': {'pos': 8, 'type': 'Real', 'doc': ''}}},


        'sec_pill_circ': {'desc': 'Sector-shaped pillbox cavity (circular cross section)',
                          'doc': '',
                          'icool_model_name': 9,
                          'parms':
                                  {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                                   'freq': {'pos': 2,  'type': 'Real', 'doc': ''},
                                   'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                                   'phase': {'pos': 4, 'type': 'Real', 'doc': ''}}},

        'var_pill': {'desc': 'Variable {frequency gradient} pillbox cavity',
                     'doc': '',
                     'icool_model_name': 10,
                     'parms':
                            {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                             'phase': {'pos': 2,  'type': 'Real', 'doc': ''},
                             'num_wavelengths': {'pos': 3, 'type': 'Real', 'doc': ''},
                             'reset_parms': {'pos': 4, 'type': 'Real', 'doc': ''},
                             'buncher_len': {'pos': 5, 'type': 'Real', 'doc': ''},
                             'g0': {'pos': 6, 'type': 'Real', 'doc': ''},
                             'g1': {'pos': 7, 'type': 'Real', 'doc': ''},
                             'g2': {'pos': 8, 'type': 'Real', 'doc': ''},
                             'phase_model': {'pos': 9, 'type': 'Real', 'doc': ''}}},

        'straight_pill': {'desc': 'Straight pillbox or SuperFish cavity in dipole region',
                          'doc': '',
                          'icool_model_name': 11,
                          'parms':
                                  {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                                   'freq': {'pos': 2,  'type': 'Real', 'doc': ''},
                                   'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                                   'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                                   'radial_offset': {'pos': 5, 'type': 'Real', 'doc': ''},
                                   'axial_length': {'pos': 6, 'type': 'Real', 'doc': ''},
                                   'cavity_type': {'pos': 7, 'type': 'Real', 'doc': ''},
                                   'file_num': {'pos': 8, 'type': 'Real', 'doc': ''},
                                   'sf_field_norm': {'pos': 9, 'type': 'Real', 'doc': ''},
                                   'sf_rad_cut': {'pos': 10, 'type': 'Real', 'doc': ''},
                                   'sf_axial_disp': {'pos': 11, 'type': 'Real', 'doc': ''},
                                   'sf_axial_sym': {'pos': 12, 'type': 'Real', 'doc': ''}}},

        'sec_pill_rec': {'desc': 'Variable {frequency gradient} pillbox cavity',
                         'doc': '',
                         'icool_model_name': 12,
                         'parms':
                                 {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                                  'freq': {'pos': 2,  'type': 'Real', 'doc': ''},
                                  'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                                  'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                                  'rad_offset': {'pos': 5, 'type': 'Real', 'doc': ''},
                                  'width': {'pos': 6, 'type': 'Real', 'doc': ''},
                                  'height': {'pos': 7, 'type': 'Real', 'doc': ''}}},

        'open_cell_stand': {'desc': 'Open cell standing wave cavity',
                            'doc': '',
                            'icool_model_name': 13,
                            'parms':
                                   {'model': {'pos': 1, 'type': 'String', 'doc': ''},
                                    'freq': {'pos': 2,  'type': 'Real', 'doc': ''},
                                    'grad': {'pos': 3, 'type': 'Real', 'doc': ''},
                                    'phase': {'pos': 4, 'type': 'Real', 'doc': ''},
                                    'focus_flag': {'pos': 5, 'type': 'Real', 'doc': ''}}},

    }

    def __init__(self, **kwargs):
        Field.__init__(self, 'ACCEL', kwargs)
        #self.ftag = 'ACCEL'

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'ACCEL':
                object.__setattr__(self, name, value)
            else:
                print '\n Illegal attempt to set incorrect ftag.\n'  # Should raise exception here
        else:
            Field.__setattr__(self, name, value)

    def __str__(self):
        return Field.__str__(self)

    def gen_fparm(self):
        Field.gen_fparm(self)

    def gen(self, file):
        Field.gen(self)


class Sol(Field):
    """
    SOL solenoid field
    1 model level
    1: Bz with constant central region + linear ends
    2: dTANH(z) Bz dependence
    3: field from sum of circular current loops
    4: field from annular current sheet
    5: field from thick annular current block
    6: interpolate field from predefined USER r-z grid
    7: tapered radius
    8: hard-edge with adjustable end fields
    9: determine field from file of Fourier coefficients
    10: determine field from file of on-axis field

    For model = 1
    2 field strength [T]
    3 length of central region, CLEN[m] (You can use this to get a tapered field profile)
    4 length of entrance end region, ELEN1 [m] This is the displacement of the
    upstream end of the solenoid from the start of the region.
    5 constant offset for Bz [T]
    Use parameter 5 to get an indefinitely long, constant solenoidal field.
    6 length of exit end region, ELEN2 [m].
    For a symmetric field, set SLEN =CLEN + ELEN1 + ELEN2. Hard-edge field models
    can include the focusing effects of the missing fringe field by using EDGE commands
    before and after the hard-edge field region.

    For model = 2
    2 field strength [T]
    3 length of central region, CLEN[m]
    4 length for end region, ELEN [m] (This is the displacement of the
    upstream end of the solenoid from the start of the region; for a symmetric field, set SLEN =
    CLEN + 2*ELEN.)
    5 order of vector potential expansion {1, 3, 5, 7}
    6 end attenuation length, [m] (Set larger than maximum beam size)
    7 constant offset for Bs [T]

    For model = 3
    2 field strength [T]
    3 length of central region, CLEN[m] (This is the region over which the coils are
    distributed)
    4 length for end region, ELEN[m] (This is the displacement of the
    upstream end of the solenoid from the start of the region; for a symmetric field, set SLEN =
    CLEN + 2*ELEN.)
    5 # of coils loops (equi-spaced over CLEN)
    6 radius of coils [m]
    For a symmetric field with 1 loop, set ELEN=0.5 SLEN.

    For model = 4
    2 field strength [T]
    3 length of sheet [m]
    4 z offset of center of sheet from start of region [m]
    5 radius of sheet [m]

    For model = 5
    2 field strength [T]
    3 length of block [m]
    4 z offset of center of block from start of region [m]
    5 inner radius of block [m]
    6 outer radius of block[m]

    For model = 6
    2 grid ##of user-supplied field {1-4}
    3 interpolation level {1-3}
    1: bi-linear
    2: bi-quadratic polynomial
    3: bi-cubic polynomial
    The required format of the field map is
    title (A80)
    # of z grid points (I) {1-5000}
    # of r grid points (I) {1-100}
    i, j, zi, rj, BZi,j, BRi,j (I, R)

    2 Bc [T] (flat central field strength)
    3 Rc [m] (flat central coil radius)
    4 Lc [m] (central field length)
    5 B1 [T] (starting field strength)
    6 R1 [m] (starting coil radius)
    7 L1 [m] (length of entrance transition region)
    8 B2 [T] (ending field strength)
    9 R2 [m] (ending coil radius)
    10 L2 [m] (length of exit transition region)
    This model applies a geometry cut on particles whose radius exceeds the specified radial taper.

    """

    models = {
        'model_descriptor': {'desc': 'Name of model parameter descriptor',
                             'name': 'model'},
        '1': {'desc': 'Ez only with no transverse variation',
              'parms': {'freq': 2, 'grad': 3, 'phase': 4, 'rect_cyn': 5, 'mode': 8}},

        '2': {'desc': 'Cylindrical TM01p pillbox',
              'parms': {'freq': 2, 'grad': 3, 'phase': 4, 'rect_cyn': 5, 'longitudinal_mode': 8}},

        '3': {'desc': 'Traveling wave cavity',
              'parms': {'freq': 2, 'grad': 3, 'phase': 4, 'rect_cyn': 5, 'x_offset': 6, 'y_offset': 7,
                        'phase_velocity': 8}},

        '4': {'desc': 'Approximate fields for symmetric circular-nosed cavity',
              'parms': {'freq': 2, 'grad': 3, 'phase': 4, 'length': 8, 'gap': 9, 'drift_tube_radius': 10,
                        'nose_radius': 11}},

        '5': {'desc': 'User-supplied azimuthally-symmetric TM mode (SuperFish)',
              'parms': {'freq': 2, 'phase': 4, 'file_no': 8, 'field_strength_norm': 9, 'rad_cut': 10, 'axial_dist': 11,
                        'axial_sym': 12}},

        '6': {'desc': 'Induction linac model - waveform from user-supplied polynomial coefficients',
              'parms': {'time_offset': 2, 'gap': 3, 'time_reset': 4, 'V0': 5, 'V1': 6, 'V2': 7, 'V3': 8, 'V4': 9,
                        'V5': 10, 'V6': 11, 'V7': 12, 'V8': 13}},

        '7': {'desc': 'Induction linac model - waveform from internally generated waveform',
              'parms': {'num_gaps': 2, 'start_volt': 3, 'volt_swing': 4, 'time_offset': 5, 'kin_en': 6, 'pulse_dur': 7,
                        'slope': 8, 'bins': 9, 'gap_len': 10, 'file_num': 11, 'kill_flag': 12, 'restart_flag': 13}},

        '8': {'desc': 'Induction linac model - Waveform from user-supplied file',
              'parms': {'time_offset': 2, 'gap': 3, 'time_reset': 4, 'file_num_wav': 5, 'poly_order': 6,
                        'file_num_out': 7, 'time_inc': 8}},

        '9': {'desc': 'Sector-shaped pillbox cavity (circular cross section)',
              'parms': {'freq': 2, 'grad': 3, 'phase': 4}},

        '10': {'desc': 'Variable {frequency gradient} pillbox cavity',
               'parms': {'phase': 4, 'num_wavelengths': 5, 'reset_parm': 6, 'buncher_length': 7, 'g0': 8, 'g1': 9,
                         'g2': 10, 'phase_model': 12}}
        }
  
    def __init__(self, **kwargs):
        Field.__init__(self, 'Accel', kwargs)
        self.ftag = 'SOL'

    def __call__(self, **kwargs):
        Field.__call__(self, kwargs)

    def __setattr__(self, name, value):
        if name == 'ftag':
            if value == 'SOL':
                object.__setattr__(self, name, value)
            else:
                print '\n Illegal attempt to set incorrect ftag.\n'  # Should raise exception here
        else:
            Field.__setattr__(self, name, value)

    def gen_fparm(self):
        Field.gen_fparm(self)

    def gen(self, file):
        Field.gen(self)
 

class Comment(PseudoRegion):
    def __init__(self, comment):
        PseudoRegion.__init__(self, None, None)
        self.comment = comment
