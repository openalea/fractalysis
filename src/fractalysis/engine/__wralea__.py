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

from openalea.core import *
from openalea.core.traitsui import View, Group, Item

__name__ = "fractalysis.engine"
__version__ = '0.0.1'
__license__ = 'CeCILL-C'
__authors__ = 'OpenAlea consortium'
__institutes__ = 'INRIA/CIRAD'
__description__ = 'Fractalysis engine nodes.'
__url__ = 'http://openalea.gforge.inria.fr'
__icon__= 'engine_icon.png' 
__editable__ = 'False' 
 
__all__ = ['BCM', 'Voxelize', 'TwoSurfaces', 'Scene2MatrixLac', 'Pix2MatrixLac', 'Lacunarity', ]

###### begin nodes definitions #############

BCM = Factory( name="BCM",
              description="Apply box counting method on scene",
              category="Fractal Analysis",
              nodemodule="engine_nodes",
              nodeclass="BCM",
              inputs=(dict(name="Scene", interface=None,),
                      dict(name="Stop Factor", interface=IInt(min=3), value=10),
                      ),
              outputs=(dict(name="Scales", interface = ISequence),
                       dict(name="Intercepted Voxels", interface = ISequence),),
              )

Voxelize = Factory( name="Voxelize",
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
              )


TwoSurfaces = Factory( name="TwoSurfaces",
              description="Computes two surfaces on a multiscale scenes",
              category="Fractal Analysis",
              nodemodule="twosurfaces",
              nodeclass="TwoSurfaces",
              inputs=(dict(name="Leaves", interface=None,),
                      dict(name="Macrorep", interface=ISequence),
                      ),
              outputs=(dict(name="Macrosurfaces", interface = ISequence),
                       dict(name="Microsurfaces", interface = ISequence),),
              )

Scene2MatrixLac = Factory( name="Scene2MatrixLac",
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


Pix2MatrixLac = Factory( name="Pix2MatrixLac",
              description="Generate a MatrixLac from an Image",
              category="Fractal Analysis",
              nodemodule="engine_nodes",
              nodeclass="lactrix_fromPix",
              inputs=(dict(name="Image path", interface=IFileStr,),
                      dict(name="Pixel width", interface=IFloat),
                      dict(name="Save Directory", interface=IDirStr, value='/tmp'),
                      ),
              outputs=(dict(name="MatrixLac", interface = None,),
                       dict(name="Thresholded image", interface = None,),
                      ),
              )


Lacunarity = Factory( name="Lacunarity",
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

###### end nodes definitions ###############

