import py.test
from ipycool import *


def b_profile_gen():
    # Create Title
    title = Title(title='Test IPYCOOL')

    # Create Namelists
    co = Cont(npart=10000)
    d = Distribution(bdistyp='gaussian', px_mean=0, px_std=0.000935, py_mean=0, py_std=0.000935,
                     pz_mean=0.2, pz_std=0.0020, x_mean=0, x_std=0.00486, y_mean=0, y_std=0.00486,
                     z_mean=0, z_std=0.86)
    c = Correlation(corrtyp='ang_mom', sol_field=1.29)
    bm = BeamType(nbcorr=1, fractbt=1, distribution=d, bmtype=2, partnum=1)
    bm.add_enclosed_command(c)
    bmt = Bmt(nbeamtyp=1)
    bmt.add_enclosed_command(bm)
    interactions = Ints()

    # Create Section
    s = Section()
    rp = Refp(phmodref='const_v', bmtype=2, pz0=0.054, t0=0)
    s.add_enclosed_command(rp)
    so_minus = Sol(model='edge', ent_def=0, ex_def=0, foc_flag=0, bs=-40)
    mat_vac = Material(geom='CBLOCK', mtag='VAC')
    sreg_minus = SRegion(zstep=0.001, nrreg=1, slen=1)
    subr_minus = SubRegion(material=mat_vac, rlow=0, rhigh=0.5, irreg=1, field=so_minus)
    sreg_minus.add_enclosed_command(subr_minus)
    wrapped = Repeat.wrapped_sreg(outstep=0.01, sreg=sreg_minus)
    s.add_enclosed_command(wrapped)

    # Generate for001.dat
    input = ICoolInput(cont=co, bmt=bmt, ints=interactions, title=title, section=s)
    file = './' + 'for001.dat'
    f = open(file, 'w')
    input.gen(f)
    f.close()