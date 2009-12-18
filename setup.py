# -*- coding: iso-8859-15 -*-

import sys, os
from setuptools import setup, find_packages
from openalea.deploy.binary_deps import binary_deps
from os.path import join as pj

from openalea.deploy.metainfo import read_metainfo
metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in zip(metadata.keys(), metadata.values()):
    exec("%s = '%s'" % (key, value))

# Scons build directory
build_prefix= "build-scons"

# platform dependencies
install_requires = [binary_deps('vplants.plantgl'),]

if sys.platform.startswith('win'):
    install_requires += [binary_deps("boostpython"),]

setup_requires = install_requires + ['openalea.deploy']

pkg_name= namespace + '.' + package
wralea_name= namespace + '.' + package + '_wralea'


# Main setup
setup(
    # Meta data
    name=name,
    version=version,
    description=description,
    long_description=long_description,
    author=authors,
    author_email=authors_email,
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
                pkg_name+'.engine', 
                pkg_name+'.fractutils',
                wralea_name, 
                wralea_name+'.light', 
                wralea_name+'.light.castshadow', 
                wralea_name+'.engine', 
                wralea_name+'.engine.boxcounting', 
                wralea_name+'.engine.two_surfaces', 

 ],

    # python packages directory
    package_dir= {  pkg_name : pj('src',name),
                    pkg_name+'.light' :pj('src', name, 'light'),
                    pkg_name+'.light.castshadow' :pj('src', name, 'light', 'castshadow'),
                    pkg_name+'.engine' :pj('src', name, 'engine'),
                    pkg_name+'.engine.boxcounting' :pj('src', name, 'engine', 'boxcounting'),
                    pkg_name+'.engine.two_surfaces' :pj('src', name, 'engine', 'two_surfaces'),
                    pkg_name+'.fractutils' :pj('src', name, 'fractutils'),
                    wralea_name : pj('src',name+'_wralea'),
                    '' : 'src',
                  },

    # add package platform libraries if any
    package_data= { '' : ['*.so', '*.dll', '*.pyd', '*.png', '*.dylib']},
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
            "fractalysis = openalea.fractalysis_wralea",
            "castshadow = openalea.fractalysis_wralea.light.castshadow",
            "two_surfaces = openalea.fractalysis_wralea.engine.two_surfaces",
            "boxcounting = openalea.fractalysis_wralea.engine.boxcounting",
            ]
                    },
   pylint_packages = ['src/fractalysis/engine','sec/fractalysis/light','src/fractalysis/fracutils']
  )


