from  openalea.plantgl.algo import surface


def scene2surfacedict(sc):
    surfdict = {}
    for sh in sc:
        surfdict[sh.id] = surface(sh.geometry)
    return surfdict

def TwoSurfaces(leaves, macroreps = []):
    """ Compute the surface of envelope and leaves representations """
    print("NbMacro:"+str(len(macroreps)))
    microsurface = []
    macrosurface = []
    detailsurf = scene2surfacedict(leaves)
    for macrograph,macrosc in macroreps:
        print(len(macrograph))
        compodict = {}
        for components in macrograph:
            compodict[components[0]] = components           
        for sh in macrosc:
            root = sh.id
            macrosurface.append(surface(sh))
            microsurface.append(sum([detailsurf[i] for i in compodict[root]]))
    return (macrosurface,microsurface)