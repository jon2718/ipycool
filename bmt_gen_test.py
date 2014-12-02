import py.test
from ipycool import *


def bmt_gen_test():
    co=Cont(npart=10000)
    d = Distribution(bdistyp='gaussian', px_mean=0.1, px_std=8, py_mean=0.23, py_std=2.45,
                     pz_mean=0.12356, pz_std=0.34, x_mean=0, x_std=7.34, y_mean=0.34, y_std=3.55,
                     z_mean=0.111, z_std=0.4)
    c = Correlation(corrtyp='palmer', beta_eff=1, strength=1)
    bm = BeamType(nbcorr=1, fractbt=1, distribution=d, bmtype=2, partnum=1)
    bm.add_enclosed_command(c)
    bmt = Bmt(nbeamtyp=1)
    file = './' + 'for001.dat'
    f = open(file, 'w')
    bmt.add_enclosed_command(bm)
    bmt.add_enclosed_command(bm)

    co.icoolgenerate_for001(f)
    bmt.icoolgenerate_for001(f)

    ac=Accel(model='sec_pill_rec', freq=1, grad=2, height=3, phase=4, rad_offset=5, width=6)

    s=Section(nsections=1)
    

    ac=Accel(model='sec_pill_rec', freq=1, grad=2, height=3, phase=4, rad_offset=5, width=6)
    cell=Cell(ncells=10, field=ac, flip=False)

    rep=Repeat(nrep=10)
    cell.add_enclosed_command(rep)

    sreg=SRegion(zstep=0.001, nrreg=1, slen=14)
    
    s.add_enclosed_command(cell)

    mat=Material(geom='cblock', mtag='lh')
    subr=SubRegion(material=mat, rlow=0, rhigh=1, irreg=1, field=ac)
    sreg.add_enclosed_command(subr)

    #rep.add_enclosed_command(sreg)
    
    #s.icoolgenerate_for001(f)
    
    s.gen_for001(f)

    f.close()

