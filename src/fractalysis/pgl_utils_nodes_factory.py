#       File author(s): Christophe Pradal <christophe.prada@cirad.fr>
#                       Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#
#       Distributed under the Cecill-C License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL-C_V1-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#


__doc__="""
Factory for utils_nodes simplify the wralea file 
"""

__license__= "Cecill-C"
__revision__=" $Id: $ "



from openalea.core.core import Factory


def define_factory(package):
    """ Define factories for PlantGL utils nodes """

    nf = Factory( name= "LoadScene", 
                      description= "load a geom scene", 
                      category = "Tools", 
                      nodemodule = "pgl_utils_nodes",
                      nodeclass = "loadScene",
                      widgetmodule = None,
                      widgetclass = None, 
                      parameters = ['file']
                      )

    package.add_factory( nf )

    nf = Factory( name= "ViewScene", 
                      description= "visualize a scene using PlantGL viewer", 
                      category = "Tools", 
                      nodemodule = "pgl_utils_nodes",
                      nodeclass = "viewScene",
                      widgetmodule = None,
                      widgetclass = None, 
                      parameters = [ ]
                      )

    package.add_factory( nf )


