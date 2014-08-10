import sys
class ICoolGen(object):
    """Generate ICOOL for001.dat
    Takes an ICoolInput object and generates an ICOOL for001.dat file.
    """
    def __init__(self, icool_input, path='.'):
        self.file=path+'/'+'for001.dat'
        self.icool_input=icool_input
      
    def gen(self):
        f=open(self.file, 'w')
        self.icool_input.gen(f)
        f.close()

    def cr(f):
        f.write('\n')

    def sp(f):
        f.write(" ")

    def list_line(f, list):
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
    def __init__(self, title=None, cont=None, bmt=None, ints=None, nhs=None, nsc=None, nzh=None, nrh=None, nem=None, ncv=None, sec=None, name=None, metadata=None):
        check_input_args(title, cont, bmt, ints, nhs, nsc, nzh, nrh, nem, ncv, sec, name, metadata)
        self.title=title
        self.cont=cont
        self.bmt=bmt
        self.ints=ints
        self.nhs=nhs
        self.nsc=nsc
        self.nzh=nzh
        self.nrh=nrh
        self.nem=nem
        self.ncv=ncv
        self.sec=sec
        self.name=name
        self.metadata=metadata
        #What is the minimum required set of commands?
    
    def add_title(title):
        self.title=title
    
    def add_cont(cont):
        self.cont=cont
    
    def add_sec(sec):
        self.sec=sec
        
    def gen(self, file):
        if self.title!=None:
            self.title.gen(file)
        if self.cont!=None:   
            self.cont.gen(file)
        if self.bmt!=None:
            self.bmt.gen(file)
        if self.ints!=None:   
            self.ints.gen(file)
        if self.nhs!=None: 
            self.nhs.gen(file)
        if self.nsc!=None:
            self.nsc.gen(file)
        if self.nzh!=None:   
            self.nzh.gen(file)
        if self.nrh!=None: 
            self.nrh.gen(file)
        if self.nem!=None:
            self.nem.gen(file)
        if self.ncv!=None:   
            self.ncv.gen(file)
        if self.sec!=None: 
            self.sec.gen(file)
        


class Title(object):
    def __init__(self, title):
        self.title=title
    def __str__(self):
        return '[Problem Title: %]' %self.title
    def __repr__(self):
        return '[Problem Title: %]' %self.title

    def gen(self, file):
        file.write(self.title)

class Cont(object):
    betaperp={'default': None,  'desc': '(R) beta value to use in calculating amplitude variable A^2', 'type':'Real'}
    bgen={'default': True,  'desc': '(L) if .true. => generate initial beam particles, otherwise read input from FOR003.DAT (true)', 'type': 'Logical'}
    
    def __init__(self, **kwargs):
        for command, value in kwargs.items():
            if valid_command(cont_dict, command, value, 'CONT')==-1:
                print 'Valid commands are:\n'
                for key in cont_dict:
                    print key,',', 
                print
                sys.exit(0)
                #raise ValueError
        self.cont_commands=kwargs
                      

    def __str__(self):
         return '[Control variables: ]'

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
            

class Region(object):
    def __init__(self, name=None, metadata=None):
        self.name = name
        self.metadata=metadata
        
    def __str__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

    def __repr__(self):
        return '[A Region can be either a RegularRegion or PseudoRegion.]'

class RegularRegion(Region):
    """
    RegularRegion commands include: SECTION, BEGS, REPEAT, CELL, SREGION, ENDREPEAT, ENDCELL,
    and ENDCELL.
    """
    def __init__(self, name=None, metadata=None):
        Region.__init__(self, name, metadata)

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


class Section(RegularRegion):
    """
    SECTION Start of cooling section region definition.
    The data must end with an ENDSECTION.   It can enclose any number of other commands. 
    If it is desired to repeat the section definitions, the control variable NSECTIONS should be
    set >1 and a BEGS command is used to define where to start repeating.
    """
    def __init__(self, nsections=1, command_list=None, name=None, metadata=None):
        RegularRegion.__init__(self, name, metadata)
        self.nsections=nsections
        self.allowed={'Cell': {}, 'Background': {}, 'SRegion':{}, 'Aperture': {}, 'Dens': {}, 'Disp': {}, 'Dummy': {}, 'DVar':{}, 'Edge': {}, 'Output': {}, 'Refp': {}, 'Ref2':{}, 'Reset':{}, 
        'RKick': {}, 'Rotate': {}, 'Tilt': {}, 'Transport': {}, 'Repeat': {}}
        if command_list!=None:
            self.command_list=command_list
        else:
            self.command_list=[]
        #if self.command_list!=None: 
        #    for command in command_list:
         #       pass

    def add_command(self, command):
        try:
            if self.check_command(command)==True:
                self.command_list.append(command)
            else:
                raise IncorrectObjectCommand('Incorrect Object Command.', 'Section', command.__class__.__name__)
        except IncorrectObjectCommand as e:
            print e
            sys.exit(0)

    def check_command(self, command):
        if command.__class__.__name__ in self.allowed.keys():
            return True
        else:
            return False

    def gen(self, file):
        file.write('\n')
        file.write('SECTION')
        for command in self.commands:
            command.gen(f)
        file.write('\n')
        file.write('ENDSECTION')

