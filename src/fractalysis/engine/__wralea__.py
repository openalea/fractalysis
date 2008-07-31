
# This file has been generated at Thu Jul 31 17:10:33 2008

from openalea.core import *


__name__ = 'vplants.fractalysis.engine'

__editable__ = True
__description__ = 'Fractalysis engine nodes.'
__license__ = 'CeCILL-C'
__url__ = 'http://openalea.gforge.inria.fr'
__alias__ = ['fractalysis.engine']
__version__ = '0.0.1'
__authors__ = 'OpenAlea consortium'
__institutes__ = 'INRIA/CIRAD'
__icon__ = 'engine_icon.png'
 

__all__ = ['twosurfaces_TwoSurfaces', 'engine_nodes_BCM', 'engine_nodes_lactrix_fromPix', 'engine_nodes_lacunarity', 'engine_nodes_lactrix_fromScene', 'engine_nodes_voxelize']



twosurfaces_TwoSurfaces = Factory(name='TwoSurfaces', 
                description='Computes two surfaces on a multiscale scenes', 
                category='Fractal Analysis', 
                nodemodule='twosurfaces',
                nodeclass='TwoSurfaces',
                inputs=({'interface': None, 'name': 'Leaves'}, {'interface': ISequence, 'name': 'Macrorep'}),
                outputs=({'interface': ISequence, 'name': 'Macrosurfaces'}, {'interface': ISequence, 'name': 'Microsurfaces'}),
                widgetmodule=None,
                widgetclass=None,
                )




engine_nodes_BCM = Factory(name='BCM', 
                description='Apply box counting method on scene', 
                category='Fractal Analysis', 
                nodemodule='engine_nodes',
                nodeclass='BCM',
                inputs=({'interface': None, 'name': 'Scene'}, {'interface': IFloat(min=3, max=16777216, step=1.000000), 'name': 'Stop Factor', 'value': 10}),
                outputs=({'interface': ISequence, 'name': 'Scales'}, {'interface': ISequence, 'name': 'Intercepted Voxels'}),
                widgetmodule=None,
                widgetclass=None,
                )




engine_nodes_lactrix_fromPix = Factory(name='Pix2MatrixLac', 
                description='Generate a MatrixLac from an Image', 
                category='Fractal Analysis', 
                nodemodule='engine_nodes',
                nodeclass='lactrix_fromPix',
                inputs=({'interface': IFileStr, 'name': 'Image path'}, {'interface': IFloat, 'name': 'Pixel width'}, {'interface': IDirStr, 'name': 'Save Directory', 'value': '/tmp'}),
                outputs=({'interface': None, 'name': 'MatrixLac'}, {'interface': None, 'name': 'Thresholded image'}),
                widgetmodule=None,
                widgetclass=None,
                )




engine_nodes_lacunarity = Factory(name='Lacunarity', 
                description='Compute lacunarity of n-dimensional matrix', 
                category='Fractal Analysis', 
                nodemodule='engine_nodes',
                nodeclass='lacunarity',
                inputs=None,
                outputs=None,
                widgetmodule=None,
                widgetclass=None,
                )




engine_nodes_lactrix_fromScene = Factory(name='Scene2MatrixLac', 
                description='Generate a MatrixLac from PlantGL scene', 
                category='Fractal Analysis', 
                nodemodule='engine_nodes',
                nodeclass='lactrix_fromScene',
                inputs=({'interface': None, 'name': 'Scene'}, {'interface': IStr, 'name': 'Name'}, {'interface': IFloat(min=2, max=16777216, step=1.000000), 'name': 'Grid Size'}, {'interface': IDirStr, 'name': 'Save Directory', 'value': '/tmp'}, {'interface': IBool, 'name': 'Density', 'value': False}),
                outputs=({'interface': None, 'name': 'MatrixLac'}, {'interface': None, 'name': 'Pgl scene'}),
                widgetmodule=None,
                widgetclass=None,
                )




engine_nodes_voxelize = Factory(name='Voxelize', 
                description='Generates an embedding grid for a scene', 
                category='Fractal Analysis', 
                nodemodule='engine_nodes',
                nodeclass='voxelize',
                inputs=({'interface': None, 'name': 'Scene'}, {'interface': IInt, 'name': 'Division Factor', 'value': 10}, {'interface': IBool, 'name': 'Density', 'value': True}),
                outputs=({'interface': IInt, 'name': 'Voxels size'}, {'interface': ISequence, 'name': 'Centers'}, {'interface': ISequence, 'name': 'Densities'}, {'interface': None, 'name': 'VoxScene'}),
                widgetmodule=None,
                widgetclass=None,
                )




