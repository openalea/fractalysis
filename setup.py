# -*- coding: iso-8859-15 -*-

import sys
import os
pj = os.path.join

from setuptools import setup, find_packages

from openalea.deploy.metainfo import read_metainfo

metadata = read_metainfo('metainfo.ini', verbose=True)
for key,value in metadata.iteritems():
    exec("%s = '%s'" % (key, value))

namespace = 'openalea'
packages=find_packages('src')
package_dir={'': 'src'}

wralea_name = 'openalea.fractalysis_wralea'

setup_requires = ['openalea.deploy']
install_requires = []
# web sites where to find eggs
dependency_links = ['http://openalea.gforge.inria.fr/pi']

build_prefix = "build-scons"

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
    packages= packages,
    package_dir= package_dir,

    # Namespace packages creation by deploy
    namespace_packages=[namespace],
    create_namespaces=True,

    zip_safe=False,

    # Dependencies
    setup_requires=setup_requires,
    install_requires=install_requires,
    dependency_links=dependency_links,

    # add package platform libraries if any
    package_data= {'': ['*.so', '*.dll', '*.pyd', '*.png', '*.dylib', '*.geom', '*.bgeom', '*.drf', '*.mtg' ]},
    include_package_data=True,

    # Specific options of openalea.deploy
    lib_dirs={'lib': pj(build_prefix, 'lib')},
    inc_dirs={'include': pj(build_prefix, 'include')},
    share_dirs={'doc': 'doc',},

    # entry_points
    entry_points={"wralea": [
                  "fractalysis = " + wralea_name,
                  "castshadow = " + wralea_name + ".light.castshadow",
                  "two_surfaces = " + wralea_name + ".engine.two_surfaces",
                  "boxcounting = " + wralea_name + ".engine.boxcounting",
                  ]
                  },
    pylint_packages=['src/openalea/fractalysis/engine',
                     'src/openalea/fractalysis/light',
                     'src/openalea/fractalysis/fracutils']
)