class Begs(RegularRegion):
    def __init__(self):
        RegularRegion.__init(self, None, None)

    def gen(self, file):
        region.gen('BEGS')

class Repeat(RegularRegion):
    """
    Start of a repeating group of region commands; the data must end with an ENDREPEAT
    command. This can be used to repeat regions inside a cell. The repeat loop can enclose any
    number of {SREGION, APERTURE, DENS, DISP, DUMMY, DVAR, EDGE, OUTPUT, REFP, REF2, RESET, RKICK, ROTATE, TILT, TRANSPORT} commands. 
    Repeat sections cannot be nested in other repeat sections. (see parameters below)
    """
    def __init__(self, num_repeats, region_command_list):
        RegularRegion.__init__(self, None, None)
        self.region_commands=region_commands
        self.num_repeats=num_repeats
        self.allowed={'SRegion': {}, 'Aperture': {}, 'Dens': {}, 'Disp': {}, 'Dummy': {}, 'Dvar': {}, 'Edge': {}, 'Output': {}, 'Refp': {},
         'Ref2': {}, 'Reset': {}, 'Rkick': {}, 'Rotate': {}, 'Tilt': {}, 'Transport': {}}
       
    def add_region_command(command):
        print

    def add_region_command_at(command, insert_point):
        print

    def remove_region_command_at(delete_point):
        print

    def gen(self, file):
        region.gen('REPEAT')

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
        self.edge_type=edge_type
        self.model=model
        self.model_parameters=model_parameters

class Cell(RegularRegion):
    """CELL Start of a repeating group of region commands; the data must end with an ENDCELL command.
    The cell loop can enclose any number of commands under REPEAT plus REPEAT and ENDREPEAT commands.
    It has an associated cell field, which is superimposed on the individual region fields. Cell sections cannot
    be nested in other cell sections. (see parameters below)
    """
    def __init__(self, name, metadata, ncells, cellflip, field):
        RegularRegion.__init__(self, None, None)
        self.region_commands=[]
        self.ncells=ncells
        self.cellflip=cellflip
        self.cftag=field.ftag
        self.cfparm=field.fparm
        self.allowed={'SRegion':{}, 'Aperture': {}, 'Dens': {}, 'Disp': {}, 'Dummy': {}, 'DVar':{}, 'Edge': {}, 'Output': {}, 'Refp': {}, 'Ref2':{}, 'Reset':{}, 
        'RKick': {}, 'Rotate': {}, 'Tilt': {}, 'Transport': {}, 'Repeat': {}}

    def add_region_command(command):
        print

    def add_region_command_at(command, insert_point):
        print

    def remove_region_command_at(delete_point):
        print


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
    def __init__(self, slen, nrreg, zstep, r_subregion_list=None, name=None):
        self.slen=slen
        self.nrreg=nrreg
        self.zstep=zstep
        self.subregions=[]
        RegularRegion.__init__(self, name)

    def __str__(self):
        return 'SRegion:\n '+'slen='+str(self.slen)+','+'nrreg='+str(self.nrreg)+','+'zstep='+str(self.zstep)
        
    def add_subregion(irreg, rlow, rhigh, field, material):
        subr=[]
        subr.append(irreg)
        subr.append(rlow)
        subr.append(rhigh)
        subr.append(field)
        subr.append(material)
        self.subregions.append(subr)

    def gen(self, file):
        file.write('\n')
        f.write('SREGION')
        file.write('\n')
        file.write(slen)
        file.write(' ')
        file.write(nrreg)
        file.write(' ')
        file.write(zstep)
        file.write('\n')
        for rsubr in subregions:
            pass


class Field:
    """
    A Field is a:
    FTAG - A tag identifying the field.  Valid FTAGS are:
    ACCEL, BLOCK, BROD, BSOL, COIL, DIP, EFLD, FOFO, HDIP, HELI(X), HORN, KICK, QUAD,
    ROD, SEX, SHEE(T), SOL, SQUA, STUS, WIG

    FPARM - 15 parameters describing the field.
    """
    def __init__(self, ftag, fparm):
        self.ftag = ftag
        self.fparm=fparm

    def gen(self, file):
        file.write('\n')
        file.write(ftag)
        file.write('\n')
        for s in fparm:
            file.write(s)
            file.write(" ")

