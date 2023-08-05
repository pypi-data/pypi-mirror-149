
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
from ..PyGui import GPU2DModel

def main(strmydir=''):
    ex = wx.App()
    exLocale = wx.Locale()
    exLocale.Init(wx.LANGUAGE_ENGLISH)
    mydro=GPU2DModel()
    ex.MainLoop()

if __name__=='__main__':
    main()