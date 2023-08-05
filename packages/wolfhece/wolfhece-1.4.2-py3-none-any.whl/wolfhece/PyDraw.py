import numpy as np
from numpy.ma import isarray
from wx import dataview
import wx
import wx.propgrid as pg
from wx.core import VERTICAL, BoxSizer, Height, ListCtrl, StaticText, TextCtrl, Width
from wx.glcanvas import GLCanvas
from wx.glcanvas import GLContext
from wx.dataview import TreeListCtrl
import matplotlib.image as mpimg
from PIL import Image
from io import BytesIO
from OpenGL.GL import *
from OpenGL.GLUT import *

if not '_' in globals()['__builtins__']: #Test de la présence de la fonction de traduction i18n "gettext" et définition le cas échéant pour ne pas créer d'erreur d'exécution
    import gettext
    _=gettext.gettext

from .PyWMS import getIGNFrance,getWalonmap
from .PyVertex import cloud_vertices
from .RatingCurve import SPWMIGaugingStations,SPWDCENNGaugingStations
from .wolf_array import WolfArray
from .PyParams import Wolf_Param
from .BcManager import BcManager
from .PyVertexvectors import *
from .Results2DGPU import wolfres2DGPU

class imagetexture():
    
    parent=None

    name:str
    idtexture:int
    xmin:float
    xmax:float
    ymin:float
    ymax:float

    width:int
    height:int

    which:str
    category:str
    subcategory:str

    France:bool
    epsg:str

    def __init__(self,which:str,label:str,cat:str,subc:str,parent,xmin,xmax,ymin,ymax,width=1000,height=1000,France=False,epsg='31370') -> None:
        
        parent.canvas.SetCurrent(parent.context)
        self.parent=parent
        self.France=France
        self.epsg=epsg

        self.xmin=xmin
        self.xmax=xmax
        self.ymin=ymin
        self.ymax=ymax
        self.idtexture=(GLuint*1)()
        glGenTextures(1,self.idtexture)
        self.width=width
        self.height=height
        self.which=which.lower()
        self.category=cat#.upper()
        self.name=label
        self.subcategory=subc#.upper()
        self.oldview=[self.xmin,self.xmax,self.ymin,self.ymax,self.width,self.height]

        self.load()        

        pass

    def load(self):
        if self.width==-99999 or self.height==-99999:
            return

        self.parent.canvas.SetCurrent(self.parent.context)
        mybytes:BytesIO   

        if self.France:
            mybytes=getIGNFrance(self.category,self.epsg,
                                    self.xmin,self.ymin,self.xmax,self.ymax,
                                    self.width,self.height,False)
        else:
            mybytes=getWalonmap(self.category+'/'+self.subcategory,
                                    self.xmin,self.ymin,self.xmax,self.ymax,
                                    self.width,self.height,False)
        image=Image.open(mybytes)  
        
        glBindTexture(GL_TEXTURE_2D, self.idtexture[0])
        if self.subcategory[:5]=='ORTHO':
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width,self.height, 0, GL_BGRA, GL_UNSIGNED_BYTE, image.tobytes())
        elif image.mode=='RGB':
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width,self.height, 0, GL_RGB, GL_UNSIGNED_BYTE, image.tobytes())
        else:
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, self.width,self.height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image.tobytes())
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        glGenerateMipmap(GL_TEXTURE_2D)
    
    def reload(self):
        dx=self.parent.xmax-self.parent.xmin
        dy=self.parent.ymax-self.parent.ymin
        cx=self.parent.mousex
        cy=self.parent.mousey

        coeff=.5
        self.xmin=cx-dx*coeff
        self.xmax=cx+dx*coeff
        self.ymin=cy-dy*coeff
        self.ymax=cy+dy*coeff
        self.width=self.parent.canvaswidth*2*coeff
        self.height=self.parent.canvasheight*2*coeff

        self.newview=[self.xmin,self.xmax,self.ymin,self.ymax,self.width,self.height]
        if self.newview!=self.oldview:
            self.load()        
            self.oldview=self.newview

    def paint(self):
        
        glColor4f(1.,1.,1.,1.)
        glEnable(GL_TEXTURE_2D)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindTexture(GL_TEXTURE_2D, self.idtexture[0])

        glBegin(GL_QUADS)
        glTexCoord2f(0.0, 0.0)
        glVertex2f(self.xmin,self.ymax)
        glTexCoord2f(1.0, 0.0)
        glVertex2f(self.xmax,self.ymax)
        glTexCoord2f(1.0, 1.0)
        glVertex2f(self.xmax,self.ymin)
        glTexCoord2f(0.0, 1.0)
        glVertex2f(self.xmin,self.ymin)
        glEnd()
        glDisable(GL_TEXTURE_2D)
        glDisable(GL_BLEND)


