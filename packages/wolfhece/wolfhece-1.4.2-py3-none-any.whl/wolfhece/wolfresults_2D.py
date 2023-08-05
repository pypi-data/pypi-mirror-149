import numpy.ma as ma
import numpy as np
from . import wolfpy
from .wolf_array import WolfArray

class OneWolfResult:
    waterdepth : WolfArray 
    qx : WolfArray
    qy : WolfArray

    def __init__(self,fname = None,mold = None):
        self.waterdepth = WolfArray()
        self.top = WolfArray()
        self.qx = WolfArray()
        self.qy = WolfArray()

class Wolfresults_2D(object):
    
    filename=""
    nb_blocks = 0
    myblocks:dict

    def __init__(self,fname = None,mold = None):

        if fname is not None:
            self.filename = fname.ljust(255)

            with open(self.filename.strip() + '.trl') as f:
                trl=f.read().splitlines()
                self.tx=float(trl[1])
                self.ty=float(trl[2])

            wolfpy.r2d_init(self.filename)
            self.nb_blocks = wolfpy.r2d_nbblocks()
            self.myblocks={}
            for i in range(self.nb_blocks):
                curblock = OneWolfResult()
                self.myblocks['block'+str(i+1)] = curblock
                nbx,nby,dx,dy,ox,oy,tx,ty = wolfpy.r2d_hblock(i+1)
                
                self.myblocks['block'+str(i+1)].waterdepth.dx = dx
                self.myblocks['block'+str(i+1)].waterdepth.dy = dy
                self.myblocks['block'+str(i+1)].waterdepth.nbx = nbx
                self.myblocks['block'+str(i+1)].waterdepth.nby = nby
                self.myblocks['block'+str(i+1)].waterdepth.origx = ox
                self.myblocks['block'+str(i+1)].waterdepth.origy = oy
                self.myblocks['block'+str(i+1)].waterdepth.translx = tx
                self.myblocks['block'+str(i+1)].waterdepth.transly = ty

                self.myblocks['block'+str(i+1)].top.dx = dx
                self.myblocks['block'+str(i+1)].top.dy = dy
                self.myblocks['block'+str(i+1)].top.nbx = nbx
                self.myblocks['block'+str(i+1)].top.nby = nby
                self.myblocks['block'+str(i+1)].top.origx = ox
                self.myblocks['block'+str(i+1)].top.origy = oy
                self.myblocks['block'+str(i+1)].top.translx = tx
                self.myblocks['block'+str(i+1)].top.transly = ty
                
                self.myblocks['block'+str(i+1)].qx.dx = dx
                self.myblocks['block'+str(i+1)].qx.dy = dy
                self.myblocks['block'+str(i+1)].qx.nbx = nbx
                self.myblocks['block'+str(i+1)].qx.nby = nby
                self.myblocks['block'+str(i+1)].qx.origx = ox
                self.myblocks['block'+str(i+1)].qx.origy = oy
                self.myblocks['block'+str(i+1)].qx.translx = tx
                self.myblocks['block'+str(i+1)].qx.transly = ty

                self.myblocks['block'+str(i+1)].qx.dx = dx
                self.myblocks['block'+str(i+1)].qx.dy = dy
                self.myblocks['block'+str(i+1)].qx.nbx = nbx
                self.myblocks['block'+str(i+1)].qx.nby = nby
                self.myblocks['block'+str(i+1)].qx.origx = ox
                self.myblocks['block'+str(i+1)].qx.origy = oy
                self.myblocks['block'+str(i+1)].qx.translx = tx
                self.myblocks['block'+str(i+1)].qx.transly = ty

            self.allocate_ressources()
            self.read_topography()
            return

    def allocate_ressources(self):
        for i in range(self.nb_blocks):
            self.myblocks['block'+str(i+1)].waterdepth.allocate_ressources()
            self.myblocks['block'+str(i+1)].top.allocate_ressources()
            self.myblocks['block'+str(i+1)].qx.allocate_ressources()
            self.myblocks['block'+str(i+1)].qy.allocate_ressources()

    def read_topography(self):

        with open(self.filename.strip() + '.topini','rb') as f:
            for i in range(self.nb_blocks):
                nbx=self.myblocks['block'+str(i+1)].top.nbx
                nby=self.myblocks['block'+str(i+1)].top.nby
                nbbytes=nbx*nby*4
                self.myblocks['block'+str(i+1)].top.array = np.frombuffer(f.read(nbbytes),dtype=np.float32)
                self.myblocks['block'+str(i+1)].top.array=self.myblocks['block'+str(i+1)].top.array.reshape(nbx,nby,order='F')


    def get_nbresults(self):
        return  wolfpy.r2d_getnbresults()
    
    def read_oneblockresult_withoutmask(self,which=-1,whichblock=-1):
        if whichblock!=-1:
            nbx = self.myblocks['block'+str(whichblock)].waterdepth.nbx
            nby = self.myblocks['block'+str(whichblock)].waterdepth.nby
            self.myblocks['block'+str(whichblock)].waterdepth.array, self.myblocks['block'+str(whichblock)].qx.array, self.myblocks['block'+str(whichblock)].qy.array = wolfpy.r2d_getresults(which,nbx,nby,whichblock)

    def read_oneblockresult(self,which=-1,whichblock=-1):
        if whichblock!=-1:
            self.read_oneblockresult_withoutmask(which,whichblock)
            self.myblocks['block'+str(whichblock)].waterdepth.array=ma.masked_equal(self.myblocks['block'+str(whichblock)].waterdepth.array,0.)
            self.myblocks['block'+str(whichblock)].qx.array=ma.masked_where(self.myblocks['block'+str(whichblock)].waterdepth.array==0.,self.myblocks['block'+str(whichblock)].qx.array)
            self.myblocks['block'+str(whichblock)].qy.array=ma.masked_where(self.myblocks['block'+str(whichblock)].waterdepth.array==0.,self.myblocks['block'+str(whichblock)].qy.array)

    def read_oneresult(self,which=-1):
        for i in range(self.nb_blocks):
            self.read_oneblockresult(which,i+1)

    def get_values_as_wolf(self,i,j,which_block=1):
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1
        
        nbx = self.myblocks['block'+str(which_block)].waterdepth.nbx
        nby = self.myblocks['block'+str(which_block)].waterdepth.nby

        if(i>0 and i<=nbx and j>0 and j<=nby):
            h = self.myblocks['block'+str(which_block)].waterdepth.array[i-1,j-1]
            top = self.myblocks['block'+str(which_block)].top.array[i-1,j-1]
            qx = self.myblocks['block'+str(which_block)].qx.array[i-1,j-1]
            qy = self.myblocks['block'+str(which_block)].qy.array[i-1,j-1]
            if(h>0.):
                vx = qx/h
                vy = qy/h
                vabs=(vx**2.+vy**2.)**.5
                fr = vabs/(9.81*h)**.5
        
        return h,qx,qy,vx,vy,vabs,fr,h+top,top

    def get_values_from_xy(self,x,y,abs=False):
        h=-1
        qx=-1
        qy=-1
        vx=-1
        vy=-1
        vabs=-1
        fr=-1
        
        exists=False
        for which_block in range(1,self.nb_blocks+1):
            nbx = self.myblocks['block'+str(which_block)].waterdepth.nbx
            nby = self.myblocks['block'+str(which_block)].waterdepth.nby
            i,j=self.get_ij_from_xy(x,y,which_block=which_block,abs=abs)

            if(i>0 and i<=nbx and j>0 and j<=nby):
                h = self.myblocks['block'+str(which_block)].waterdepth.array[i-1,j-1]
                top = self.myblocks['block'+str(which_block)].top.array[i-1,j-1]
                qx = self.myblocks['block'+str(which_block)].qx.array[i-1,j-1]
                qy = self.myblocks['block'+str(which_block)].qy.array[i-1,j-1]
                
                exists = top>0.
                
                if(h>0.):
                    vx = qx/h
                    vy = qy/h
                    vabs=(vx**2.+vy**2.)**.5
                    fr = vabs/(9.81*h)**.5
                    exists=True
                if exists:
                    break

        if exists:
            return (h,qx,qy,vx,vy,vabs,fr,h+top,top),(i,j,which_block)
        else:
            return (-1,-1,-1,-1,-1,-1,-1),('-','-','-')

    def get_xy_from_ij(self,i,j,which_block,abs=False):
        x,y = self.myblocks['block'+str(which_block)].waterdepth.get_xy_from_ij(i,j)
        if abs:
            return x+self.tx,y+self.ty
        else:
            return x,y

    def get_ij_from_xy(self,x,y,which_block,abs=False):
        locx=x
        locy=y
        if abs:
            locx=x-self.tx
            locy=y-self.ty
        
        i,j = self.myblocks['block'+str(which_block)].waterdepth.get_ij_from_xy(locx,locy)
        return i+1,j+1 # En indices WOLF

    def get_blockij_from_xy(self,x,y,abs=False):
        locx=x
        locy=y
        if abs:
            locx=x-self.tx
            locy=y-self.ty

        ret=self.get_values_from_xy(x,y,abs)
        
        return ret[1]

    def extract_allsteps(x,y):
        myvalues=np.zeros()
