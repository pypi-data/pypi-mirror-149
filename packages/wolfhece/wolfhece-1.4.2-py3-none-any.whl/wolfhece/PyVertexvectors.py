from matplotlib.pyplot import title
from numpy.lib.function_base import append
import matplotlib.path as mpltPath
import numpy as np
from wx.dataview import TreeListCtrl
from wx.core import HORIZONTAL, BoxSizer, FlexGridSizer, TreeItemId
from wx.lib.agw import xlsgrid
import wx.grid
import wx.dataview
from OpenGL.GL  import *

if not '_' in globals()['__builtins__']: #Test de la présence de la fonction de traduction i18n "gettext" et définition le cas échéant pour ne pas créer d'erreur d'exécution
    import gettext
    _=gettext.gettext

from .CpGrid import CpGrid
from .PyVertex import wolfvertex,getIfromRGB,getRGBfromI
from .PyParams import Wolf_Param

class vectorproperties:
    
    used:bool
    
    color:int
    width:int
    style:int
    alpha:int
    closed=bool
    filled:bool
    legendvisible:bool
    transparent:bool
    flash:bool

    legendtext:str
    legendrelpos:int
    legendx:float
    legendy:float

    legendbold:bool
    legenditalic:bool
    legendunderlined:bool
    legendfontname=str
    legendfontsize:int
    legendcolor:int

    extrude:bool = False

    myprops:Wolf_Param = None

    def __init__(self,lines=[]) -> None:
        
        if len(lines)>0:
            line1=lines[0].split(',')
            line2=lines[1].split(',')

            self.color=int(line1[0])
            self.width=int(line1[1])
            self.style=int(line1[2])
            self.closed=line1[3]=='#TRUE#'
            self.filled=line1[4]=='#TRUE#'
            self.legendvisible=line1[5]=='#TRUE#'
            self.transparent=line1[6]=='#TRUE#'
            self.alpha=int(line1[7])
            self.flash=line1[8]=='#TRUE#'

            self.legendtext=line2[0]
            self.legendrelpos=int(line2[1])
            self.legendx=float(line2[2])
            self.legendy=float(line2[3])
            self.legendbold=line2[4]=='#TRUE#'
            self.legenditalic=line2[5]=='#TRUE#'
            self.legendfontname=str(line2[6])
            self.legendfontsize=int(line2[7])
            self.legendcolor=int(line2[8])
            self.legendunderlined=line2[9]=='#TRUE#'

            self.used=lines[2]=='#TRUE#'
        else:
            self.color=0
            self.width=1
            self.style=1
            self.closed=False
            self.filled=False
            self.legendvisible=False
            self.transparent=False
            self.alpha=0
            self.flash=False

            self.legendtext=''
            self.legendrelpos=5
            self.legendx=0.
            self.legendy=0.
            self.legendbold=False
            self.legenditalic=False
            self.legendfontname='Arial'
            self.legendfontsize=10
            self.legendcolor=0
            self.legendunderlined=False

            self.used=True
        pass
    
    def fill_property(self):
        
        curdict=self.myprops.myparams
        if 'Draw' in curdict.keys():
            keysactive = curdict['Draw'].keys()
            if 'Color' in keysactive:
                self.color = getIfromRGB(curdict['Draw']['Color']['value'].replace('(','').replace(')','').split(', '))
            if 'Width' in keysactive:
                self.width = int(curdict['Draw']['Width']['value'])
            if 'Style' in keysactive:
                self.style = int(curdict['Draw']['Style']['value'])
            if 'Closed' in keysactive:
                self.closed = bool(curdict['Draw']['Closed']['value'])
            if 'Filled' in keysactive:
                self.filled = bool(curdict['Draw']['Filled']['value'])
            if 'Transparent' in keysactive:
                self.transparent = bool(curdict['Draw']['Transparent']['value'])
            if 'Alpha' in keysactive:
                self.alpha = int(curdict['Draw']['Alpha']['value'])
            if 'Flash' in keysactive:
                self.flash = bool(curdict['Draw']['Flash']['value'])

        if 'Legend' in curdict.keys():
            keysactive = curdict['Legend'].keys()
            if 'Underlined' in keysactive:
                self.legendunderlined = bool(curdict['Legend']['Underlined']['value'])
            if 'Bold' in keysactive:
                self.legendbold = bool(curdict['Legend']['Bold']['value'])
            if 'Font name' in keysactive:
                self.legendfontname = str(curdict['Legend']['Font name']['value'])
            if 'Font size' in keysactive:
                self.legendfontsize = int(curdict['Legend']['Font size']['value'])
            if 'Color' in keysactive:
                self.legendcolor = getIfromRGB(curdict['Legend']['Color']['value'].replace('(','').replace(')','').split(', '))
            if 'Italic' in keysactive:
                self.legenditalic = bool(curdict['Legend']['Italic']['value'])
            if 'relative Position' in keysactive:
                self.legendrelpos = int(curdict['Legend']['relative Position']['value'])
            if 'Text' in keysactive:
                self.legendtext = str(curdict['Legend']['Text']['value'])
            if 'Visible' in keysactive:
                self.legendvisible = bool(curdict['Legend']['Visible']['value'])
            if 'X' in keysactive:
                self.legendx = float(curdict['Legend']['X']['value'])
            if 'Y' in keysactive:
                self.legendy = float(curdict['Legend']['Y']['value'])

    def defaultprop(self):
        if self.myprops is None:
            self.myprops=Wolf_Param(title='Vector Properties',to_read=False)
            self.myprops.callbackdestroy = self.destroyprop
            self.myprops.callback=self.fill_property
            self.myprops.saveme.Disable()
            self.myprops.loadme.Disable()
            self.myprops.reloadme.Disable()

        self.myprops.addparam('Draw','Color',(0,0,0),'Color','Drawing color',whichdict='Default')
        self.myprops.addparam('Draw','Width',1,'Integer','Drawing width',whichdict='Default')
        self.myprops.addparam('Draw','Style',1,'Integer','Drawing style',whichdict='Default')
        self.myprops.addparam('Draw','Closed',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Filled',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Transparent',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Draw','Alpha',0,'Integer','Transparent intensity',whichdict='Default')
        self.myprops.addparam('Draw','Flash',False,'Logical','',whichdict='Default')

        self.myprops.addparam('Legend','Visible',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Text','','String','',whichdict='Default')
        self.myprops.addparam('Legend','relative Position',5,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','X',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Y',0,'Float','',whichdict='Default')
        self.myprops.addparam('Legend','Bold',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Italic',False,'Logical','',whichdict='Default')
        self.myprops.addparam('Legend','Font name','Arial','String','',whichdict='Default')
        self.myprops.addparam('Legend','Font size',10,'Integer','',whichdict='Default')
        self.myprops.addparam('Legend','Color',(0,0,0),'Color','',whichdict='Default')
        self.myprops.addparam('Legend','Underlined',False,'Logical','',whichdict='Default')

    def destroyprop(self):
        self.myprops=None

    def show(self):
        self.defaultprop()

        self.myprops.addparam('Draw','Color',getRGBfromI(self.color),'Color','Drawing color')
        self.myprops.addparam('Draw','Width',self.width,'Integer','Drawing width')
        self.myprops.addparam('Draw','Style',self.style,'Integer','Drawing style')
        self.myprops.addparam('Draw','Closed',self.closed,'Logical','')
        self.myprops.addparam('Draw','Filled',self.filled,'Logical','')
        self.myprops.addparam('Draw','Transparent',self.transparent,'Logical','')
        self.myprops.addparam('Draw','Alpha',self.alpha,'Integer','Transparent intensity')
        self.myprops.addparam('Draw','Flash',self.flash,'Logical','')

        self.myprops.addparam('Legend','Visible',self.legendvisible,'Logical','')
        self.myprops.addparam('Legend','Text',self.legendtext,'String','')
        self.myprops.addparam('Legend','relative Position',self.legendrelpos,'Integer','')
        self.myprops.addparam('Legend','X',self.legendx,'Float','')
        self.myprops.addparam('Legend','Y',self.legendy,'Float','')
        self.myprops.addparam('Legend','Bold',self.legendbold,'Logical','')
        self.myprops.addparam('Legend','Italic',self.legenditalic,'Logical','')
        self.myprops.addparam('Legend','Font name',self.legendfontname,'String','')
        self.myprops.addparam('Legend','Font size',self.legendfontsize,'Integer','')
        self.myprops.addparam('Legend','Color',getRGBfromI(self.legendcolor),'Color','')
        self.myprops.addparam('Legend','Underlined',self.legendunderlined,'Logical','')

        self.myprops.Populate()
        self.myprops.Show()


class vector:

    myname:str
    nbvertices:int
    myvertices:list
    myprop:vectorproperties
    minx:float
    miny:float
    maxx:float
    maxy:float

    mytree:TreeListCtrl
    myitem:TreeItemId

    def __init__(self,lines=[],is2D=True,name='') -> None:

        if len(lines)>0:
            self.myname=lines[0]
            self.nbvertices=int(lines[1])
            self.myvertices=[]

            if is2D:
                for i in range(self.nbvertices):
                    curx,cury=lines[2+i].split()
                    curvert = wolfvertex(float(curx),float(cury))
                    self.myvertices.append(curvert)
            else:
                for i in range(self.nbvertices):
                    curx,cury,curz=lines[2+i].split()
                    curvert = wolfvertex(float(curx),float(cury),float(curz))
                    self.myvertices.append(curvert)

            self.myprop=vectorproperties(lines[self.nbvertices+2:])

        if name!='':
            self.myname=name
            self.nbvertices=0
            self.myvertices=[]
            self.myprop=vectorproperties()
        
    def isinside(self,x,y):
        polygon=np.asarray(list([vert.x,vert.y] for vert in self.myvertices))
        path = mpltPath.Path(polygon)
        inside2 = path.contains_points([[x,y]])
        return inside2

    def reset(self):
        self.nbvertices=0
        self.myvertices=[]
    
    def add_vertex(self,addedvert):
        if type(addedvert) is list:
            for curvert in addedvert:
                self.add_vertex(curvert)
        else:
            self.myvertices.append(addedvert)
            self.nbvertices+=1

    def count(self):
        self.nbvertices=len(self.myvertices)

    def nblines(self):
        return self.nbvertices+5

    def find_minmax(self):
        self.minx=min(vert.x for vert in self.myvertices)
        self.miny=min(vert.y for vert in self.myvertices)
        self.maxx=max(vert.x for vert in self.myvertices)
        self.maxy=max(vert.y for vert in self.myvertices)

    def plot(self):

        if self.myprop.used:        
            glLineWidth(float(self.myprop.width))
            #glPointSize(float(self.myprop.width))

            glBegin(GL_LINE_STRIP)
            #!J'aimerais bien changer la largeur du trait mais je n'y parviens pas...
            #!call glGet(GL_ALIASED_LINE_WIDTH_RANGE, max_width)
            rgb=getRGBfromI(self.myprop.color)
            
            glColor3ub(int(rgb[0]),int(rgb[1]),int(rgb[2]))
            for curvertex in self.myvertices:
                glVertex2d(curvertex.x, curvertex.y)

            if self.myprop.closed and (self.myvertices[0].x != self.myvertices[-1].x or self.myvertices[0].y != self.myvertices[-1].y):
                curvertex = self.myvertices[0]
                glVertex2d(curvertex.x, curvertex.y)

            glEnd()

    def add2tree(self,tree:TreeListCtrl,root):
        self.mytree=tree
        self.myitem=tree.AppendItem(root, self.myname,data=self)
        if self.myprop.used:
            tree.CheckItem(self.myitem)

    def unuse(self):
        self.myprop.used=False
        self.mytree.UncheckItem(self.myitem)

    def use(self):
        self.myprop.used=True
        self.mytree.CheckItem(self.myitem)

    def fillgrid(self,gridto:wx.grid.Grid):
        curv:wolfvertex

        gridto.SetColLabelValue(0,'X')
        gridto.SetColLabelValue(1,'Y')
        gridto.SetColLabelValue(2,'Z')
        gridto.SetColLabelValue(3,'value')
        
        nb=gridto.GetNumberRows()
        if len(self.myvertices)-nb>0:
            gridto.AppendRows(len(self.myvertices)-nb)
        k=0
        for curv in self.myvertices:
           gridto.SetCellValue(k,0,str(curv.x))
           gridto.SetCellValue(k,1,str(curv.y))
           gridto.SetCellValue(k,2,str(curv.z))
           k+=1

class zone:

    myname:str
    nbvectors:int
    myvectors:list
    minx:float
    miny:float
    maxx:float
    maxy:float
    selected_vectors:list
    mytree:TreeListCtrl
    myitem:TreeItemId

    def __init__(self,lines=[],name='') -> None:

        if len(lines)>0:
            self.myname=lines[0]
            self.nbvectors=int(lines[1])
            self.myvectors=[]
            curstart=2
            for i in range(self.nbvectors):
                curvec=vector(lines[curstart:])
                curstart+=curvec.nblines()
                self.myvectors.append(curvec)

        if name!='':
            self.myname=name
            self.nbvectors=0
            self.myvectors=[]
        
        self.selected_vectors=[]

        pass

    def add_vector(self,addedvect):
        self.myvectors.append(addedvect)
        self.nbvectors+=1

    def count(self):
        self.nbvectors=len(self.myvectors)

    def nblines(self):
        nb=2
        for curvec in self.myvectors:
            nb+=curvec.nblines()
        
        return nb

    def find_minmax(self,update=False):
        if update:
            for vect in self.myvectors:
                vect.find_minmax()

        self.minx=min(vect.minx for vect in self.myvectors)
        self.miny=min(vect.miny for vect in self.myvectors)
        self.maxx=max(vect.maxx for vect in self.myvectors)
        self.maxy=max(vect.maxy for vect in self.myvectors)

    def plot(self):
        for curvect in self.myvectors:
            curvect.plot()

    def select_vectors_from_point(self,x:float,y:float):
        curvect:vector
        self.selected_vectors.clear()
        for curvect in self.myvectors:
            if curvect.isinside(x,y):
                self.selected_vectors.append(curvect)

    def add2tree(self,tree:TreeListCtrl,root):
        self.mytree=tree
        self.myitem=tree.AppendItem(root, self.myname,data=self)
        tree.CheckItem(self.myitem)
        for curvect in self.myvectors:
            curvect.add2tree(tree,self.myitem)

    def unuse(self):
        for curvect in self.myvectors:
            curvect.unuse()
        self.mytree.UncheckItem(self.myitem)

    def use(self):
        for curvect in self.myvectors:
            curvect.use()
        self.mytree.CheckItem(self.myitem)

class Zones(wx.Frame):

    idx:str
    tx:float
    ty:float
    minx:float
    miny:float
    maxx:float
    maxy:float

    nbzones:int

    myzones:list
    treelist:TreeListCtrl
    xls:wx.grid.Grid

    def __init__(self,myfile='',ox:float=0.,oy:float=0.,tx:float=0.,ty:float=0.,parent=None):

        if myfile!='':
            f = open(myfile, 'r')
            lines = f.read().splitlines()
            f.close()

            tx,ty=lines[0].split()
            self.tx=float(tx)
            self.ty=float(ty)
            self.nbzones=int(lines[1])
            self.myzones=[]

            curstart=2
            for i in range(self.nbzones):
                curzone=zone(lines[curstart:])
                self.myzones.append(curzone)
                curstart+=curzone.nblines()

            self.find_minmax(True)
        else:
            self.minx=ox
            self.miny=oy
            self.tx=tx
            self.ty=ty
            self.myzones=[]
            self.nbzones=0

        super(Zones, self).__init__(parent, size=(300, 400))
        self.Bind(wx.EVT_CLOSE,self.OnClose)

        pass

    def OnClose(self,e):
        self.Hide()
        pass

    def add_zone(self,addedzone):
        self.myzones.append(addedzone)
        self.nbzones+=1

    def find_minmax(self,update=False):
        
        if update:
            for zone in self.myzones:
                zone.find_minmax(update)

        self.minx=min(zone.minx for zone in self.myzones)
        self.miny=min(zone.miny for zone in self.myzones)
        self.maxx=max(zone.maxx for zone in self.myzones)
        self.maxy=max(zone.maxy for zone in self.myzones)

    def plot(self):
        for curzone in self.myzones:
            curzone.plot()

    def select_vectors_from_point(self,x:float,y:float):
        curzone:zone
        for curzone in self.myzones:
            curzone.select_vectors_from_point(x,y)

    def showstructure(self,parent):

        box = BoxSizer(orient=wx.HORIZONTAL)
        self.xls=CpGrid(self,-1,wx.WANTS_CHARS)
        self.xls.CreateGrid(10,4)

        self.treelist = TreeListCtrl(self,style=wx.dataview.TL_CHECKBOX|wx.LC_EDIT_LABELS)
        self.treelist.AppendColumn('Zones')
        self.treelist.Bind(wx.dataview.EVT_TREELIST_ITEM_CHECKED, self.OnCheckItem)
        self.treelist.Bind(wx.dataview.EVT_TREELIST_ITEM_ACTIVATED, self.OnActivateItem)

        box.Add(self.treelist,1,wx.EXPAND)
        box.Add(self.xls,1,wx.EXPAND)

        root = self.treelist.GetRootItem()
        mynode=self.treelist.AppendItem(root, 'All zones',data=self)
        self.treelist.CheckItem(mynode)
        
        curzone:zone
        for curzone in self.myzones:
            curzone.add2tree(self.treelist,mynode)

        self.treelist.SetSize(300,500)

        self.SetSizer(box)
        self.Show()

    def unuse(self):
        for curzone in self.myzones:
            curzone.unuse()

    def use(self):
        for curzone in self.myzones:
            curzone.use()

    def OnCheckItem(self,event):

        myitem=event.GetItem()
        check = self.treelist.GetCheckedState(myitem)
        myitemdata=self.treelist.GetItemData(myitem)
        if check:
            myitemdata.use()
        else:
            myitemdata.unuse()

    def OnActivateItem(self,event):
        myitem=event.GetItem()
        myitemdata=self.treelist.GetItemData(myitem)
        if type(myitemdata) is vector:
            self.xls.ClearGrid()
            myitemdata.fillgrid(self.xls)
            myitemdata.myprop.show()
            
class Grid(Zones):

    def __init__(self, size:float=1000.,ox:float=0.,oy:float=0.,ex:float=1000.,ey:float=1000., parent=None):
        super().__init__(ox=ox, oy=oy, parent=parent)

        mygrid=zone(name='mygrid')
        self.add_zone(mygrid)
        mygridx=vector(name='mygridx')
        mygridy=vector(name='mygridy')
        contour=vector(name='contour')
        mygrid.add_vector(mygridx)
        mygrid.add_vector(mygridy)
        mygrid.add_vector(contour)
        self.creategrid(size,ox,oy,ex,ey)

    def creategrid(self,size:float=100.,ox:float=0.,oy:float=0.,ex:float=1000.,ey:float=1000.):

        mygridx=self.myzones[0].myvectors[0]
        mygridy=self.myzones[0].myvectors[1]
        contour=self.myzones[0].myvectors[2]
        mygridx.reset()
        mygridy.reset()
        contour.reset()

        locox=int(ox/size)*size
        locoy=int(oy/size)*size
        locex=(int(ex/size))*size
        locey=(int(ey/size))*size

        nbx=int((locex-locox)/size)
        nby=int((locey-locoy)/size)

        dx=locex-locox
        dy=locey-locoy

        #grillage vertical        
        xloc=locox
        yloc=locoy
        for i in range(nbx):
            newvert=wolfvertex(xloc,yloc)
            mygridx.add_vertex(newvert)
            
            yloc+=dy
            newvert=wolfvertex(xloc,yloc)
            mygridx.add_vertex(newvert)
            
            xloc+=size
            dy=-dy

        #grillage horizontal        
        xloc=locox
        yloc=locoy
        for i in range(nby):
            newvert=wolfvertex(xloc,yloc)
            mygridy.add_vertex(newvert)
            
            xloc+=dx
            newvert=wolfvertex(xloc,yloc)
            mygridy.add_vertex(newvert)
            
            yloc+=size
            dx=-dx

        newvert=wolfvertex(locox,locoy)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locex,locoy)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locex,locey)
        contour.add_vertex(newvert)
        newvert=wolfvertex(locox,locey)
        contour.add_vertex(newvert)

        self.find_minmax(True)