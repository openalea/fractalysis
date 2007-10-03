#from _light import *
import os
import openalea.plantgl.all as pgl
import skyTurtle as skt
import openalea.fractalysis.fractutils
fruti = openalea.fractalysis.fractutils
import cPickle
import csv
from PIL import Image
from time import sleep

#savedir = "/home/ddasilva/dev/fractalysis/Results/light"
#beam_file = "peachtree4_L.beams"
#sproj_file = "peachtree4_L.sproj"
#beam_file = "cantor.beams"
#sproj_file = "cantor.sproj"

def saveBeams(self,skt_idx, beams, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  beam_file = self.name + "_skt_"+ str(skt_idx) + ".beams"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  param = {'dir':(dir.x, dir.y, dir.z)}
  result = {'beams':beams}
  res = fruti.ParamRes(param, result)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, beam_file)
  f = open(file, 'a')
  cPickle.dump(res, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

def removeScale(self, sc):
  assert sc > 0 and sc < self.depth, "sc not in range"
  for idx in self.get1Scale( sc - 1 ):
    self.getNode( idx ).components = []
  for idx in self.get1Scale( sc ) :
    n = self.getNode( idx )
    n.scale = -1
    cplx = n.cplx
    for cp in n.components :
      self.sonOf( cp, cplx )
  for s in range( sc + 1, self.depth + 1):
    for i in self.get1Scale( s ) :
      self.getNode( i ).scale = s-1
  self.countScale() 

def loadBeams(self, skt_idx, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  beam_file = self.name + "_skt_"+ str(skt_idx) + ".beams"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  file = os.path.join(savedir, beam_file)
  if os.path.isfile( file ):
    f = open( file, 'r' )
    try:
      while( 1 ):
        res = cPickle.load( f )
        if res.testParamEq( "dir", ( dir.x,dir.y,dir.z ) ):
          beams = res.getResult( 'beams' )
          return beams
    except EOFError:
      f.close()
  else :
    print"file does not exist"
    return None

def saveSproj(self, skt_idx, sproj, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_skt_"+ str(skt_idx) + ".sproj"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  param = {'dir':(dir.x, dir.y, dir.z)}
  result = {'sproj':sproj}
  res = fruti.ParamRes(param, result)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  file = os.path.join(savedir, sproj_file)
  f = open(file, 'a')
  cPickle.dump(res, f, protocol=cPickle.HIGHEST_PROTOCOL)
  f.close()

def loadSproj(self,skt_idx, pth=os.path.abspath(os.curdir)):
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  sproj_file = self.name + "_skt_"+ str(skt_idx) + ".sproj"
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  file = os.path.join(savedir, sproj_file)
  print "loading ", file
  if os.path.isfile( file ):
    f = open( file, 'r' )
    try:
      while( 1 ):
        res = cPickle.load( f )
        if res.testParamEq( "dir", ( dir.x,dir.y,dir.z ) ):
          sproj = res.getResult( 'sproj' )
          return sproj
    except EOFError:
      f.close()
  else :
    print"file does not exist"
    return None

def makePict(self, skt_idx, distrib, matrix, width, height, pth=os.path.abspath(os.curdir)):
  dir = "img_skt_" + str(skt_idx)
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name, dir)
  savedir = os.path.join(pth, self.name, dir)
  if not os.path.isdir(savedir):
    os.mkdir(savedir) 
  dis=""
  for d in distrib:
    dis+=str(d)
  pic_file = dis +".jpg"
  file = os.path.join(savedir, pic_file)
  img = Image.new('L', (width, height))
  for x in range(height):
    for y in range(width):
      ndg = 255-255*matrix[x][y]
      try :
        img.putpixel((x,y), ndg) #cause picture are 1/4 clockwise rotated
      except OverflowError:
        print "too big value : ", matrix[x][y]
        img.putpixel((x,y), 0) #cause picture are 1/4 clockwise rotated
  out = img.rotate(90)
  out.save(file, "JPEG")

def checkFactor(self, factor):
  for i in range(1,47):
    prepareScene(self.genScaleScene(1), 300,300, skt_idx = i, dist_factor=factor)
    sleep(0.3)
  
#def computeProjections2(self, skt_idx, width=600, height=600):
#  dir = skt.getSkyTurtleDir(skt_idx)
#  dir.normalize()
#  total = []
#  for s in range(self.countScale()):
#    print "scale ",s+1
#    sc=pgl.Scene([ pgl.Shape(pgl.Translated(-pgl.BoundingBox(i.geometry).getCenter(),i.geometry),i.appearance,i.id) for i in self.genScaleScene(s+1)]) #center each shape of scene
#    pgl.Viewer.display(sc)
#    self.prepareScene(sc, skt_idx, width, height)
#    proj = pgl.Viewer.frameGL.getProjectionSizes(pgl.Viewer.getCurrentScene())
#    total += proj
#  return total

def getPEA(self, **kwds):
  width = kwds.get('width', 300)
  height = kwds.get('height', 300)
  d_factor = kwds.get('d_factor', 4)
  pth = kwds.get('pth', os.path.abspath(os.curdir))
  root_id = self.get1Scale(1)[0]
  skyT = kwds.get('skyT', False)
  integrated = kwds.get('integrated', False)
  PEA = []
  if (integrated or not skyT):
    globPEA = 0
    for s in range(1,47):
      az, el, soc = skt.getSkyTurtleAt(s)
      dir = skt.getSkyTurtleDir(s)
      dir.normalize()
      prepareScene(self.genScaleScene(1), width, height, skt_idx = s, dist_factor=d_factor)
      sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
      PEA.append(sproj)
      globPEA += sproj*soc
    PEA.append(globPEA)
  else :
    az, el, soc = skt.getSkyTurtleAt(skyT)
    dir = skt.getSkyTurtleDir(skyT)
    dir.normalize()
    prepareScene(self.genScaleScene(1), width, height, skt_idx = skyT, dist_factor=d_factor)
    sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
    print "sproj", sproj, "soc", soc
    PEA.append(sproj*soc)
  return PEA

def vgStar(self, **kwds):
  width = kwds.get('width', 300)
  height = kwds.get('height', 300)
  d_factor = kwds.get('d_factor', 4)
  pth = kwds.get('pth', os.path.abspath(os.curdir))
  root_id = self.get1Scale(1)[0]
  tla = self.totalLA(root_id)
  rstar = []
  #cstar = []
  for s in range(1,47):
    dir = skt.getSkyTurtleDir(s)
    dir.normalize()
    prepareScene(self.genScaleScene(self.depth), width, height, skt_idx = s, dist_factor=d_factor)
    sproj = pgl.Viewer.frameGL.getProjectionSize()[0]
    real_star = sproj / tla
    #classic_star = self.starClassic(root_id, dir)
    rstar.append(real_star)
    #cstar.append(classic_star)
    #writing result to file
    az,el,wg = skt.getSkyTurtleAt(s)
    row=[] #line to write in csv file
    row.append(s)   #skyTurtle index
    row.append(str(az).replace('.',','))        #azimut
    row.append(str(el).replace('.',','))        #elevation
    #row.append(str(classic_star).replace('.',',')) #star with uniform leaves distribution in root hull
    row.append(str(real_star).replace('.',',')) #star with uniform leaves distribution in root hull
    row.append(str(wg).replace('.',','))
    savedir = os.path.join(pth, self.name)
    csv_file = self.name + "_vgstar.csv"
    file = os.path.join(savedir, csv_file)
    writer = csv.writer(open(file, 'ab'), dialect='excel')
    writer.writerow(row)

  starReal = 0
  #starUnif = 0
  for i,w in enumerate(skt.weights) :
    starReal+= w*rstar[i]
    #starUnif+= w*cstar[i]

  return starReal#, starUnif

def directionalG(self, skt_idx, **kwds):
  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  pth = kwds.get( 'pth', os.path.abspath(os.curdir) )
  width = kwds.get('width', 300)
  height = kwds.get('height', 300)
  scale = kwds.get('scale', self.depth)

  sproj=self.loadSproj(skt_idx, pth)
  if sproj != None:
    print "projected surface loaded..."
    self.sprojToNodes(dir, sproj)
  else :
    print "computing projections..."
    sproj=self.computeProjections( dir )
    self.saveSproj(skt_idx, sproj, pth)
  
  nodelist = self.get1Scale(scale)
  ratio = 0
  for idx in nodelist:
    n = self.getNode(idx)
    ratio += n.getProjSurface(dir) / n.surface 

  return ratio / len(nodelist)
  



def computeDir(self, skt_idx, distrib=None, width=300, height=300, d_factor=4, pth=os.path.abspath(os.curdir)):
  if distrib== None:
    distrib=[['R']*self.countScale()]

  dir = skt.getSkyTurtleDir(skt_idx)
  dir.normalize()
  az,el,wg = skt.getSkyTurtleAt(skt_idx)

  globScene = self.genScaleScene(1)
  for i in range(1,self.depth):
    globScene.add(self.genScaleScene(i+1))

  prepareScene(globScene, width, height, skt_idx=skt_idx, dist_factor=d_factor)
  #raw_input("Hit return when scene is completely visible in GL frame")
  
  b=self.loadBeams(skt_idx, pth)
  if b != None:
    print "beams loaded..."
  else :
    print "computing beams..."
    b=pgl.Viewer.frameGL.castRays2(pgl.Viewer.getCurrentScene())
    self.saveBeams(skt_idx,b, pth)
  self.beamsToNodes(dir, b)

  sproj=self.loadSproj(skt_idx, pth)
  if sproj != None:
    print "projected surface loaded..."
    self.sprojToNodes(dir, sproj)
  else :
    print "computing projections..."
    sproj=self.computeProjections( dir )
    self.saveSproj(skt_idx, sproj, pth)

  res=[]
  row=[] #line to write in csv file
  row.append(skt_idx)   #skyTurtle index
  #row.append(str(az).replace('.',','))        #azimut
  #row.append(str(el).replace('.',','))        #elevation
  row.append(az)        #azimut
  row.append(el)        #elevation
  row.append(dir)       #vector
  
  root_id = self.get1Scale(1)[0]
  s_classic = self.starClassic(root_id, dir)
  #row.append(str(s_classic).replace('.',',')) #star with uniform leaves distribution in root hull
  row.append(s_classic) #star with uniform leaves distribution in root hull
  res.append(('Beer', s_classic)) 
  for d in distrib:
    print "computing ",d,"..."
    matrix = self.probaImage(root_id, dir, d, width, height)
    self.makePict(skt_idx,d, matrix, width, height, pth)
    s=self.star(root_id, dir, d)
    po = self.getNode(root_id).getPOmega(dir,d)
    res.append((d, s, po ))
    #row.append(str(s).replace('.',','))
    #row.append(str(po).replace('.',','))
    row.append(s)
    row.append(po)

  #row.append(str(wg).replace('.',','))
  row.append(wg)

  #writing in file
  #savedir = os.path.join(frut.pathDB().LIGHTRESULTDIR, self.name)
  savedir = os.path.join(pth, self.name)
  csv_file = self.name + ".csv"
  file = os.path.join(savedir, csv_file)
  writer = csv.writer(open(file, 'ab'), dialect='excel')
  writer.writerow(row)
  
  return res


def prepareScene(scene, width, height, skt_idx=False, dist_factor=4):
  if( skt_idx):
    dir = skt.getSkyTurtleDir(skt_idx)
  else :
    dir = pgl.Viewer.camera.getPosition()[1]
    dir.normalize()
  pgl.Viewer.start()
  pgl.Viewer.display(scene)
  bbox=pgl.BoundingBox( scene )
  pgl.Viewer.animation( True )
  pgl.Viewer.grids.set(False,False,False,False)
  pgl.Viewer.camera.setOrthographic()
  pgl.Viewer.frameGL.setSize(width,height)
  d_factor = max(bbox.getXRange() , bbox.getYRange() , bbox.getZRange())
  pgl.Viewer.camera.lookAt(bbox.getCenter() + dir*(-dist_factor)*d_factor, bbox.getCenter())
  #pgl.Viewer.display(scene)
  return dir



