import enum
import os
import sys
import numpy as np
import numpy.ma as ma
import math as m
from OpenGL.GL  import *
import math
import matplotlib.pyplot as plt
from scipy.sparse import csc_matrix,lil_matrix
import matplotlib.path as mpltPath

if not '_' in globals()['__builtins__']: #Test de la présence de la fonction de traduction i18n "gettext" et définition le cas échéant pour ne pas créer d'erreur d'exécution
    import gettext
    _=gettext.gettext

try:
    from . import wolfogl
except:
    print('Error importing wolfogl.pyd')
    print('   Python version : ' + sys.version)
    print('   If your Python version is not 3.7.x, you need to compile an adapted library with compile_wcython.py in wolfhece library path')
    print('   See comments in compile_wcython.py or launch *python compile_wcython.py build_ext --inplace* in :')
    print('      ' + os.path.dirname(__file__))
    exit()

from .xyz_file import XYZFile
from .PyPalette import wolfpalette
from .PyVertexvectors import vector,wolfvertex

# Objet Wolf Array en simple précision
class WolfArray:
    """ Classe pour l'importation de WOLF arrays"""
    filename = ""
    nbdims = 2
    wolftype = 1
    
    origx = 0.0
    origy = 0.0
    origz = 0.0
    
    translx = 0.0
    transly = 0.0
    translz = 0.0

    dx = 0.0
    dy = 0.0
    dz = 0.0
    
    nbx = 0
    nby = 0
    nbz = 0

    array : ma.masked_array
    rgb=None
    mypal = None
   
    nullvalue = 0
    nbnotnull = 99999
    nbtoplot = 0

    gridsize=100
    gridmaxscales = -1
    mygrid:dict
    idx:str

    myselection:list

    plotted=False

    def __init__(self,fname = None,mold = None,masknull=True):

        self.mypal=wolfpalette(None,"Palette of colors")
        self.mypal.default16()
        self.mygrid={}
        self.myselection=[]

        """ Constructeur d'un WOLF array """
        if fname is not None:
            self.filename = fname
            self.read_all()
            if masknull:
                self.mask_data(0.)
            return
        
        if mold is not None:
            self.nbdims = mold.nbdims
            self.nbx = mold.nbx
            self.nby = mold.nby
            self.nbz = mold.nbz
            self.dx = mold.dx
            self.dy = mold.dy
            self.dz = mold.dz
            self.origx = mold.origx
            self.origy = mold.origy
            self.origz = mold.origz
            self.translx = mold.translx
            self.transly = mold.transly
            self.translz = mold.translz
            self.array = ma.copy(mold.array)
            #return

    def __add__(self, other):
        """Surcharge de l'opérateur d'addition"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims==3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz
        
        newArray.array = self.array + other.array
        return newArray

    def __sub__(self, other):
        """Surcharge de l'opérateur de soustraction"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims==3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz
        
        newArray.array = self.array - other.array
        return newArray

    def __pow__(self, other):
        """Surcharge de l'opérateur puissance"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims==3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz
        
        newArray.array = self.array**other
        return newArray

    def __truediv__(self, other):
        """Surcharge de l'opérateur puissance"""
        newArray = WolfArray()
        newArray.nbdims = self.nbdims
        newArray.nbx = self.nbx
        newArray.nby = self.nby
        newArray.dx = self.dx
        newArray.dy = self.dy
        newArray.origx = self.origx
        newArray.origy = self.origy
        newArray.translx = self.translx
        newArray.transly = self.transly

        if self.nbdims==3:
            newArray.nbz = self.nbz
            newArray.dz = self.dz
            newArray.origz = self.origz
            newArray.translz = self.translz
        
        newArray.array=np.where(other==0.,0.,self.array/other.array)
        return newArray

    def get_xy_infootprint_vect(self,myvect:vector) -> np.ndarray:
        i1,j1=self.get_ij_from_xy(myvect.minx,myvect.miny)
        i2,j2=self.get_ij_from_xy(myvect.maxx,myvect.maxy)
        mypts=np.zeros(((i2-i1+1)*(j2-j1+1),2))
        k=0
        for j in range(j1,j2+1): 
            for i in range(i1,i2+1):
                x,y=self.get_xy_from_ij(i,j)
                mypts[k]=[x,y]
                k+=1
        return mypts

    def select_insidepoly(self,myvect:vector):
        mypoints=self.get_xy_infootprint_vect(myvect)
        polygon=np.asarray(list([vert.x,vert.y] for vert in myvect.myvertices))
        path = mpltPath.Path(polygon)
        inside = path.contains_points(mypoints)
        self.myselection = list(np.where(inside,mypoints))

    def plot_selection(self):
        if len(self.myselection)==0:
            return
        glBegin(GL_QUADS)
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        for cursel in self.myselection:
            x1=cursel[0]-self.dx/2.
            x2=cursel[0]+self.dx/2.
            y1=cursel[1]-self.dy/2.
            y2=cursel[1]+self.dy/2.
            glColor3f(1.,0.,0.)
            glVertex2f(x1,y1)
            glVertex2f(x2,y1)
            glVertex2f(x2,y2)
            glVertex2f(x1,y2)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        for cursel in self.myselection:
            x1=cursel[0]-self.dx/2.
            x2=cursel[0]+self.dx/2.
            y1=cursel[1]-self.dy/2.
            y2=cursel[1]+self.dy/2.
            glColor3f(0.,1.,0.)
            glVertex2f(x1,y1)
            glVertex2f(x2,y1)
            glVertex2f(x2,y2)
            glVertex2f(x1,y2)
        glEnd()

    def reset(self):
        if self.nbdims==2:
            self.array[:,:] = 0.0
        elif self.nbdims==3:
            self.array[:,:,:] = 0.0

    def allocate_ressources(self):
        if self.nbdims==2:
            self.array = ma.ones([self.nbx,self.nby]) 
        elif self.nbdims==3:
            self.array = ma.ones([self.nbx,self.nby,self.nbz]) 

    def read_all(self):
        """ Lecture d'un Wolf aray depuis le nom de fichier """
        self.read_txt_header()
        self.read_data()

    def write_all(self):
        """ Ecriture de tous les fichiers d'un Wolf array """
        self.write_txt_header()
        self.write_array()

    def read_txt_header(self):
        """ Lecture du header .txt """
        f = open(self.filename + '.txt', 'r')
        lines = f.readlines()
        f.close()

        tmp = lines[0].split(':')
        self.nbx = int(tmp[1])
        tmp = lines[1].split(':')
        self.nby = int(tmp[1])
        tmp = lines[2].split(':')
        self.origx = float(tmp[1])
        tmp = lines[3].split(':')
        self.origy = float(tmp[1])
        tmp = lines[4].split(':')
        self.dx = float(tmp[1])
        tmp = lines[5].split(':')
        self.dy = float(tmp[1])
        tmp = lines[6].split(':')
        self.wolftype = int(tmp[1])
        tmp = lines[7].split(':')
        self.translx = float(tmp[1])
        tmp = lines[8].split(':')
        self.transly = float(tmp[1])

        tmp = lines[6].split(':')
        if int(tmp[1])==7:
            self.nbdims=3
            tmp = lines[9].split(':')
            self.nbz = int(tmp[1])
            tmp = lines[10].split(':')
            self.origz = float(tmp[1])
            tmp = lines[11].split(':')
            self.dz = float(tmp[1])
            tmp = lines[12].split(':')
            self.translz = float(tmp[1])

    def write_txt_header(self):
        """ Ecriture de l'en-tête de Wolf array """
        f = open(self.filename + '.txt', 'w')
        f.write('NbX :\t{0}\n'.format(str(self.nbx)))
        f.write('NbY :\t{0}\n'.format(str(self.nby)))
        f.write('OrigX :\t{0}\n'.format(str(self.origx)))
        f.write('OrigY :\t{0}\n'.format(str(self.origy)))
        f.write('DX :\t{0}\n'.format(str(self.dx)))
        f.write('DY :\t{0}\n'.format(str(self.dy)))
        f.write('TypeEnregistrement :\t{0}\n'.format(str(self.wolftype)))
        f.write('TranslX :\t{0}\n'.format(str(self.translx)))
        f.write('TranslY :\t{0}\n'.format(str(self.transly)))
        if self.nbdims==3:
            f.write('NbZ :\t{0}\n'.format(str(self.nbz)))
            f.write('OrigZ :\t{0}\n'.format(str(self.origz)))
            f.write('DZ :\t{0}\n'.format(str(self.dz)))
            f.write('TranslZ :\t{0}\n'.format(str(self.translz)))
        f.close()

    def read_data(self):
        with open(self.filename, 'rb') as f:

            if self.wolftype==1 or self.wolftype==7:
                locarray = np.fromfile(f, dtype=np.float32)
                self.array = ma.masked_array(locarray, dtype=np.float32)
            elif self.wolftype ==2:
                locarray = np.fromfile(f, dtype=np.float64)
                self.array = ma.masked_array(locarray, dtype=np.float64)

            if self.nbdims==2:
                self.array = self.array.reshape(self.nbx, self.nby, order='F')
            elif self.nbdims==3:
                self.array = self.array.reshape(self.nbx, self.nby, self.nbz, order='F')

    def write_array(self):
        """ Ecriture du tableau en binaire """
        self.array.data.transpose().tofile(self.filename, "")

    def write_xyz(self, fname):
        """ Ecriture d un fichier xyz avec toutes les données du Wolf Array """
        my_file = XYZFile(fname)
        my_file.fill_from_wolf_array(self)
        my_file.write_to_file()

    def set_general_frame_from_xyz(self, fname, dx, dy):
        """ Lecture d'un fichier xyz et initialisation des données de base """
        my_file = XYZFile(fname)
        my_file.read_from_file()
        (xlim, ylim) = my_file.get_extent()

        self.dx = dx
        self.dy = dy
        self.origx = m.floor(xlim[0]) - 5.0*self.dx
        self.origy = m.floor(ylim[0]) - 5.0 * self.dy
        self.nbx = int((m.floor(xlim[1]) - m.ceil(xlim[0]))/self.dx) + 10
        self.nby = int((m.floor(ylim[1]) - m.ceil(ylim[0]))/self.dy) + 10

        self.array = np.zeros((self.nbx, self.nby))

    def mask_reset(self):
        if self.nbdims==2:
            self.array.mask = np.zeros((self.nbx,self.nby))
            self.nbnotnull = self.nbx * self.nby
        elif self.nbdims==3:
            self.array.mask = np.zeros((self.nbx,self.nby,self.nbz))
            self.nbnotnull = self.nbx * self.nby * self.nbz 

    def mask_data(self, value):
        self.array.mask = self.array.data == value
        #self.array = np.ma.masked_where(self.array == value, self.array)
        self.nbnotnull = self.array.count()

    def mask_allexceptdata(self, value):
        self.array.mask = self.array.data != value
        self.nbnotnull = self.array.count()

    def mask_invert(self):
        self.array.mask = not(self.array.mask)
        self.nbnotnull = self.array.count()

    def meshgrid(self,mode='gc'):
        x_start = self.translx + self.origx
        y_start = self.transly + self.origy
        if mode is 'gc':
            x_discr = np.linspace(x_start + self.dx / 2, x_start + self.nbx * self.dx - self.dx / 2, self.nbx)
            y_discr = np.linspace(y_start + self.dy / 2, y_start + self.nby * self.dy - self.dy / 2, self.nby)
        elif mode is 'borders':
            x_discr = np.linspace(x_start, x_start + self.nbx * self.dx , self.nbx+1)
            y_discr = np.linspace(y_start , y_start + self.nby * self.dy , self.nby+1)

        y, x = np.meshgrid(y_discr, x_discr)
        return x, y

    def crop(self,i_start,j_start,nbx,nby,k_start=1,nbz=1):
        newWolfArray = WolfArray()
        newWolfArray.nbx = nbx
        newWolfArray.nby = nby
        newWolfArray.dx = self.dx
        newWolfArray.dy = self.dy
        newWolfArray.origx = self.origx + i_start*self.dx
        newWolfArray.origy = self.origy + j_start * self.dy
        newWolfArray.translx = self.translx
        newWolfArray.transly = self.transly

        if self.nbdims ==3:
            newWolfArray.nbz = nbz
            newWolfArray.dz = self.dz
            newWolfArray.origz = self.origz + k_start*self.dz
            newWolfArray.translz = self.translz
            
            newWolfArray.array = self.array[i_start:i_start+nbx, j_start:j_start+nby, k_start:k_start+nbz]
        elif self.nbdims==2:
            newWolfArray.array = self.array[i_start:i_start+nbx, j_start:j_start+nby]
        
        return newWolfArray

    def extremum(self,which='min'):
        if which=='min':
            my_extr = np.amin(self.array)
        else:
            my_extr = np.amax(self.array)

        return my_extr

    def get_ij_from_xy(self,x,y,z=0.,scale=1.,aswolf=False):
        i = int((x - self.origx - self.translx) / (self.dx*scale))
        j = int((y - self.origy - self.transly) / (self.dy*scale))

        if aswolf:
            i+=1
            j+=1

        if self.nbdims==3:
            k = int((z - self.origz - self.translz) / (self.dz*scale))
            if aswolf:
                k+=1
            return i, j, k # ATTENTION, Indices en numérotation Python --> WOLF ajouter +1
        elif self.nbdims==2:
            return i, j # ATTENTION, Indices en numérotation Python --> WOLF ajouter +1

    def get_xy_from_ij(self,i,j,k=0,scale=1.,aswolf=False):
        
        if aswolf:
            i += -1
            j += -1

        x= (i + .5) * (self.dx*scale) + self.origx + self.translx
        y= (j + .5) * (self.dy*scale) + self.origy + self.transly

        if self.nbdims==3:
            if aswolf:
                k += -1
            z= (k - .5) * (self.dz*scale) + self.origz + self.translz
            return x,y,z
        elif self.nbdims==2:
            return x,y

    def get_value(self,x,y,z=0.):

        if self.nbdims==2:        
            i, j = self.get_ij_from_xy(x,y)
            value = self.array[i,j]
        elif self.nbdims==3:
            i, j, k = self.get_ij_from_xy(x,y,z)
            value = self.array[i,j,k]

        return value

    def get_xlim(self,window_x,window_y):
        a_x = window_x / (self.nbx*self.dx)
        a_y = window_y / (self.nby*self.dy)
        if a_x < a_y :
            #C'est la mise à l'échelle selon x qui compte
            return (self.origx + self.translx, self.origx + self.translx + self.nbx * self.dx)
        else:
            #C'est la mise à l'échelle selon y qui compte
            l = (self.nby * self.dy) / window_y * window_x
            return (self.origx + self.translx + self.nbx * self.dx * 0.5 - l * 0.5,
                    self.origx + self.translx + self.nbx * self.dx * 0.5 + l * 0.5)

    def get_ylim(self,window_x,window_y):
        a_x = window_x / (self.nbx * self.dx)
        a_y = window_y / (self.nby * self.dy)
        if a_x < a_y:
            # C'est la mise à l'échelle selon x qui compte
            l = (self.nbx * self.dx) / window_x * window_y
            return (self.origy + self.transly + self.nby * self.dy * 0.5 - l * 0.5,
                    self.origy + self.transly + self.nby * self.dy * 0.5 + l * 0.5)
        else:
            # C'est la mise à l'échelle selon y qui compte
            return (self.origy + self.transly, self.origy + self.transly + self.nby * self.dy)


    def updatepalette(self,which):

        self.mypal.isopop(self.array,self.nbnotnull)
        
        self.rgb=np.ones((self.nbx,self.nby,4),order='F',dtype=np.integer)
        
        self.rgb = self.mypal((self.array-self.mypal.values[0])/(self.mypal.values[-1]-self.mypal.values[0]))

    def plot(self, sx=None, sy=None,xmin=None,ymin=None,xmax=None,ymax=None):

        if not self.plotted:
            return

        if self.plotted and sx is None:
            sx=self.sx
            sy=self.sy
            xmin=self.xmin
            xmax=self.xmax
            ymin=self.ymin
            ymax=self.ymax
        else:
            self.sx=sx
            self.sy=sy
            self.xmin=xmin
            self.xmax=xmax
            self.ymin=ymin
            self.ymax=ymax

        nbpix=min(sx*self.dx,sy*self.dy)
        if nbpix>=1.:
            #si une maille est tracée sur au moins 2 pixels
            curscale=1
        elif math.ceil(1./nbpix)<=3:
            curscale = math.ceil(math.ceil(1./nbpix))
        else:
            curscale = math.ceil(math.ceil(1./nbpix)/3)*3

        curscale=max(curscale,1)
        cursize = curscale #2.**curscale
        curnbx = max(math.ceil(float(self.nbx)/(self.gridsize*cursize)),1)
        curnby = max(math.ceil(float(self.nby)/(self.gridsize*cursize)),1)

        if not cursize in self.mygrid.keys():
            self.mygrid[cursize]={}
            curlist=self.mygrid[cursize]
            curlist['nbx']=curnbx
            curlist['nby']=curnby
            print('réservation listes ')
            numlist = glGenLists(curnbx*curnby)
            curlist['firstlist']=numlist
            print(numlist)
            curlist['mylists']= np.linspace(numlist,numlist+curnbx*curnby-1,num=curnbx*curnby,dtype=np.integer).reshape((curnbx,curnby),order='F')
            curlist['done']=np.zeros((curnbx,curnby),dtype=np.integer,order='F')

        if(curnbx==1 and curnby==1):
            if(self.gridmaxscales==-1):
                self.gridmaxscales=curscale
            elif curscale>self.gridmaxscales:
                curscale=self.gridmaxscales
                cursize = curscale
                curnbx = max(math.ceil(float(self.nbx)/(self.gridsize*cursize)),1)
                curnby = max(math.ceil(float(self.nby)/(self.gridsize*cursize)),1)
            
        istart,jstart = self.get_ij_from_xy(xmin,ymin,scale=cursize*float(self.gridsize))
        iend,jend     = self.get_ij_from_xy(xmax,ymax,scale=cursize*float(self.gridsize))

        istart=max(0,istart)
        jstart=max(0,jstart)
        iend=min(curnbx-1,iend)
        jend=min(curnby-1,jend)
        
        for j in range(jstart,jend+1):
            for i in range(istart,iend+1):
                self.fillonecellgrid(curscale,i,j)
                try:
                    mylistdone = self.mygrid[cursize]['done'][i,j]
                    if mylistdone==1 :
                        mylist = self.mygrid[cursize]['mylists'][i,j]
                        if mylist>0:
                            glCallList(self.mygrid[cursize]['mylists'][i,j])                        
                except:
                    pass

    def delete_lists(self):
        for idx,cursize in enumerate(self.mygrid):
            curlist=self.mygrid[cursize]
            nbx=curlist['nbx']
            nby=curlist['nby']
            first=curlist['firstlist']
            glDeleteLists(first,nbx*nby)

        self.mygrid={}

    def plot_matplotlib(self):

        self.mask_data(0.)
        self.updatepalette(0)

        fig = plt.figure()

        ax = fig.add_subplot(111)
        plt.imshow(self.array.transpose(),origin='lower',cmap=self.mypal,extent=(self.origx,self.origx+self.dx*self.nbx,self.origy,self.origy+self.dy*self.nby))
        ax.set_aspect('equal')

        plt.show()

                            
    def fillonecellgrid(self,curscale,loci,locj,force=False):

        cursize = curscale #2**curscale

        curlist=self.mygrid[cursize]
        exists=curlist['done'][loci,locj]

        if exists==0 or force:
            #print('Computing OpenGL List for '+str(loci)+';' +str(locj) + ' on scale factor '+str(curscale))
            
            ox=self.origx+self.translx
            oy=self.origy+self.transly
            dx=self.dx
            dy=self.dy

            numlist = curlist['mylists'][loci,locj]
            #print(numlist)

            glNewList(numlist,GL_COMPILE)
            glPolygonMode(GL_FRONT_AND_BACK,GL_FILL)      

            step=self.gridsize*cursize
            jstart = max(locj*step,0)
            jend = min(jstart+step,self.nby)
            istart = max(loci*step,0)
            iend = min(istart+step,self.nbx)
            
            if self.wolftype==2:
                if self.nbnotnull!=self.nbx*self.nby:  
                    wolfogl.addme(self.array.astype(dtype=np.float32),self.rgb,ox,oy,dx,dy,jstart,jend,istart,iend,cursize,self.nullvalue)
                else:
                    wolfogl.addmeall(self.array.astype(dtype=np.float32),self.rgb,ox,oy,dx,dy,jstart,jend,istart,iend,cursize,self.nullvalue)
            else:
                if self.nbnotnull!=self.nbx*self.nby:  
                    wolfogl.addme(self.array,self.rgb,ox,oy,dx,dy,jstart,jend,istart,iend,cursize,self.nullvalue)
                else:
                    wolfogl.addmeall(self.array,self.rgb,ox,oy,dx,dy,jstart,jend,istart,iend,cursize,self.nullvalue)

            glEndList()

            curlist['done'][loci,locj]=1