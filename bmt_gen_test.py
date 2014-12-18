import py.test
from ipycool import *


def bmt_gen_test():
    title=Title(title='Test IPYCOOL')
    co = Cont(npart=10000)
    
    d = Distribution(bdistyp='gaussian', px_mean=0, px_std=0.000935, py_mean=0, py_std=0.000935,
                     pz_mean=0.0076, pz_std=0.0020, x_mean=0, x_std=0.00486, y_mean=0.34, y_std=0.00486,
                     z_mean=0, z_std=0.86)
    #d(y_std=4)
    c = Correlation(corrtyp='palmer', beta_eff=1, strength=1)
    bm = BeamType(nbcorr=1, fractbt=1, distribution=d, bmtype=2, partnum=1)
    bm.add_enclosed_command(c)
    bmt = Bmt(nbeamtyp=1)
    bmt.add_enclosed_command(bm)
    #bmt.add_enclosed_command(bm)
    interactions=Ints(lstrag = True)

    #output=Output()
    
    background_sol=Sol(model='bz', strength=0, elen2=4, elen1=4, clen=8, offset=4)
    s = Section()
    ac = Accel(model='sec_pill_rec', freq=1, grad=2, height=3, phase=4, rad_offset=5, width=6)
    so=Sol(model='edge', ent_def =1 , ex_def=2, foc_flag=1, bs=40)
    cell = Cell(ncells=10, field=background_sol, flip=False)
   
    rep = Repeat(nrep=1)
    cell.add_enclosed_command(rep)

    sreg = SRegion(zstep=0.001, nrreg=1, slen=0.001)
  
    s.add_enclosed_command(cell)

    mat = Material(geom='CBLOCK', mtag='VAC')
    subr = SubRegion(material=mat, rlow=0, rhigh=10, irreg=1, field=so)
    sreg.add_enclosed_command(subr)

    rep.add_enclosed_command(sreg)
    
    input = ICoolInput(cont=co, bmt=bmt, ints=interactions, title=title, section=s)
    file = './' + 'for001.dat'
    f = open(file, 'w')
    
    input.gen(f)
    f.close()

