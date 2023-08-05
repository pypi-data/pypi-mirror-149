import os
import gettext
if os.path.exists(os.path.dirname(__file__)+'\\..\\locales'):
    t = gettext.translation('base', localedir=os.path.dirname(__file__)+'\\..\\locales', languages=['fr'])
    t.install()
else:
    try:
        t = gettext.translation('base', localedir='wolfhece\\locales', languages=['fr'])
        t.install()
    except:
        _=gettext.gettext

import wx
import sys
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.shape_base import block
from numpy.testing._private.utils import measure
from wolfhece.hydrology.Optimisation import Optimisation

from ..hydrology.PostProcessHydrology import PostProcessHydrology
from ..hydrology.Catchment import *
from ..PyParams import*


def main():
    app = wx.App()
    myOpti = Optimisation()

    # %% Show  graphs
    myOpti.Show()
    app.MainLoop()
    print("That's all folks! ")

if __name__=='__main__':
    main()