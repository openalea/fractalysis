/* -*-c++-*-
 *  ----------------------------------------------------------------------------
 *
 *       Copyright 2005-2008 UMR DAP 
 *
 *       File author(s): D. Da SILVA (david.da_silva@cirad.fr)
 *                       F. BOUDON (frederic.boudon@cirad.fr)
 *
 *       $Id: gridcomputer.cpp,v 1.4 2006/06/20 10:22:57 fboudon Exp $
 *
 *  ----------------------------------------------------------------------------
 *
 *                      GNU General Public Licence
 *
 *       This program is free software; you can redistribute it and/or
 *       modify it under the terms of the GNU General Public License as
 *       published by the Free Software Foundation; either version 2 of
 *       the License, or (at your option) any later version.
 *
 *       This program is distributed in the hope that it will be useful,
 *       but WITHOUT ANY WARRANTY; without even the implied warranty of
 *       MERCHANTABILITY or FITNESS For A PARTICULAR PURPOSE. See the
 *       GNU General Public License for more details.
 *
 *       You should have received a copy of the GNU General Public
 *       License along with this program; see the file COPYING. If not,
 *       write to the Free Software Foundation, Inc., 59
 *       Temple Place - Suite 330, Boston, MA 02111-1307, USA.
 *
 *  ----------------------------------------------------------------------------
 */

#include <string>
#include <vector>
#include <plantgl/math/util_vector.h>
#include <plantgl/tool/util_array.h>
#include <plantgl/scenegraph/scene/scene.h>
#include <plantgl/scenegraph/scene/shape.h>
#include <plantgl/gui3/viewer/pglapplication.h>
#include <plantgl/algo/base/bboxcomputer.h>
#include <plantgl/algo/base/tesselator.h>
#include <plantgl/algo/base/surfcomputer.h>
#include <plantgl/scenegraph/geometry/boundingbox.h>
#include <plantgl/scenegraph/geometry/triangleset.h>


GEOM_USING_NAMESPACE
TOOLS_USING_NAMESPACE
using namespace std;

typedef vector<pair<int,double> > FrResult; //vecteur de couple pour transformer en liste ?
typedef vector<pair<Vector3,float> > FrPointList;

FrPointList * pointDiscretize(const ScenePtr& scene);

pair<Vector3,Vector3> bbox(const FrPointList& points);

pair<Vector3,Vector3> bbox2(const ScenePtr& sc);

void scene2Grid( const FrPointList& points, const pair<Vector3,Vector3>& mbbox, int gridSize, int& intercepted, double& voxelSize  );

pair<int,double> computeGrid(const ScenePtr& scene, int gridSize);

FrResult computeGrids(const ScenePtr& scene, int maxGridSize);

