#import openalea.fractalysis.light as lit
import openalea.plantgl.all as pgl

red = pgl.Material(ambient=pgl.Color3(60,10,30),diffuse=3)
green = pgl.Material(ambient=pgl.Color3(30,60,10),diffuse=3)
blue = pgl.Material(ambient=pgl.Color3(10,30,60),diffuse=3)

def setup_func():
  sc = pgl.Scene()
  sc += pgl.Shape(pgl.Box(1,1,1), red)
  sc+= pgl.Shape(pgl.Translated(4,4,6,pgl.Sphere(1)), blue)
  sc+= pgl.Shape(pgl.Translated(2,3,-3,pgl.Cone(1,2)), green)
  sc+= pgl.Shape(pgl.Translated(-8,3,-2,pgl.Box(4,2,0.5)), blue)
  sc+= pgl.Shape(pgl.Translated(-4,-2,5,pgl.EulerRotated(3.14,2.7,0,pgl.Cone(2,5))), green)
  sc+= pgl.Shape(pgl.Translated(4,-3,-3,pgl.Sphere(2)), red)


  return sc

def teardown_func():
  pass

#@with_setup(setup_func, teardown_func)
def test_setup():
  sc = setup_func()
  pgl.Viewer.display(sc)

def test_projectionPerShape():
  sc = setup_func()
  pgl.Viewer.display(sc)
  nbPixSh, pixSize = pgl.Viewer.frameGL.getProjectionPerShape()
  idScene = [sh.id for sh in sc]
  idScene.sort()
  idProj = [pr[0] for pr in nbPixSh]
  idProj.sort()
  print idScene
  print idProj
  assert idScene == idProj

if __name__ == "__main__":
  #test_setup()
  test_projectionPerShape()