class Material:
    """
    A Material is a:
    MTAG (A) material composition tag
    MGEOM (A) material geometry tag
    GPARM (R) 10 parameters that describe the geometry of the material

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
    def __init__(self, mtag, mgeom, gparm):
        self.mtag = mtag
        self.mgeom=mgeom
        self.mparm=gparm

    def gen(self, file):
        file.write('\n')
        file.write(mtag)
        file.write('\n')
        file.write(mgeom)
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
    def __init__(self, model, field_parameters):
        self.model=model
        field.__init__(self, 'ACCEL', model, field_parameters)

    def gen(self, file):
        print


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
    def __init__(self, model, field_parameters):
        self.model=model
        field.__init__(self, 'SOL', model, field_parameters)

    def gen(self, file):
        print

class Sheet(Field):
    def __init__(self, model, field_parameters):
        self.model=model
        field.__init__(self, 'SHEET', field_parameters)

    def gen(self, file):
        print
        
class Comment(PseudoRegion):
    def __init__(self, comment):
        PseudoRegion.__init__(self, None, None)
        self.comment = comment

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
        string=self.msg+' '+self.expr
        return repr(string)

class IncorrectType(InputError):
    """Exception raised for incorrect type in the input."""
    def __init__(self, expr, expected_type, actual_type):
        InputError.__init__(self, expr, 'Incorrect type.')
        self.expected_type=expected_type
        self.actual_type=actual_type
        
    def __str__(self):
        msg="Incorrect type.  Expected "+self.expected_type+" but instead got "+self.actual_type
        return repr(msg)

class UnknownCommand(InputError):   
      """Exception raised for unknown type in the input."""
      def __init__(self, expr, command, namelist):
          InputError.__init__(self, expr, 'Unknown command.')
          self.command=command
          self.namelist=namelist
          
      def __str__(self):
          msg='Unknown command: '+self.command+' in namelist: '+self.namelist
          return repr(msg)
          
class IncorrectNamelistObject(InputError):   
      """Exception raised for unknown type in the input."""
      def __init__(self, expr, namelist, type):
          InputError.__init__(self, expr, 'Incorrect Namelist object.')
          self.namelist=namelist
          self.type=type
          
      def __str__(self):
          msg='Incorrect Namelist object. Expected type: '+self.type+' but got:' +str(type(self.namelist))
          return repr(msg)

class IncorrectObjectCommand(InputError):
    """Exception raised for attempt to add incorrect command to an object."""
    def __init__(self, expr, object, command):
        self.object=object
        self.command=command
        
    def __str__(self):
        msg='Command: '+self.command+' is not supported in object: '+self.object
        return repr(msg)
    
class FieldError(InputError):
    pass


cont_dict =\
            {
                'betaperp'      : {'default': None,  'desc': '(R) beta value to use in calculating amplitude variable A^2', 'type':'Real'},
                
                'bgen'          : {'default': True,  'desc': '(L) if .true. => generate initial beam particles, otherwise read input from FOR003.DAT (true)', 
                                'type': 'Logical'},
                
                'bunchcut'      : {1E6,   '(R) maximum time difference allowed between a particle and the reference particle [s]', 'Real'},
                'bzfldprd'      : {None,  '(R) Bz for solenoid at location of production plane (0.) This is used for output to file\
                                               for009.dat and for canonical angular momentum correction.', 'Real'},
                'dectrk'        : {False, '(L) if .true. => continue tracking daughter particle following decay', 'Logical'},
                'diagref'       : {False, '(L) if .true. => continue tracking daughter particle following decay'},
                'epsf'          : {0.05,  '(R) desired tolerance on fractional field variation, energy loss, and\
                                               multiple scattering per step', 'Real'},
                'epsreq'        : {None,  '(R) required tolerance on error in tracking parameters (1E-3) This parameter is only\
                                               used if varstep = true', 'Real' },
                'epsstep'       : {1E-6,  '(R) desired tolerance in spatial stepping to reach each destination plane [m]', 'Real'},
                'ffcr'          : {False, '(L) if .true. => inserts form feed and carriage returns in the output log file\
                                               so there are two plots per page starting at the top of a page', 'Logical'},
                'forcerp'       : {True,  '(L) if .true. => set x, y, Px, and Py for reference particle to 0 for each\
                                               new REFP command and for each ACCEL region with phasemodel=4.', 'Logical'},
                'fsav'          : {None,  '(L) if .true. => store particle info at plane IZFILE into file\
                                              FOR004.DAT. (false).  It is possible to get the initial distribution\
                                              of particles that get a given error flag be setting the plane=IFAIL #. It is\
                                              possible to get the initial distribution of particles that successfully make it to the\
                                              end of the simulation by setting the plane= -1.', 'Logical'},                                             
                'fsavset'       : {False, '(L) if .true. => modify data stored using FSAV in FOR004.DAT to have z=0 and times relative\
                                            to reference particle at plane IZFILE.', 'Logical' },
                'f9dp'          : {None, '(I) number of digits after the decimal point for floating point variables in FOR009.DAT {4,6,8,10,12,14,16,17}\
                                          (4) F9DP=17 gives 16 digits after the decimal point and 3 digits in the exponent', 'Integer'},
                'goodtrack'     : {True, '(L) if .true. and BGEN=.false. => only accepts input data from file FOR003.DAT if IPFLG=0.;\
                                          if .false. => resets IPFLG of bad input tracks to 0 (this allows processing a file of bad tracks for diagnostic purposes)', 'Logical'},
                'izfile'        : {None, '(I) z-plane where particle info is desired when using FSAV. Use 1 to\
                                          store beam at production. Saves initial particle properties for bad tracks if IZFILE=IFAIL #.\
                                          Saves initial particle properties for tracks that get to the end of the simulation if IZFILE=-1.\
                                          IZFILE should point to the end of a REGION or to an APERTURE , ROTATE or TRANSPORT pseudoregion command.', 'Integer'},
                'magconf'       : {0,    '(I) if 19 < MAGCONF=mn < 100 => reads in file FOR0mn.DAT, which contains data on solenoidal magnets. Used with SHEET,\
                                          model 4.', 'Integer'},
                'mapdef'        : {0,     '(I) if 19 < MAPDEF=mn < 100 => reads in file FOR0mn.DAT, which contains data on how to set up field grid. Used with \
                                           SHEET, model 4.', 'Integer'},
                'neighbor'      : {False, "(L) if .true. => include fields from previous and following regions when calculating field.  This parameter can be used\
                                           with soft-edge fields when the magnitude of the field doesn't fall to 0 at the region boundary. A maximum of 100 regions\
                                           can be used with this feature.", 'Logical'},
                'neutrino'      : {0,      '(I) if 19 < NEUTRINO=mn < 100 => writes out file FOR0mn.DAT, which contains neutrino production data. See\
                                            section 5.2 for the format.', 'Integer'},
                'nnudk'         : {1,      '(I) # of neutrinos to produce at each muon, pion and kaon decay.', 'Integer'},
                'npart'         : {'default': None,   'desc': "(I) # of particles in simulation. The first 300,000 particles are stored in memory. Larger numbers\
                                    are allowed in principle since ICOOL writes the excess particle information to disc. However, there\
                                            can be a large space and speed penalty in doing so.", 'type': 'Integer'},
                'nprnt'         : {},
                'npskip'        : {},
                'nsections'     : {},
                'ntuple'        : {},
                'nthmin'        : {},
                'nuthmax'       : {},
                'output1'       : {},
                'phantom'       : {},
                'phasemodel'    : {},
                'prlevel'       : {},
                'prnmax'        : {},
                'pzmintrk'      : {},
                'rfdiag'        : {},
                'rfphase'       : {},
                'rnseed'        : {},
                'rtuple'        : {},
                'rtuplen'       : {},
                'run_env'       : {},
                'scalestep'     : {},
                'spin'          : {},
                'spinmatter'    : {},
                'spintrk'       : {},
                'stepmax'       : {},
                'stepmin'       : {},
                'steprk'        : {}, 
                'summary'       : {},
                'termout'       : {},
                'timelim'       : {},
                'varstep'       : {}
                }
                
               

def valid_command(command_dict, command, value, namelist):
    try:
        if command in command_dict.keys():
            dictionary_entry=command_dict[command]
            command_type=dictionary_entry['type']
            try:
                if check_type(command_type, value.__class__.__name__):
                    return 0
                else:
                    raise IncorrectType('Incorrect type', command_type, value.__class__.__name__)
            except IncorrectType as e:
                 print e
                 return -1   
        else:
            raise UnknownCommand('Unknown command', command, namelist)
    except UnknownCommand as e:
        print e
        return -1
        
def check_input_args(title, cont, bmt, ints, nhs, nsc, nzh, nrh, nem, ncv, sec, name, metadata):
    try:
        cl=str(cont.__class__)
        dot=cl.find('.')
        if cl[dot+1:dot+5]=='Cont':
            return 0
        else:
            raise IncorrectNamelistObject('Incorrect Namelist Object', cont, 'Cont')
    except IncorrectNamelistObject as e:
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
    