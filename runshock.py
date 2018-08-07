#!/usr/bin/env python3
"""
Demonstration of NRL LCPFCT code in Python
Michael Hirsch

Old-fashioned way:
gfortran runshock.f shock.f lcpfct.f gasdyn.f -o shock
./shock  #writes fort.11 file
python runshock.py

New way-- 50+ times faster!:
f2py3 -m shock -h shock.pyf shock.f lcpfct.f gasdyn.f
f2py3 -c shock.pyf shock.f gasdyn.f lcpfct.f
python runshock.py

"""
from pandas import Panel
from matplotlib.pyplot import draw, pause, subplots, show
from time import time
import shock  # fortran code needs f2py3 first as noted in comments

nx = 50


def runshock():

    darr = shock.shock(nx)
    dr = darr[:, :5].reshape((-1, nx, 5), order='C')

    dpan = Panel(dr, major_axis=darr[:nx, 5],
                 minor_axis=('Density', 'Temperature', 'Pressure',
                             'Velocity', 'Energy'))  # FIXME read dt from Fortran

    return dpan

# def readshock(fn):
#    fn = expanduser(fn)
#
# %% get first header
#    with open(fn,'r') as f:
#        hd = f.readline().split() #column names for Panel
#        hd2 = f.readline().split()
#    if hd2[0] != '1':
#        print('** warning, I appear to not be reading the header correctly')
#
#    nx = int(hd2[-4])
#    dt = float(hd2[-1])
#
# %% read data frames
#    d = []; lines=''
#    with open(fn,'r') as f:
#        while True:
#            lines=''
#            #get to next record
#            line = f.readline()
#            if not line:
#                break
#            if line[0] != '1':
#                continue
#            #read the record
#            for i in range(nx):
#                lines += f.readline()
#            d.append(loadtxt(StringIO(lines), usecols=(1,2,3,4,5,6)))
# %% setup output
#    nt = len(d)
#    t = arange(0,nt*dt,dt)
#
#    dat = asarray(d)
#    return Panel(dat[...,:5], t, dat[0,:,5], hd[1:-1])


def plotshock(dat):
    fg, ax = subplots(5, 1, num=1, sharex=True)
    fg.subplots_adjust(hspace=0.05)
    fg.suptitle('1-D shock')
    ax[-1].set_xlabel('x displacement')

    for i, j in enumerate(dat.minor_axis.values):
        ax[i].set_ylabel(j)

    for t, da in dat.items():
        # ht.set_text('1-D shock: t={:.3f} sec.'.format(t)) #FIXME get more variables from Fortran
        for i, (j, d) in enumerate(da.iteritems()):
            ax[i].plot(d, label=j)
        draw()
        pause(0.5)


def main():
    tic = time()
    fdata = runshock()
    forttime = time()-tic
    print(f'fortran took {forttime:0.3e} seconds')

    plotshock(fdata)
    show()


if __name__ == '__main__':
    main()
