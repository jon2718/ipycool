from ICoolObject import *


class Region(ICoolObject):

    def __init__(self, kwargs):
        ICoolObject.__init__(self, kwargs)

    def __call__(self, **kwargs):
        ICoolObject.__call__(self, kwargs)

    def __str__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __repr__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __setattr__(self, name, value):
        ICoolObject.__setattr__(self, name, value)

    def gen_for001(self, file):
        if hasattr(self, 'begtag'):
            print 'Writing begtag'
            file.write(self.get_begtag())
            file.write('\n')
        parm = self.gen_parm()
        splits = self.get_line_splits()
        count = 0
        split_num = 0
        cur_split = splits[split_num]
        for command in parm:
            if count == cur_split:
                file.write('\n')
                count = 0
                split_num = split_num + 1
                cur_split = splits[split_num]
            print 'Command is: ', command
            if hasattr(command, 'gen_for001'):
                command.gen_for001(file)
            else:
                file.write(self.for001_str_gen(command))
            file.write(' ')
            count = count + 1
        file.write('\n')


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

    def __init__(self, kwargs):
        Region.__init__(self, kwargs)

    def __str__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'

    def __repr__(self):
        return '[A PseudoRegion can be either a APERTURE, CUTV, DENP, DENS, DISP, DUMMY, DVAR, EDGE, GRID\
                OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TAPER, TILT, TRANSPORT, BACKGROUND, BFIELD, ENDB, ! or &]'


class RegularRegionContainer(RegularRegion, Container):

    def gen_for001(self, file):
        # self.gen_begtag(file)
        # if hasattr(self, 'begtag'):
        #    print 'Writing begtag'
        #    file.write(self.get_begtag())
        #    file.write('\n')
        Region.gen_for001(self, file)
        Container.gen_for001(self, file)
        # self.gen_endtag(file)
        if hasattr(self, 'endtag'):
            file.write(self.get_endtag())
            file.write('\n')


class SubRegion(RegularRegion):

    """
    A SubRegion is a:
    (1) IRREG r-region number;
    (2) RLOW Innter radius of this r subregion;
    (3) RHIGH Outer radius of this r subregion;
    (4) Field object; and
    (5) Material object.
    """
    num_params = 5
    for001_format = {'line_splits': [3, 1, 1]}

    command_params = {
        'irreg': {'desc': 'R-Region Number',
                  'doc': '',
                  'type': 'Integer',
                  'req': True,
                  'pos': 1},

        'rlow': {'desc': 'Inner radius of this r subregion',
                 'doc': '',
                 'type': 'Real',
                 'req': True,
                 'pos': 2},

        'rhigh': {'desc': 'Outer radius of this r subregion',
                  'doc': '',
                  'type': 'Real',
                  'req': True,
                  'pos': 3},

        'field': {'desc': 'Field object',
                  'doc': '',
                  'type': 'Field',
                  'req': True,
                  'pos': 4},

        'material': {'desc': 'Material object',
                     'doc': '',
                     'type': 'Material',
                     'req': True,
                     'pos': 5}
    }

    def __init__(self, **kwargs):
        RegularRegion.__init__(self, kwargs)

    def __str__(self):
        return 'SubRegion:\n' + 'irreg=' + str(self.irreg) + '\n' + 'rlow=' + str(self.rlow) + '\n' + \
            'rhigh=' + str(self.rhigh) + '\n' + 'Field=' + \
            str(self.field) + '\n' + \
            'Material=' + str(self.material)

    def __repr__(self):
        return 'SubRegion:\n' + 'irreg=' + str(self.irreg) + '\n' + 'rlow=' + str(self.rlow) + '\n' + \
            'rhigh=' + str(self.rhigh) + '\n' + 'Field=' + \
            str(self.field) + '\n' + \
            'Material=' + str(self.material)

    def __setattr__(self, name, value):
        Region.__setattr__(self, name, value)