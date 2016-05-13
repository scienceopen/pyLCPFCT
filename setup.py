#!/usr/bin/env python3
import subprocess
import setuptools #needed to enable develop

try:
    subprocess.run(['conda','install','--yes','--file','requirements.txt'])
except Exception as e:
    print('you will need to install packages in requirements.txt')
#%%
with open('README.rst','r') as f:
	long_description = f.read()
#%%
from numpy.distutils.core import setup,Extension

ext=[Extension(name='lcpfct',
               sources=['lcpfct.f','gasdyn.f'],
               f2py_options=['--quiet'],
               extra_f77_compile_args=['-Wno-unused-label']
               ),
Extension(name='shock',
               sources=['shock.f','gasdyn.f','lcpfct.f'],
               f2py_options=['--quiet'],
               extra_f77_compile_args=['-Wno-unused-label']
               )
    ]

               #include_dirs=[root],
               #library_dirs=[root])]

#%% install
setup(name='pylcpfct',
      version='0.1',
	 description='Python wrapper for LCPFCT model',
	 long_description=long_description,
	 author='Michael Hirsch',
	 url='https://github.com/scienceopen/pylcpfct',
      packages=['pylcpfct'],
      ext_modules=ext,
	  install_requires=[],
      )
