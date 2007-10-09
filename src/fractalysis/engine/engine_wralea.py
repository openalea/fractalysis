# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea fractal analysis library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Wralea for Fractalysis.Library 
"""

__license__= "Cecill-C"
__revision__=" $Id$ "

from openalea.core import *

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'DDS',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'fractalysis.engine nodes.',
               }


    package = Package("fractalysis.engine", metainfo)

###### begin nodes definitions #############

    nf = Factory( name="BCM",
                  description="Apply box counting method on scene",
                  category="compute engine",
                  nodemodule="engine_nodes",
                  nodeclass="BCM",
                  inputs=(dict(name="scene", interface=None,),
                          dict(name="stopFactor", interface=IInt, value=10),
                          ),
                  outputs=(dict(name="scales", interface = ISequence),
                           dict(name="interceptedVoxels", interface = ISequence),),
                  )

    package.add_factory( nf )

    nf = Factory( name="Voxelize",
                  description="Generates an embedding grid for a scene",
                  category="compute engine",
                  nodemodule="engine_nodes",
                  nodeclass="voxelize",
                  inputs=(dict(name="Scene", interface=None,),
                          dict(name="Division Factor", interface=IInt, value=10),
                          dict(name="Density", interface=IBool, value=True),
                          ),
                  outputs=(dict(name="Voxels size", interface = IInt),
                           dict(name="Centers", interface = ISequence),
                           dict(name="Densities", interface = ISequence),
                           dict(name="VoxScene", interface = None),
                          ),
                  #outputs=(dict(name="Voxels", interface = None),
                  #         dict(name="VoxScene", interface = None),),
                  )

    package.add_factory( nf )


###### end nodes definitions ###############

    pkgmanager.add_package(package)


