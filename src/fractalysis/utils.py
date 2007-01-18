#! /usr/bin/env python
"""
:Authors:
  - Da SILVA David
:Organization: Virtual Plants
:Contact: david.da_silva:cirad.fr
:Version: 1.0
:Date: July 2005
"""
import rpy
import pylab
from matplotlib import rc
rc( 'text', usetex=True )

"""
:Abstract: Contain utils functions
"""

##########################Plotting utils#######################################
def delta_vect(list):
    """
    Giving a list, return its step by step difference list.
    
    :param list: the list to be computed
    :type list: float list
    
    :Returns: the step by step difference list
    :Returntype: float list
    """ 
    x_tmp = []
        
    for i in range(1, len(list)):
        dx = float((list[i] - list[i-1]))/(list[i-1])
        x_tmp.append(dx)
        
    return x_tmp

def regression(x, y, regmodel, alpha ):
    
    d = rpy.r.data_frame(X=x, Y=y)
    model = regmodel
    #reg = rpy.r.lm(model, data = d)
    n=rpy.sqrt( len( x ) )
    norm=rpy.r.qnorm( 1. - ( alpha/200. ) )
    Rlm = rpy.with_mode(rpy.NO_CONVERSION, rpy.r.lm)
    reg2 = Rlm(model, data = d)
    result = rpy.r.summary(reg2)
    coef=result['coefficients']
    r2 = result['r.squared']
    r2adj = result['adj.r.squared']
    ic = result[ 'sigma' ]*norm/n
    try:
      pente = coef[1][0]
      intercept = coef[0][0]
    except IndexError :
      pente = coef[0][0]
      intercept = 0

    data = {'pente':pente, 'intercept':intercept, 'r2':r2, 'adj_r2':r2adj, 'ic':ic, 'x':x, 'y':y}
    return data
   
def regLin(x, y, alpha=5):
    """
    Compute the slope and intercept of the 2 given vector linear regression.
    
    :Parameters:
     - `x`: X-axis values
     - `y`: Y-axis values
    
    :Types:
     - `x`: float list
     - `y`: float list
    
    :Returns: the slope and the intercept of the linear regression
    :Returntype: float cople

    :attention: the 2 vector/list must have the same size
    """
    model = rpy.r("Y~X")
    data = regression(x, y, model, alpha )
    return data
    
    #return (reg['coefficients']['X'], reg['coefficients']['(Intercept)']) 

    
def regLinOri(x, y, alpha=5):
    """
    Compute the slope of the 2 given vector pass-through-origin linear regression.
    
    :Parameters:
     - `x`: X-axis values
     - `y`: Y-axis values

    :Types:
     - `x`: float list
     - `y`: float list

    :Returns: the slope of the linear regression
    :Returntype: float
    
    :attention: the 2 vector/list must have the same size
    """
    model = rpy.r("Y~-1+X")
    data = regression(x, y, model, alpha )
    return data
    
    #print "Regression Origine : ", reg

def regLin2Plot( reg, point_legend="data", reg_linestyle='-', point_marker='^', point_color='dodgerblue' ):
    reg_x=rpy.array( [ min(reg[ 'x' ]), max(reg[ 'x' ]) ] )
    reg_y = reg_x*reg[ 'pente' ]+reg[ 'intercept' ]
    reg_legend = "y = "+str( round( reg[ 'pente' ],3 ) )+"x + "+str( round(reg[ 'intercept' ],3 ))+" $\pm$ "+str( round( reg[ 'ic' ],3 ) )+"    r2 = "+str( round( reg[ 'r2' ],3 ) )
    reg_color='red'

    points = plotObject( x=reg[ 'x' ], y=reg[ 'y' ], legend=point_legend, linestyle=None, marker = point_marker, color=point_color )
    line = plotObject( x=reg_x, y=reg_y, legend=reg_legend, linestyle=reg_linestyle, marker=None, color=reg_color )

    return [ points, line ]

def plot2D( objList = None, title='MyPlot', xlabel='x-axis', ylabel='yaxis' ):
    if objList == None :
        pass
    else :
        legend =[]
        for obj in objList :
            pylab.plot( obj.x, obj.y, linestyle=obj.linestyle, marker=obj.marker, color=obj.color, markerfacecolor=obj.color )
            legend.append(r''+obj.legend )
        pylab.legend( tuple( legend ), loc='best', shadow=True )
        pylab.title( title )
        pylab.xlabel( xlabel )
        pylab.ylabel( ylabel )
        pylab.show()


class plotObject:

    def __init__( self, x, y, legend, linestyle, marker, color, ):
        self.x = x
        self.y = y
        self.legend = legend
        self.linestyle = linestyle
        self.marker = marker
        self.color = color
