# -*- coding: iso-8859-15 -*-

import sys, os
from setuptools import setup, find_packages
from os.path import join as pj

# Package name
name= 'fractalysis'
namespace="openalea"

pkg_name= namespace + '.' + name

version= '0.0.2'

# Description of the package
name= 'fractalysis'

description= '3D Fractal analysis package.' 

long_description= '''
It contains code in C++, Python, as well as Boost.Python wrappers.
The package can be installed on various platform.
'''

author= 'Da SILVA David'
author_email= 'david.da_silva@cirad.fr'
url= 'http://openalea.gforge.inria.fr'

# License: License for the template package.
# Please, choose an OpenSource license for distribution of your package.
license= 'Cecill-C' # or 'GPL' or 'Cecill' or  'LGPL'

# Scons build directory
build_prefix= "build-scons"

# platform dependencies
install_requires = ['plantgl',]

if("win" in sys.platform):
    install_requires += ["boostpython",]

setup_requires = install_requires + ['openalea.deploy']


# Main setup
setup(
    # Meta data
    name='VPlants.Fractalysis',
    version=version,
    description=description,
    long_description=long_description,
    author=author,
    author_email=author_email,
    url=url,
    license=license,
    
    # Define what to execute with scons
    # scons is responsible to put compiled library in the write place
    # ( lib/, package/, etc...)
    scons_scripts = ['SConstruct'],

    # scons parameters  
    scons_parameters = ["build","build_prefix="+build_prefix],

    # Packages
    namespace_packages = [namespace],
    create_namespaces = True,

    # pure python  packages
    packages= [ pkg_name, 
                pkg_name+'.light', 
                pkg_name+'.light.castshadow', 
                pkg_name+'.engine', 
                pkg_name+'.engine.boxcounting', 
                pkg_name+'.engine.two_surfaces', 
                pkg_name+'.fractutils' ],

    # python packages directory
    package_dir= {  pkg_name : pj('src',name),
                    pkg_name+'.light' :pj('src', name, 'light'),
                    pkg_name+'.light.castshadow' :pj('src', name, 'light', 'castshadow'),
                    pkg_name+'.engine' :pj('src', name, 'engine'),
                    pkg_name+'.engine.boxcounting' :pj('src', name, 'engine', 'boxcounting'),
                    pkg_name+'.engine.two_surfaces' :pj('src', name, 'engine', 'two_surfaces'),
                    pkg_name+'.fractutils' :pj('src', name, 'fractutils'),
                    '' : 'src',
                  },

    # add package platform libraries if any
    package_data= { '' : ['*.so', '*.dll', '*.pyd', '*.png']},
    include_package_data=True,
    zip_safe = False,
                     

    # Specific options of openalea.deploy
    lib_dirs = {'lib' : pj(build_prefix, 'lib'),},
    inc_dirs = { 'include' : pj(build_prefix, 'include') },
    share_dirs = { 'doc': 'doc',},
          

    # Dependencies
    setup_requires = setup_requires ,
    install_requires = install_requires,
    dependency_links = ['http://openalea.gforge.inria.fr/pi'],

    # entry_points
    entry_points = {"wralea": [
            "fractalysis = openalea.fractalysis",
            "castshadow = openalea.fractalysis.light.castshadow",
            "two_surfaces = openalea.fractalysis.engine.two_surfaces",
            "boxcounting = openalea.fractalysis.engine.boxcounting",
            ]
                    },

  )


