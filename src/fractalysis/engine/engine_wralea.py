# -*- python -*-
#
#       OpenAlea.Fractalysis : OpenAlea fractal analysis library module
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Da SILVA David <david.da_silva@cirad.fr>
#                       Boudon Frederic <frederic.boudon@cirad.fr>
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
from openalea.core.traitsui import View, Group, Item

def register_packages(pkgmanager):
    """ Initialisation function
    Return a list of package to include in the package manager.
    This function is called by the package manager when it is updated
    """


    metainfo={ 'version' : '0.0.1',
               'license' : 'CECILL-C',
               'authors' : 'DDS, FB',
               'institutes' : 'INRIA/CIRAD',
               'description' : 'fractalysis.engine nodes.',
               }


    package = Package("fractalysis.engine", metainfo)

###### begin nodes definitions #############

    nf = Factory( name="BCM",
                  description="Apply box counting method on scene",
                  category="Fractal Analysis",
                  nodemodule="engine_nodes",
                  nodeclass="BCM",
                  inputs=(dict(name="scene", interface=None,),
                          dict(name="stopFactor", interface=IInt(min=3), value=10),
                          ),
                  outputs=(dict(name="scales", interface = ISequence),
                           dict(name="interceptedVoxels", interface = ISequence),),
                  )

    package.add_factory( nf )

    nf = Factory( name="Voxelize",
                  description="Generates an embedding grid for a scene",
                  category="Fractal Analysis",
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


    nf = Factory( name="TwoSurfaces",
                  description="Computes two surfaces on a multiscale scenes",
                  category="Fractal Analysis",
                  nodemodule="twosurfaces",
                  nodeclass="TwoSurfaces",
                  inputs=(dict(name="leaves", interface=None,),
                          dict(name="macrorep", interface=ISequence),
                          ),
                  outputs=(dict(name="macrosurfaces", interface = ISequence),
                           dict(name="microsurfaces", interface = ISequence),),
                  )

    package.add_factory( nf )

    nf = Factory( name="Scene2MatrixLac",
                  description="Generate a MatrixLac from PlantGL scene",
                  category="Fractal Analysis",
                  nodemodule="engine_nodes",
                  nodeclass="lactrix_fromScene",
                  inputs=(dict(name="Scene", interface=None,),
                          dict(name="Name", interface=IStr),
                          dict(name="Grid Size", interface=IInt(min=2)),
                          dict(name="Save Directory", interface=IDirStr, value='/tmp'),
                          dict(name="Density", interface=IBool, value=False),
                          ),
                  outputs=(dict(name="MatrixLac", interface = None,),
                           dict(name="Pgl scene", interface = None,),
                          ),
                  )

    package.add_factory( nf )

    nf = Factory( name="Lacunarity",
                  description="Compute lacunarity of n-dimensional matrix",
                  category="Fractal Analysis",
                  nodemodule="engine_nodes",
                  nodeclass="lacunarity",
                  view=View(
                          Item("Type"),
                          Group(
                              "GlidingBox radius",
                              Item("Start"),
                              Item("Stop"),
                              layout='-',
                              )
                            ),
                )

    package.add_factory( nf )



###### end nodes definitions ###############

    pkgmanager.add_package(package)


