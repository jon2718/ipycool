import py.test
from ipycool import *


def bmt_gen_test():
    title = Title(title='Test IPYCOOL')
    co = Cont(npart=10000)
    
    d = Distribution(bdistyp='gaussian', px_mean=0, px_std=0.000935, py_mean=0, py_std=0.000935,
                     pz_mean=0.0076, pz_std=0.0020, x_mean=0, x_std=0.00486, y_mean=0, y_std=0.00486,
                     z_mean=0, z_std=0.86)
    #d(y_std=4)
    c = Correlation(corrtyp='ang_mom', sol_field=1.29)
    bm = BeamType(nbcorr=1, fractbt=1, distribution=d, bmtype=2, partnum=1)
    bm.add_enclosed_command(c)
    bmt = Bmt(nbeamtyp=1)
    bmt.add_enclosed_command(bm)
    #bmt.add_enclosed_command(bm)
    interactions = Ints()

    output = Output()
    
    background_sol = Sol(model='bz', strength=0, elen2=0, elen1=0, clen=0, offset=0)
    s = Section()
    ac = Accel(model='sec_pill_rec', freq=1, grad=2, height=3, phase=4, rad_offset=5, width=6)
    so = Sol(model='edge', ent_def=0, ex_def=0, foc_flag=0, bs=20)
    so_minus = Sol(model='edge', ent_def=0, ex_def=0, foc_flag=0, bs=-20)
    cell = Cell(ncells=1, field=background_sol, flip=False)
   
    rep = Repeat(nrep=1)
    cell.add_enclosed_command(rep)
    rep.add_enclosed_command(output)
    sreg = SRegion(zstep=0.001, nrreg=1, slen=10)
  
    s.add_enclosed_command(cell)

    empty=NoField()
    mat = Material(geom='CBLOCK', mtag='VAC')
    subr = SubRegion(material=mat, rlow=0, rhigh=0.5, irreg=1, field=so)
    sreg.add_enclosed_command(subr)

    sreg_minus = SRegion(zstep=0.001, nrreg=1, slen=10)
    subr_minus = SubRegion(material=mat, rlow=0, rhigh=0.5, irreg=1, field=so_minus)
    sreg_minus.add_enclosed_command(subr_minus)

    rep.add_enclosed_command(sreg)
    rep.add_enclosed_command(sreg_minus)
    
    input = ICoolInput(cont=co, bmt=bmt, ints=interactions, title=title, section=s)
    file = './' + 'for001.dat'
    f = open(file, 'w')
    
    input.gen(f)
    f.close()

