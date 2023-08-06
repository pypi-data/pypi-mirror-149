import femagtools.machine as machine
import femagtools.bch as bch
import matplotlib.pylab as pl
import numpy as np
import io

psim=[0.11171972, 0.11171972]
i1=[80.0]
beta=[0.0, -41.1]
ld=[0.0014522728, 0.0014522728]
lq=[0.0032154, 0.0038278836]
r1=0.0806
m=3
p=4

filename = '/home/tar/Documents/ScientificPython/download/TEST_001.BCH-1'
bchresults = bch.Reader()
with io.open(filename, encoding='latin1', errors='ignore') as f:
    bchresults.read(f.readlines())

pm = machine.PmRelMachineLdq(m, p, psim, ld, lq, r1, beta, i1)
b = np.linspace(-90, 0)
pl.plot(b, pm.torque_iqd(*machine.iqd(b/180*np.pi, 80)), label='Vector')

pm = machine.PmRelMachineLdq(m, p, psim, ld, lq, r1, beta, i1)
pl.plot(b, pm.torque(b/180*np.pi, 80), label='Vector 2')

pm = machine.PmRelMachineLdq(m, p, psim[1], ld[1], lq[1], r1)
#pm = machine.PmRelMachineLdq(m, p, psim[0], ld[0], lq[0])
pl.plot(b, pm.torque_iqd(*machine.iqd(b/180*np.pi, 80)), label='Scalar')

pm = machine.PmRelMachineLdq(m, p, psim[1], ld[1], lq[1], r1)
#pm = machine.PmRelMachineLdq(m, p, psim[0], ld[0], lq[0])
pl.plot(b, pm.torque(b/180*np.pi, 80), label='Scalar 2')

i1 = bchresults.ldq['i1']
beta = bchresults.ldq['beta']
ld = bchresults.ldq['ld']
lq = bchresults.ldq['lq']
psim = bchresults.ldq['psim']

pm = machine.PmRelMachineLdq(m, p, psim, ld, lq, r1, beta, i1)
#pm = machine.PmRelMachineLdq(m, p, psim[0], ld[0], lq[0])

#iq, id = machine.iqd(b/180*np.pi, 80)
#pl.plot(iq, id)
#pl.show()

pl.plot(b, pm.torque_iqd(*machine.iqd(b/180*np.pi, 80)), label='Matrix')

pm = machine.PmRelMachineLdq(m, p, psim, ld, lq, r1, beta, i1)
#pm = machine.PmRelMachineLdq(m, p, psim[0], ld[0], lq[0])

#iq, id = machine.iqd(b/180*np.pi, 80)
#pl.plot(iq, id)
#pl.show()

#pl.plot(b, pm.torque(b/180*np.pi, 80), label='Matrix 2')
pl.legend(loc='upper left')
pl.grid()
pl.show()