class WolfMapViewer(wx.Frame):
    '''
    Fenêtre de visualisation de données WOLF grâce aux WxWidgets
    '''
    
    TIMER_ID = 100 #délai d'attente avant action
    
    mybc : BcManager = None #Gestionnaire de CL
    myarrays:list #matrices ajoutées
    myvectors:list #zones vectorielles ajoutées
    myclouds:list #nuages de vertices
    myothers:list 
    mywmsback:list 
    mywmsfore:list 
    regular = True #Gestion de la taille de fenêtre d'affichage, y compris l'arbre de gestion

    sx=1                #facteur d'échelle selon X = largeur en pixels/largeur réelle
    sy=1                #facteur d'échelle selon Y = hauteur en pixels/hauteur réelle
    samescale = True    #force le même facteur d'échelle

    #emprise initiale
    xmin=0.
    ymin=0.
    xmax=40.
    ymax=40.
    width = xmax-xmin   #largeur de la zone d'affichage en coordonnées réelles
    height = ymax-ymin  #hauteur de la zone d'affichage en coordonnées réelles
    canvaswidth=100
    canvasheight=100

    #position de la caméra
    mousex=width/2.
    mousey=height/2.

    bordersize = 0          #zone réservée au contour
    titlesize = 0           #zone réservée au titre
    treewidth = 200         #largeur de la zone d'arbre "treelist"
    canvas:GLCanvas         #canvas OpenGL
    context:GLContext       #context OpenGL
    mytooltip:Wolf_Param    #Objet WOLF permettant l'analyse de ce qui est sous la souris
    treelist:TreeListCtrl   #Gestion des éléments sous forme d'arbre
    selitem:StaticText
    leftbox:BoxSizer
    added:dict              # dictionnaire des éléments ajoutés

    backcolor = wx.Colour(255,255,255)  #couleur de fond
    mousedown=(0.,0.)                   #position initiale du bouton position bas
    mouseup=(0.,0.)                     #position initiale du bouton position haut
    oneclick=True   #détection d'un simple click ou d'un double-click
    move=False      #la souris est-elle en train de bouger?
    
    linked=False
    linkedList=None
    forcemimic=True

    def __init__(self, parent, title,w=500,h=500,treewidth=200):
        self.treewidth = treewidth
        super(WolfMapViewer, self).__init__(parent, title = title,size = (w+self.treewidth,h))

        #Gestion des menus
        self.popupmenu = wx.Menu()
        for text in "one two three four five".split():
            item = self.popupmenu.Append(-1, text)
            self.Bind(wx.EVT_MENU, self.OnPopupItemSelected, item)

        self.menubar = wx.MenuBar()

        self.filemenu = wx.Menu()
        openitem = self.filemenu.Append(wx.ID_OPEN,_('Open'),_('Open file...'))
        saveitem = self.filemenu.Append(wx.ID_SAVE,_('Save'),_('Save data to file'))
        addarray = self.filemenu.Append(wx.ID_FILE1,_('Add array...'),_('Add array (binary file - real)'))
        addvector = self.filemenu.Append(wx.ID_FILE2,_('Add vectors...'),_('Add vectors'))
        addcloud = self.filemenu.Append(wx.ID_FILE3,_('Add cloud...'),_('Add cloud'))

        self.menubar.Append(self.filemenu,_('&File'))
        self.SetMenuBar(self.menubar)
        self.Bind(wx.EVT_MENU, self.OnMenubar)

        #Ajout du conteneur OpenGL
        self.canvas = GLCanvas(self)
        self.context = GLContext(self.canvas)
        self.mybackisloaded=False
        self.myfrontisloaded=False

        #ajout d'une liste en arbre des objets
        self.treelist = TreeListCtrl(self,style=wx.dataview.TL_CHECKBOX|wx.LC_EDIT_LABELS)
        self.selitem = StaticText(self)

        self.root = self.treelist.GetRootItem()
        self.treelist.AppendColumn(_('Objects to plot'))
        self.myitemsarray=self.treelist.AppendItem(self.root, _("Arrays"))
        self.myitemsvector=self.treelist.AppendItem(self.root, _("Vectors"))
        self.myitemscloud=self.treelist.AppendItem(self.root, _("Clouds"))
        self.myitemsothers=self.treelist.AppendItem(self.root, _("Others"))
        self.myitemswmsback=self.treelist.AppendItem(self.root, _("WMS-background"))
        self.myitemswmsfore=self.treelist.AppendItem(self.root, _("WMS-foreground"))

        self.added={}
        self.added['arrays']={}
        self.added['vectors']={}
        self.added['clouds']={}
        self.added['others']={}
        self.added['wms-background']={}
        self.added['wms-foreground']={}

        width,height=self.GetClientSize()
        self.bordersize = int((w-width+self.treewidth)/2)
        self.titlesize = h-height-self.bordersize
        self.SetSize(w+2*self.bordersize+self.treewidth,h+self.bordersize+self.titlesize)

        #dimensionnement et positionnement de la fenêtre OpenGL
        self.canvas.SetSize(width-self.treewidth,height)
        self.canvas.SetPosition((self.treewidth,0))

        self.setbounds()

        #dimensionnement et positionnement de l'arbre
        self.leftbox=BoxSizer(orient=wx.VERTICAL)
        self.leftbox.Add(self.treelist,1,wx.LEFT)
        self.leftbox.Add(self.selitem,0,wx.LEFT)
        self.treelist.SetSize(self.treewidth,height)
        #self.selitem.SetSize(self.treewidth,30)
        self.SetSizer(self.leftbox)
        
        #self.treelist.SetPosition((0,0))
        #self.selitem.SetPosition((0,height-30))
    
        #fenêtre ToolTip
        self.mytooltip = Wolf_Param(self,"Values",ontop=True,to_read=False,withbuttons=False)
        self.mytooltip.SetSize(300,400)
        self.mytooltip.Show(False)

        self.timer = wx.Timer(self, self.TIMER_ID)
        self.Bind(wx.EVT_TIMER, self.OnLMaintains)

        self.InitUI()
    
    def InitUI(self):

        self.Bind(wx.EVT_SIZE, self.OnSize)
        self.Bind(wx.EVT_CLOSE , self.OnClose)

        self.canvas.Bind(wx.EVT_CONTEXT_MENU, self.OnShowPopup)
        self.canvas.Bind(wx.EVT_PAINT, self.OnPaint)
        self.canvas.Bind(wx.EVT_CHAR, self.OnHotKey)
        self.canvas.Bind(wx.EVT_BUTTON, self.OnButton)
        self.canvas.Bind(wx.EVT_LEFT_DCLICK, self.OnLDClick)
        self.canvas.Bind(wx.EVT_LEFT_DOWN, self.OnLDown)
        self.canvas.Bind(wx.EVT_LEFT_UP, self.OnLUp)
        self.canvas.Bind(wx.EVT_RIGHT_DOWN, self.OnRightDown)
        self.canvas.Bind(wx.EVT_RIGHT_UP, self.OnRightUp)
        self.canvas.Bind(wx.EVT_MOTION, self.OnMotion)
        self.canvas.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.canvas.Bind(wx.EVT_MOUSEWHEEL, self.OnButton)
        self.treelist.Bind(dataview.EVT_TREELIST_ITEM_CHECKED, self.OnCheckItem)
        self.treelist.Bind(dataview.EVT_TREELIST_ITEM_ACTIVATED,self.OnRDown)
        # dispo dans wxpython 4.1 self.Bind(wx.EVT_GESTURE_ZOOM,self.OnZoomGesture)

        self.Centre()

        self.myarrays=[]
        self.myvectors=[]
        self.myclouds=[]
        self.myothers=[]
        self.mywmsback=[]
        self.mywmsfore=[]

        self.Show(True)

    def OnSize(self, e):
        """
        Redimensionnement de la fenêtre
        """
        if self.regular:
            #retrouve la taille de la fenêtre
            width,height=self.GetClientSize()
            #enlève la barre d'arbre
            width-=self.treewidth
            #définit la taille de la fenêtre graphique OpenGL et sa position (à droite de l'arbre)
            self.canvas.SetSize(width,height)
            self.canvas.SetPosition((self.treewidth,0))
            #calcule les limites visibles sur base de la taille de la fenêtre et des coefficients sx sy
            self.setbounds()
            #fixe la taille de l'arbre (notamment la hauteur)
            #self.treelist.SetSize(self.treewidth,height)
            e.Skip()

    def setbounds(self):
        '''
        Calcule les limites visibles de la fenêtrte graphique sur base des facteurs d'échelle courants
        '''
        self.updatescalefactors()
        #retrouve la taille de la fenêtre OpenGL
        width,height = self.canvas.GetSize()
        self.canvaswidth=width
        self.canvasheight=height

        #calcule la taille selon X et Y en coordonnées réelles
        width = width / self.sx
        height = height / self.sy
        #retrouve les bornes min et max sur base de la valeur centrale qui est censée ne pas bouger
        self.xmin = self.mousex - width/2.
        self.xmax = self.xmin+width
        self.ymin = self.mousey - height/2.
        self.ymax = self.ymin+height

        self.width = width
        self.height = height

        self.mousex=self.xmin+width/2.
        self.mousey=self.ymin+height/2.

        self.updatescalefactors()
        
        self.mybackisloaded=False
        self.myfrontisloaded=False
        
        self.Refresh()
        if self.forcemimic:
            self.mimicme()

    def updatescalefactors(self):
        width, height = self.canvas.GetSize()

        self.sx=1
        self.sy=1
        if width>0:
            self.sx = float(width)/self.width
        if height>0:
            self.sy = float(height)/self.height

        self.sx=min(self.sx,self.sy)
        self.sy=self.sx

    def OnMenubar(self,event):
        id = event.GetId()
        item = self.menubar.FindItemById(event.GetId())

        if id==wx.ID_FILE1 :
            self.add_object(which='array',ToCheck=True)
            #self.mybc=BcManager(self,newarray.dx,newarray.dy,newarray.origx,newarray.origy,"Boundary conditions")
            #self.mybc.FindBorders(newarray.array)
        elif id==wx.ID_FILE2:
            self.add_object(which='vector',ToCheck=True)
        elif id==wx.ID_FILE3:
            self.add_object(which='cloud',ToCheck=True)

        if len(self.myarrays)+len(self.myvectors)==1:
            self.Autoscale()

    def add_object(self,which:str='array',filename='',newobj=None,ToCheck=True,id=''):
        filterArray="bin (*.bin)|*.bin|all (*.*)|*.*"
        filterVector="vec (*.vec)|*.vec|vecz (*.vecz)|*.vecz|all (*.*)|*.*"
        filterCloud="xyz (*.xyz)|*.xyz|text (*.txt)|*.txt|all (*.*)|*.*"

        if filename=='' and newobj is None:
            #ouverture d'une boîte de dialogue
            if which.lower()=='array':
                file=wx.FileDialog(self,"Choose file", wildcard=filterArray)
            elif which.lower()=='vector':
                file=wx.FileDialog(self,"Choose file", wildcard=filterVector)
            elif which.lower()=='cloud':
                file=wx.FileDialog(self,"Choose file", wildcard=filterCloud)
            elif which.lower()=='other':
                file=wx.FileDialog(self,"Choose file", wildcard=filterCloud)
            elif which.lower()=='wmsback':
                file=wx.FileDialog(self,"Choose file", wildcard=filterCloud)
            elif which.lower()=='wmsfore':
                file=wx.FileDialog(self,"Choose file", wildcard=filterCloud)

            if file.ShowModal() == wx.ID_CANCEL:
                return
            else:
                #récuparétaion du nom de fichier avec chemin d'accès
                filename =file.GetPath()

        if which.lower()=='array':
            curdict=self.added['arrays']
            curtree=self.myitemsarray

            if newobj is None :
                newobj = WolfArray(filename)

            newobj.updatepalette(0)
            self.myarrays.append(newobj)

        elif which.lower()=='vector':
            curdict=self.added['vectors']
            curtree=self.myitemsvector
            if newobj is None:
                newobj = Zones(filename)
            self.myvectors.append(newobj)

        elif which.lower()=='cloud':
            curdict=self.added['clouds']
            curtree=self.myitemscloud
            if newobj is None:
                newobj = cloud_vertices(filename)
            self.myclouds.append(newobj)

        elif which.lower()=='other':
            if not newobj is None:
                curdict=self.added['others']
                curtree=self.myitemsothers
                self.myothers.append(newobj)

        elif which.lower()=='wmsback':
            if not newobj is None:
                curdict=self.added['wms-background']
                curtree=self.myitemswmsback
                self.mywmsback.append(newobj)

        elif which.lower()=='wmsfore':
            if not newobj is None:
                curdict=self.added['wms-foreground']
                curtree=self.myitemswmsfore
                self.mywmsfore.append(newobj)

        if id=='':
            dlg = wx.TextEntryDialog(self, 'ID ? (case insensitive)','Choose an identifier')
            dlg.SetValue('')
            if len(curdict)==0:
                if dlg.ShowModal() == wx.ID_OK:
                    id=dlg.GetValue()
            else:
                id=list(curdict.keys())[0]
                while id.lower() in curdict:
                    if dlg.ShowModal() == wx.ID_OK:
                        id=dlg.GetValue()
            dlg.Destroy()
            
        newobj.idx=id.lower()
            
        myitem=self.treelist.AppendItem(curtree,id,data=newobj)
        
        if ToCheck:
            self.treelist.CheckItem(myitem)
            self.treelist.CheckItem(self.treelist.GetItemParent(myitem))
            newobj.plotted=True

        loc=curdict[id.lower()]={}
        if filename!='':
            loc['listname']=filename.lower()
            loc['filename']=filename.lower()
        loc['values']=newobj
        loc['listitem']=myitem
        loc['checked']=ToCheck

    def getobj(self,id:str):
        for curdict in self.added:
            if id.lower() in self.added[curdict].keys():
                try:
                    return self.added[curdict][id]['values']
                except:
                    pass

    def OnShowPopup(self, event):
        pos = event.GetPosition()
        if pos==(-1,-1):
            width, height = self.GetSize()
            pos = (width/2.,height/2.)
        else:
            pos = pos - self.GetPosition()
        self.PopupMenu(self.popupmenu, pos)

    def OnPopupItemSelected(self, event):
        item = self.popupmenu.FindItemById(event.GetId())
        text = item.GetText()
        wx.MessageBox("You selected item '%s'" % text)

    def OnClose(self,event):
        #glDeleteLists(1,nblists)
        self.Destroy()

    def OnActivatedItem(self,e):
        myitem=e.GetItem()
        nameitem=self.treelist.GetItemText(myitem).lower()
        self.selitem.SetLabel(nameitem)
        pass

    def OnCheckItem(self,event):

        myitem=event.GetItem()
        myparent=self.treelist.GetItemParent(myitem)
        check = self.treelist.GetCheckedState(myitem)
        nameparent=self.treelist.GetItemText(myparent).lower()
        nameitem=self.treelist.GetItemText(myitem).lower()
        
        if nameparent != '':
            curobj=self.getobj(nameitem)
            self.added[nameparent][nameitem]['checked']=bool(check)
            curobj.plotted=bool(check)
            if nameparent=='vectors':
                curobj.showstructure(self)
            if curobj.idx=='grid' and check:
                dlg = wx.TextEntryDialog(self, 'Size of the Grid ? (float)','Choose an size')
                dlg.SetValue('1000.')
                size=1000.
                if dlg.ShowModal() == wx.ID_OK:
                    size=float(dlg.GetValue())
                curobj.creategrid(size,self.xmin,self.ymin,self.xmax,self.ymax)
                pass

    def getXY(self,pospix):

        width,height = self.canvas.GetSize()
        X=float(pospix[0])/self.sx+self.xmin
        Y=float(height - pospix[1])/self.sy+self.ymin
        return X,Y

    def OnZoomGesture(self,e):
        pass

    def OnLeave(self,e):
        if  e.ControlDown():
            self.mytooltip.Show(False)

    def OnRightDown(self,e):
        pos=e.GetPosition()
        x,y =self.getXY(pos)

        self.rightdown=(x,y)

    def OnRightUp(self,e):
        pos=e.GetPosition()
        x,y =self.getXY(pos)

        try:
            minx=min(self.rightdown[0],x)
            miny=min(self.rightdown[1],y)
            maxx=max(self.rightdown[0],x)
            maxy=max(self.rightdown[1],y)

            if minx!=maxx and maxy!=miny :
                self.mybc.ray_tracing_numpy([[minx,miny],[maxx,miny],[maxx,maxy],[minx,maxy]],'X')
                self.mybc.ray_tracing_numpy([[minx,miny],[maxx,miny],[maxx,maxy],[minx,maxy]],'Y')
            else:
                self.mybc.query_kdtree((x,y))
        
            self.mybc.Populate()
            self.Refresh()

        except:
            pass

    def OnButton(self, e):
        d=e.GetWheelDelta()
        r=e.GetWheelRotation()
        a=e.GetWheelAxis()

        self.width=self.width * (1- .1 * (r/max(d,1)))
        self.height=self.height * (1- .1 * (r/max(d,1)))

        self.setbounds()

    def OnLDClick(self,e):
        self.timer.Stop()
        pos=e.GetPosition()
        x,y =self.getXY(pos)
        self.mousex=self.mousedown[0]
        self.mousey=self.mousedown[1]
        self.mousedown=(0.,0.)
        self.oneclick=False
        self.setbounds()

    def OnLDown(self,e):
        if not self.move:
            pos=e.GetPosition()
            x,y =self.getXY(pos)
            self.mousedown=(x,y)
            self.mouseup=self.mousedown
        
            self.timer.Start(1000)

            e.Skip()
        else:
            self.move=False
            self.timer.Stop()
    
    def OnRDown(self,e):
        curzones:Zones
        curzone:zone
        curvect:vector

        myitem=e.GetItem()
        myparent=self.treelist.GetItemParent(myitem)
        check = self.treelist.GetCheckedState(myitem)
        myobj=self.treelist.GetItemData(myitem)
        
        nameparent=self.treelist.GetItemText(myparent).lower()
        nameitem=self.treelist.GetItemText(myitem).lower()

        if type(myobj)==Zones:
            myobj.showstructure(self)
        elif type(myobj)==cloud_vertices:
            myobj.myprop.show()


    def OnLMaintains(self,e):
        if not self.move:
            self.move=True
            print('move on!')
            self.timer.Start(10)
            e.Skip()
        else:
            dx=self.mouseup[0]-self.mousedown[0]
            dy=self.mouseup[1]-self.mousedown[1]

            self.mousex -= dx
            self.mousey -= dy
            self.mouseup = (self.mouseup[0]-dx,self.mouseup[1]-dy)
            
            self.mousedown=self.mouseup
            
            self.Refresh()
            e.Skip()

    def OnLUp(self,e):
        if not self.move:
            self.timer.Stop()
            pos=e.GetPosition()
            x,y =self.getXY(pos)
            self.mouseup = (x,y)

            if self.oneclick:
                self.mousex -= x-self.mousedown[0]
                self.mousey -= y-self.mousedown[1]
                self.setbounds()
            else:
                self.oneclick=True
        
        e.Skip()

    def OnMotion(self, e):

        #Déplacement de la souris sur le canvas OpenGL
        posframe = self.GetPosition()
        pos=e.GetPosition()
        x,y =self.getXY(pos)
        if self.move:
            self.mouseup= (x,y)

        self.mytooltip.myparams.clear()

        curgroup = 'Position'
        self.mytooltip.myparams[curgroup]={}

        curpar = 'Pixel'
        self.mytooltip.myparams[curgroup][curpar]={}
        self.mytooltip.myparams[curgroup][curpar]['name'] ='Pixel'
        self.mytooltip.myparams[curgroup][curpar]['value'] ='('+str(pos[0])+' ; '+str(pos[1])+')'
        self.mytooltip.myparams[curgroup][curpar]['type'] ='String'
        self.mytooltip.myparams[curgroup][curpar]['comment'] =''

        curpar = 'x'
        self.mytooltip.myparams[curgroup][curpar]={}
        self.mytooltip.myparams[curgroup][curpar]['name'] ='Coordinate X'
        self.mytooltip.myparams[curgroup][curpar]['value'] =x
        self.mytooltip.myparams[curgroup][curpar]['type'] ='Float'
        self.mytooltip.myparams[curgroup][curpar]['comment'] =''

        curpar = 'y'
        self.mytooltip.myparams[curgroup][curpar]={}
        self.mytooltip.myparams[curgroup][curpar]['name'] ='Coordinate Y'
        self.mytooltip.myparams[curgroup][curpar]['value'] =y
        self.mytooltip.myparams[curgroup][curpar]['type'] ='Float'
        self.mytooltip.myparams[curgroup][curpar]['comment'] =''

        for locarray in self.myarrays:
            curgroup = locarray.idx
            if self.added['arrays'][curgroup]['checked']:
                self.mytooltip.myparams[curgroup]={}

                try:
                    val = locarray.get_value(x,y)
                    i,j = locarray.get_ij_from_xy(x,y)

                    curpar = 'Indices'
                    self.mytooltip.myparams[curgroup][curpar]={}
                    self.mytooltip.myparams[curgroup][curpar]['name'] ='Indice (i;j)'
                    self.mytooltip.myparams[curgroup][curpar]['value'] ='('+str(i+1)+';'+str(j+1)+')'
                    self.mytooltip.myparams[curgroup][curpar]['type'] ='String'
                    self.mytooltip.myparams[curgroup][curpar]['comment'] =''

                    curpar = 'Value'
                    self.mytooltip.myparams[curgroup][curpar]={}
                    self.mytooltip.myparams[curgroup][curpar]['name'] ='Value'
                    self.mytooltip.myparams[curgroup][curpar]['value'] =val
                    self.mytooltip.myparams[curgroup][curpar]['type'] ='Float'
                    self.mytooltip.myparams[curgroup][curpar]['comment'] =''
                except:
                    pass
                
        if self.linked:
            for curFrame in self.linkedList:
                if not curFrame is self:
                    for locarray in curFrame.myarrays:
                        curgroup = locarray.idx
                        if curFrame.added['arrays'][curgroup]['checked']:
                            self.mytooltip.myparams[curgroup]={}

                            try:
                                val = locarray.get_value(x,y)
                                i,j = locarray.get_ij_from_xy(x,y)

                                curpar = 'Indices'
                                self.mytooltip.myparams[curgroup][curpar]={}
                                self.mytooltip.myparams[curgroup][curpar]['name'] ='Indice (i;j)'
                                self.mytooltip.myparams[curgroup][curpar]['value'] ='('+str(i+1)+';'+str(j+1)+')'
                                self.mytooltip.myparams[curgroup][curpar]['type'] ='String'
                                self.mytooltip.myparams[curgroup][curpar]['comment'] =''

                                curpar = 'Value'
                                self.mytooltip.myparams[curgroup][curpar]={}
                                self.mytooltip.myparams[curgroup][curpar]['name'] ='Value'
                                self.mytooltip.myparams[curgroup][curpar]['value'] =val
                                self.mytooltip.myparams[curgroup][curpar]['type'] ='Float'
                                self.mytooltip.myparams[curgroup][curpar]['comment'] =''
                            except:
                                pass

        self.mytooltip.PopulateOnePage()

        if  e.ControlDown():
            ttsize = self.mytooltip.GetSize()
            self.mytooltip.position(pos+posframe+(ttsize[0]/2.+15,15))
        else:
            width, height = self.GetSize()
            posframe[0]+=width
            self.mytooltip.position(posframe)

        self.mytooltip.Show(True)

        self.Refresh()

    def Autoscale(self,update_backfore=True):
        self.findminmax()
        self.width = self.xmax-self.xmin
        self.height = self.ymax-self.ymin

        centerx=self.xmin+self.width/2.
        centery=self.ymin+self.height/2.

        iwidth=self.width*self.sx
        iheight=self.height*self.sy

        width,height = self.canvas.GetSize()

        sx=float(width)/float(iwidth)
        sy=float(height)/float(iheight)

        if sx>sy:
            self.xmax=self.xmin + self.width*sx/sy
            self.width=self.xmax-self.xmin
        else:
            self.ymax=self.ymin + self.height*sy/sx
            self.height=self.ymax-self.ymin

        self.mousex=centerx
        self.mousey=centery

        if update_backfore:
            #dessin du background
            for id,(key,curmap) in enumerate(self.added['wms-background'].items()):
                if curmap['checked']:
                    curmap['values'].reload()
            #dessin du foreground
            for id,(key,curmap) in enumerate(self.added['wms-foreground'].items()):
                if curmap['checked']:
                    curmap['values'].reload()

        self.setbounds()
    
    def OnHotKey(self, e):
        '''
        Gestion des touches clavier
            F5 : autoscale
            F7 : refresh
            Z  : zoom avant
            z  : zoom artrière
            Flèches : déplacements latéraux
        '''
        key=e.GetKeyCode()
        
        if e.KeyCode==wx.WXK_F2:
            #Dessin des matrices
            try:
                for curarray in self.added['arrays']:
                    if self.added['arrays'][curarray]['checked']:
                        if type(self.added['arrays'][curarray]['values']) is wolfres2DGPU:
                            self.added['arrays'][curarray]['values'].onnext(1)
                
                self.OnPaint(1)
            except:
                pass
        
        
        if e.KeyCode==wx.WXK_F5:
            #Autoscale
            self.Autoscale()

        if e.KeyCode==wx.WXK_F7:
            #dessin du background
            for id,(key,curmap) in enumerate(self.added['wms-background'].items()):
                if curmap['checked']:
                    curmap['values'].reload()
            #dessin du foreground
            for id,(key,curmap) in enumerate(self.added['wms-foreground'].items()):
                if curmap['checked']:
                    curmap['values'].reload()

            self.Refresh()
        elif e.KeyCode == 90: #Z
            self.width=self.width / 1.1
            self.height=self.height / 1.1
            self.setbounds()
        elif e.KeyCode == 122: #z
            self.width=self.width * 1.1
            self.height=self.height * 1.1
            self.setbounds()
        elif e.KeyCode == wx.WXK_UP:
            self.mousey = self.mousey+self.height/10.
            self.setbounds()
        elif e.KeyCode == wx.WXK_DOWN:
            self.mousey = self.mousey-self.height/10.
            self.setbounds()
        elif e.KeyCode == wx.WXK_LEFT:
            self.mousex = self.mousex-self.width/10.
            self.setbounds()
        elif e.KeyCode == wx.WXK_RIGHT:
            self.mousex = self.mousex+self.width/10.
            self.setbounds()

    def OnPaint(self, e):

        width,height=self.canvas.GetSize()

        #C'est bien ici que la zone de dessin utile est calculée sur base du centre et de la zone en coordonnées réelles
        # Les commandes OpenGL sont donc traitées en coordonnées réelles puisque la commande glOrtho définit le cadre visible
        self.xmin=self.mousex-self.width/2.
        self.ymin=self.mousey-self.height/2.
        self.xmax=self.mousex+self.width/2.
        self.ymax=self.mousey+self.height/2.

        self.canvas.SetCurrent(self.context)

        glClearColor(1.,1.,1.,0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glViewport(0,0,int(width),int(height))

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(self.xmin, self.xmax, self.ymin, self.ymax, -99999, 99999)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        #dessin du background
        for id,(key,curmap) in enumerate(self.added['wms-background'].items()):
            if curmap['checked']:
                curmap['values'].paint()

        #Dessin des matrices
        try:
            for curarray in self.added['arrays']:
                if self.added['arrays'][curarray]['checked']:
                    self.added['arrays'][curarray]['values'].plot(self.sx,self.sy,self.xmin,self.ymin,self.xmax,self.ymax)
        except:
            pass

        #Dessin des vecteurs
        try:
            for curvect in self.added['vectors']:
                if self.added['vectors'][curvect]['checked']:
                    self.added['vectors'][curvect]['values'].plot()
        except:
            pass

        #Dessin des nuages
        try:
            for curcloud in self.added['clouds']:
                if self.added['clouds'][curcloud]['checked']:
                    self.added['clouds'][curcloud]['values'].plot()
        except:
            pass

        #Dessin du reste
        try:
            for curobj in self.added['others']:
                if self.added['others'][curobj]['checked']:
                    curobj=self.added['others'][curobj]['values']
                    if type(curobj) is SPWDCENNGaugingStations or type(curobj) is SPWMIGaugingStations:
                        curobj.plot((self.xmax-self.xmin)/100.)
                        
        except: 
            pass

        #Dessin du Front
        for id,(key,curmap) in enumerate(self.added['wms-foreground'].items()):
            if curmap['checked']:
                curmap['values'].paint()


        #Gestion des BC (si actif)
        try:
            if self.mybc!=None:
                self.mybc.plot()
        except:
            pass
    
        glFlush()
        self.canvas.SwapBuffers()
        e.Skip()

    def findminmax(self,force=False):
        xmin = 1.e30
        ymin = 1.e30
        xmax = -1.e30
        ymax = -1.e30

        k=0
        for locarray in self.myarrays:
            if self.added['arrays'][locarray.idx]['checked'] or force:
                xmin = min(locarray.origx+locarray.translx,xmin)
                xmax = max(locarray.origx+locarray.translx + float(locarray.nbx) * locarray.dx,xmax)
                ymin = min(locarray.origy+locarray.transly,ymin)
                ymax = max(locarray.origy+locarray.transly + float(locarray.nby) * locarray.dy,ymax)
                k+=1

        for locvector in self.myvectors:
            if self.added['vectors'][locvector.idx]['checked'] or force:
                if locvector.idx!='grid':
                    locvector.find_minmax()
                    xmin = min(locvector.minx,xmin)
                    xmax = max(locvector.maxx,xmax)
                    ymin = min(locvector.miny,ymin)
                    ymax = max(locvector.maxy,ymax)
                    k+=1

        for loccloud in self.myclouds:
            if self.added['clouds'][loccloud.idx]['checked'] or force:
                loccloud.find_minmax(force)
                xmin = min(loccloud.xbounds[0],xmin)
                xmax = max(loccloud.xbounds[1],xmax)
                ymin = min(loccloud.ybounds[0],ymin)
                ymax = max(loccloud.ybounds[1],ymax)
                k+=1

        if k>0:
            self.xmin=xmin
            self.xmax=xmax
            self.ymin=ymin
            self.ymax=ymax

    def resizeFrame(self,w,h):
        self.SetClientSize(w,h)
        
    def mimicme(self):
        if self.linked:
            if not self.linkedList is None:
                width,height=self.GetClientSize()
                for curFrame in self.linkedList:
                    curFrame.forcemimic=False
                
                for curFrame in self.linkedList:
                    if curFrame != self:
                        curFrame.resizeFrame(width,height)
                        curFrame.mousex = self.mousex
                        curFrame.mousey = self.mousey
                        curFrame.sx = self.sx
                        curFrame.sy = self.sy
                        curFrame.width = self.width
                        curFrame.height = self.height
                        curFrame.setbounds()

                for curFrame in self.linkedList:
                    curFrame.forcemimic=True
                