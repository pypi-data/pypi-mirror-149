import wx
import wx.lib.agw.aui as aui
import wx.lib.mixins.inspection as wit

from matplotlib import figure as mplfig
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas, NavigationToolbar2WxAgg as NavigationToolbar


class Plot(wx.Panel):

    figure:mplfig.Figure

    def __init__(self, parent, id=-1, dpi=None, **kwargs):
        super().__init__(parent, id=id, **kwargs)
        self.figure = mplfig.Figure(dpi=dpi, figsize=(2, 2))    #Création d'une figure Matplotlib
        self.canvas = FigureCanvas(self, -1, self.figure)       #Création d'un Canvas wx pour contenir le dessin de la figure Matplotlib
        self.toolbar = NavigationToolbar(self.canvas)           #Ajout d'une barre d'outils pour la figure courante
        self.toolbar.Realize()

        sizer = wx.BoxSizer(wx.VERTICAL)                        #ajout d'un sizer pour placer la figure et la barre d'outils l'une au-dessus de l'autre
        sizer.Add(self.canvas, 1, wx.EXPAND)                    #ajout du canvas
        sizer.Add(self.toolbar, 0, wx.LEFT | wx.EXPAND)         #ajout de la barre
        self.SetSizer(sizer)                                    #application du sizer


class PlotNotebook(wx.Panel):
    def __init__(self, parent = None, id=-1):
        if parent is None:
            self.frame = wx.Frame(None, -1, 'Plotter',size=(1024,768))
            super().__init__(self.frame, id=id)
            self.frame.Show()
        else:
            super().__init__(parent, id=id)

        self.ntb = aui.AuiNotebook(self)    #ajout du notebook 
        sizer = wx.BoxSizer()               #sizer pour servir de contenant au notebook
        sizer.Add(self.ntb, 1, wx.EXPAND)   #ajout du notebook au sizer et demande d'étendre l'objet en cas de redimensionnement
        self.SetSizer(sizer)                #applique le sizer

    def add(self, name="plot") -> mplfig.Figure:
        page = Plot(self.ntb)               #crée un objet Plot
        self.ntb.AddPage(page, name)        #ajout de l'objet Plot au notebook
        return page.figure                  #retourne la figure Matplotlib

    def getfigure(self,index = -1, caption="") -> mplfig.Figure:
        if index!=-1:
            return self.ntb.GetPage(index).figure
        elif caption!="":
            for curpage in range(self.ntb.GetPageCount()):
                if caption==self.ntb.GetPageText(curpage):
                    return self.ntb.GetPage(curpage).figure
            return
        else:
            return

def demo():
    app = wx.App()
    frame = wx.Frame(None, -1, 'Plotter')
    plotter = PlotNotebook(frame)
    axes1 = plotter.add('figure 1').add_subplot()
    axes1.plot([1, 2, 3], [2, 1, 4])
    axes2 = plotter.add('figure 2').add_subplot()
    axes2.plot([1, 2, 3, 4, 5], [2, 1, 4, 2, 3])

    fig=plotter.getfigure(0)
    fig.get_axes()[0].plot([5, 6, 10], [2, 1, 10])

    frame.Show()
    app.MainLoop()

if __name__ == "__main__":
    demo()