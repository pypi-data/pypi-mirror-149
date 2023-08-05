import wx
import numpy as np
import numpy.ma as ma
from bisect import bisect_left
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from collections import OrderedDict

if not '_' in globals()['__builtins__']: #Test de la présence de la fonction de traduction i18n "gettext" et définition le cas échéant pour ne pas créer d'erreur d'exécution
    import gettext
    _=gettext.gettext

class wolfpalette(wx.Frame,LinearSegmentedColormap):
    filename=''
    nb = 0
    values = None
    colors : np.array
    colorsflt : np.array
    colormin = [1.,1.,1.]
    colormax = [0,0,0]

    def __init__(self, parent, title,w=100,h=500):

        #pass
        #Appel à l'initialisation d'un frame général
        if(parent!=None):
            wx.Frame.__init__(self, parent, title=title, size=(w,h),style=wx.DEFAULT_FRAME_STYLE)
        LinearSegmentedColormap.__init__(self,'wolf',{},5096*2)

        self.set_under(tuple(self.colormin))
        self.set_over(tuple(self.colormax))

    def export_palette_matplotlib(self):
        cmaps = OrderedDict()
        cmaps['Perceptually Uniform Sequential'] = ['viridis', 'plasma', 'inferno', 'magma', 'cividis']

        cmaps['Sequential'] = ['Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds','YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu','GnBu', 'PuBu', 'YlGnBu','PuBuGn', 'BuGn', 'YlGn']
        cmaps['Sequential (2)'] = ['binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink','spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia','hot', 'afmhot', 'gist_heat', 'copper']
        cmaps['Diverging'] = ['PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu','RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']
        cmaps['Cyclic'] = ['twilight', 'twilight_shifted', 'hsv']
        cmaps['Qualitative'] = ['Pastel1', 'Pastel2', 'Paired', 'Accent','Dark2', 'Set1', 'Set2', 'Set3','tab10', 'tab20', 'tab20b', 'tab20c']
        cmaps['Miscellaneous'] = ['flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern','gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg','gist_rainbow', 'rainbow', 'jet', 'nipy_spectral', 'gist_ncar']

        for cmap_category, cmap_list in cmaps.items():
            self=plt.get_cmap(cmap_list)        

    def lookupcolor(self,x):
        if x < self.values[0]:  return wx.Colour(self.colormin)
        if x > self.values[-1]: return wx.Colour(self.colormax)

        i = bisect_left(self.values, x)
        k = (x - self.values[i-1])/(self.values[i] - self.values[i-1])
        
        r=int(k*(float(self.colors[i,0]-self.colors[i-1,0]))) + self.colors[i-1,0]
        g=int(k*(float(self.colors[i,1]-self.colors[i-1,1]))) + self.colors[i-1,1]
        b=int(k*(float(self.colors[i,2]-self.colors[i-1,2]))) + self.colors[i-1,2]
        a=int(k*(float(self.colors[i,3]-self.colors[i-1,3]))) + self.colors[i-1,3]

        y = wx.Colour(r,g,b,a)

        return y    

    def lookupcolorrgb(self,x):
        if x < self.values[0]:  return wx.Colour(self.colormin)
        if x > self.values[-1]: return wx.Colour(self.colormax)

        i = bisect_left(self.values, x)
        k = (x - self.values[i-1])/(self.values[i] - self.values[i-1])
        
        r=int(k*(float(self.colors[i,0]-self.colors[i-1,0]))) + self.colors[i-1,0]
        g=int(k*(float(self.colors[i,1]-self.colors[i-1,1]))) + self.colors[i-1,1]
        b=int(k*(float(self.colors[i,2]-self.colors[i-1,2]))) + self.colors[i-1,2]
        a=int(k*(float(self.colors[i,3]-self.colors[i-1,3]))) + self.colors[i-1,3]

        return r,g,b,a   

    def default16(self):
        self.nb=16
        self.values = np.linspace(0.,1.,16)
        self.colors = np.zeros((self.nb,4) , dtype=int)
        self.colorsflt = np.zeros((self.nb,4) , dtype=float)
        
        self.colors[0,:] = [128,255,255,255]
        self.colors[1,:] = [89,172,255,255]
        self.colors[2,:] = [72,72,255,255]
        self.colors[3,:] = [0,0,255,255]
        self.colors[4,:] = [0,128,0,255]
        self.colors[5,:] = [0,221,55,255]
        self.colors[6,:] = [128,255,128,255]
        self.colors[7,:] = [255,255,0,255]
        self.colors[8,:] = [255,128,0,255]
        self.colors[9,:] = [235,174,63,255]
        self.colors[10,:] = [255,0,0,255]
        self.colors[11,:] = [209,71,12,255]
        self.colors[12,:] = [128,0,0,255]
        self.colors[13,:] = [185,0,0,255]
        self.colors[14,:] = [111,111,111,255]
        self.colors[15,:] = [192,192,192,255]

        self.fill_segmentdata()

    def fill_segmentdata(self):

        self.colorsflt = self.colors.astype(float)/255.

        self._segmentdata={}
        self._segmentdata['red'] =[]
        self._segmentdata['green'] =[]
        self._segmentdata['blue'] =[]

        if (self.values[-1]-self.values[0])>0.:
            normval = (self.values-self.values[0])/(self.values[-1]-self.values[0])
        else:
            normval = self.values
        normval[0]=0.
        normval[-1]=1.

        for i in range(16):
            self._segmentdata['red'].append((normval[i],self.colorsflt[i,0],self.colorsflt[i,0]))
            self._segmentdata['green'].append((normval[i],self.colorsflt[i,1],self.colorsflt[i,1]))
            self._segmentdata['blue'].append((normval[i],self.colorsflt[i,2],self.colorsflt[i,2]))

    def readfile(self,*args):
        if len(args)>0:
            #s'il y a un argument on le prend tel quel
            self.filename = str(args[0])
        else:
            #ouverture d'une bo�te de dialogue
            file=wx.FileDialog(self,"Choose .pal file", wildcard="pal (*.pal)|*.pal|all (*.*)|*.*")
            if file.ShowModal() == wx.ID_CANCEL: 
                return
            else:
                #r�cupar�taion du nom de fichier avec chemin d'acc�s
                self.filename =file.GetPath()

        #lecture du contenu
        with open(self.filename, 'r') as myfile:
            #split des lignes --> r�cup�ration des infos sans '\n' en fin de ligne
            #  diff�rent de .readlines() qui lui ne supprime pas les '\n'
            mypallines = myfile.read().splitlines()
            myfile.close()

            self.nb = int(mypallines[0])
            self.values = np.zeros(self.nb , dtype=float)
            self.colors = np.zeros((self.nb,3) , dtype=int)

            for i in range(self.nb):
                self.values[i] = mypallines[i*4+1]
                self.colors[i,0] = mypallines[i*4+2]
                self.colors[i,1] = mypallines[i*4+3]
                self.colors[i,2] = mypallines[i*4+4]
                self.colors[i,3] = 255

    #remplissage des valeurs de palette sur base d'une �quir�partition de valeurs
    def isopop(self,array: ma.masked_array,nbnotnull=99999):

        sortarray = array.flatten(order='F')
        sortarray.sort(axis=-1)

        #valeurs min et max
        self.values[0] = sortarray[0]
        
        if(nbnotnull==99999):
            self.values[-1] = sortarray[-1]
            nb = sortarray.count()
        else:
            self.values[-1] = sortarray[nbnotnull-1]
            nb = nbnotnull

        interv = int(nb / (self.nb-1))
        if interv==0:
            self.values[:] = self.values[-1]
            self.values[0]=self.values[-1]-1.
        else:
            for cur in range(1,self.nb-1):
                self.values[cur] = sortarray[cur * interv]

        self.fill_segmentdata()
