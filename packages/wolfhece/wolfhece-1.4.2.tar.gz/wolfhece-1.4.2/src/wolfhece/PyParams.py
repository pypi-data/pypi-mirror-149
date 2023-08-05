import wx
import wx.propgrid as pg
import pandas as pd
import os.path
import json
import sys

if not '_' in globals()['__builtins__']: #Test de la présence de la fonction de traduction i18n "gettext" et définition le cas échéant pour ne pas créer d'erreur d'exécution
    import gettext
    _=gettext.gettext

#Gestion des paramètres au format WOLF
class Wolf_Param(wx.Frame):
    #Définition des propriétés
    filename:str
    myparams:dict
    myparams_default:dict
    myIncGroup:dict
    myIncParam:dict
    prop:pg.PropertyGridManager

    callback = None
    callbackdestroy=None

    def addparam(self,groupname='',name='',value='',type='',comment='',jsonstr='',whichdict=''):
        
        if whichdict=='All':
            locparams=[self.myparams,self.myparams_default]
        elif whichdict=='Default':
            locparams=[self.myparams_default]
        else:
            locparams=[self.myparams]

        for curdict in locparams:
            if not groupname in curdict.keys():
                curdict[groupname]={}

            if not name in curdict[groupname].keys():
                curdict[groupname][name]={}
            
            curpar=curdict[groupname][name]

            curpar['name']=name
            curpar['type']=type
            curpar['value']=value
            curpar['comment']=comment

            if jsonstr!='':
                parsed_json = json.loads(jsonstr)
                curpar['added_json']=parsed_json

    #Initialisation
    def __init__(self, parent=None, title="Default Title", w=500,h=800,ontop=False,to_read=True,filename='',withbuttons=True,DestroyAtClosing=True):
        # Initialisation des propriétés
        self.filename=filename
        self.myparams={}
        self.myparams_default={}
        self.myIncGroup={}
        self.myIncParam={}

        #Appel à l'initialisation d'un frame général
        if ontop:
            wx.Frame.__init__(self, parent, title=title, size=(w,h),style=wx.DEFAULT_FRAME_STYLE| wx.STAY_ON_TOP)
        else:
            wx.Frame.__init__(self, parent, title=title, size=(w,h),style=wx.DEFAULT_FRAME_STYLE)

        self.Bind(wx.EVT_CLOSE,self.OnClose)
        self.DestroyAtClosing = DestroyAtClosing
        
        #découpage de la fenêtre
        self.sizer = wx.BoxSizer(wx.HORIZONTAL)

        if withbuttons:
            self.sizerbut = wx.BoxSizer(wx.VERTICAL)
            #boutons
            self.saveme = wx.Button(self,id=10,label="Save to file")
            self.loadme = wx.Button(self,id=10,label="Load from file")
            self.applychange = wx.Button(self,id=10,label="Apply change")
            self.reloadme = wx.Button(self,id=10,label="Reload")
        
            #liaison des actions des boutons
            self.saveme.Bind(wx.EVT_BUTTON,self.SavetoFile)
            self.loadme.Bind(wx.EVT_BUTTON,self.LoadFromFile)
            self.reloadme.Bind(wx.EVT_BUTTON,self.Reload)
            self.applychange.Bind(wx.EVT_BUTTON,self.ApplytoMemory)

        #ajout d'un widget de gestion de propriétés
        if ontop:
            self.prop = pg.PropertyGridManager(self,
                style = pg.PG_BOLD_MODIFIED|pg.PG_SPLITTER_AUTO_CENTER|
                # Plus defaults.
                pg.PGMAN_DEFAULT_STYLE
            )
        else:
            self.prop = pg.PropertyGridManager(self,
                style = pg.PG_BOLD_MODIFIED|pg.PG_SPLITTER_AUTO_CENTER|
                # Include toolbar.
                pg.PG_TOOLBAR |
                # Include description box.
                pg.PG_DESCRIPTION | 
                pg.PG_TOOLTIPS |
                # Plus defaults.
                pg.PGMAN_DEFAULT_STYLE
            )

        self.prop.Bind(pg.EVT_PG_DOUBLE_CLICK,self.OnDblClick)
        
        #ajout au sizer
        if withbuttons:
            self.sizerbut.Add(self.loadme,0,wx.EXPAND)
            self.sizerbut.Add(self.saveme,1,wx.EXPAND)
            self.sizerbut.Add(self.applychange,1,wx.EXPAND)
            self.sizerbut.Add(self.reloadme,1,wx.EXPAND)
            self.sizer.Add(self.sizerbut,0,wx.EXPAND)
        self.sizer.Add(self.prop,1,wx.EXPAND)
        
        if to_read:
            self.ReadFile(filename)
            self.Populate()
        
        #ajout du sizert à la page
        self.SetSizer(self.sizer)
        #self.SetSize(w,h)
        self.SetAutoLayout(1)
        #self.sizer.Fit(self)

        #affichage de la page
        self.Show(True)
        pass
    
    #Gestion du double-click pour ajouter des éléments ou remise à valeur par défaut
    def OnDblClick(self, event):

        #obtention de la propriété sur laquelle on a cliqué
        p = event.GetProperty()
        #nom et valeur du paramètre
        name = p.GetName()
        val = p.GetValue()
        
        #nom du groupe
        group=p.GetParent()
        groupname=group.GetName()

        #on se place sur la page des paramètres actifs
        page = self.prop.GetPage(0)
        if name[0:3]=='def':
            propname = name[3+len(groupname):]
        else:
            propname = name[len(groupname):]

        #pointage vers le paramètre par défaut
        param_def = self.myparams_default[groupname][propname]

        if name[0:3]=='def':
            #click depuis la page des param par défaut

            #essai pour voir si le groupe existe ou non dans les params actifs 
            try:
                locgroup = self.myparams[groupname]
            except:
                locgroup=None

            #si groupe non existant on ajoute
            if locgroup==None:
                page.Append(pg.PropertyCategory(groupname))

            #teste si param existe
            try:
                param = self.myparams[groupname][propname]
            except:
                param=None

            if param==None:
                #si non existant --> on ajoute, si existant --> rien
                locname = groupname + propname
                if 'added_json' in param_def.keys():
                    list_keys = [ k for k in param_def['added_json']['Values'].keys()]
                    list_values = [ k for k in param_def['added_json']['Values'].values()]
                    page.AppendIn(groupname,pg.EnumProperty(propname,name=locname,labels=list_keys,values=list_values,value=int(param_def['value'])))
                else:
                    if param_def['type']=='Integer_or_Float':
                        page.AppendIn(groupname,pg.IntProperty(propname,name=locname,value=float(param_def['value'])))
                    elif param_def['type']=='Integer':
                        page.AppendIn(groupname,pg.IntProperty(propname,name=locname,value=int(param_def['value'])))
                    elif param_def['type']=='Logical':
                        if param_def['value']=='.true.' or param_def['value']=='.True.':
                            mybool=True
                        elif param_def['value']=='.false.' or param_def['value']=='.False.':
                            mybool=False
                        page.AppendIn(groupname,pg.BoolProperty(propname,name=locname,value=mybool))
                    elif param_def['type']=='Float':
                        page.AppendIn(groupname,pg.FloatProperty(propname,name=locname,value=float(param_def['value'])))
                    elif param_def['type']=='File':
                        page.AppendIn(groupname,pg.FileProperty(propname,name=locname,value=param_def['value']))
                    elif param_def['type']=='Directory':
                        newobj=pg.DirProperty(locname,locname,value=param_def['value'])
                        newobj.SetLabel(propname)
                        page.Append(newobj)
                    elif param_def['type']=='Color':
                        page.AppendIn(groupname,pg.ColourProperty(propname,name=locname,value=param_def['value']))
                    elif param_def['type']=='Fontname':
                        page.AppendIn(groupname,pg.FontProperty(propname,name=locname,value=param_def['value']))
                    else:
                        page.AppendIn(groupname,pg.StringProperty(propname,name=locname,value=param_def['value']))

                    try:
                        self.prop.SetPropertyHelpString(locname,param_def['added_json']['Full_Comment'])
                    except:
                        self.prop.SetPropertyHelpString(locname,param_def['comment'])

        else:
            #recopiage de la valeur par défaut
            if param_def['type']=='Integer_or_Float':
                self.prop.SetPropertyValue(groupname + propname,float(param_def['value']))
            elif param_def['type']=='Integer':
                self.prop.SetPropertyValue(groupname + propname,int(param_def['value']))
            elif param_def['type']=='Logical':
                if param_def['value']=='.true.' or param_def['value']=='.True.':
                    mybool=True
                elif param_def['value']=='.false.' or param_def['value']=='.False.':
                    mybool=False
                self.prop.SetPropertyValue(groupname + propname,mybool)
            elif param_def['type']=='Float':
                self.prop.SetPropertyValue(groupname + propname,float(param_def['value']))
            elif param_def['type']=='File':
                self.prop.SetPropertyValue(groupname + propname,param_def['value'])
            elif param_def['type']=='Directory':
                self.prop.SetPropertyValue(groupname + propname,param_def['value'])
            elif param_def['type']=='Color':
                self.prop.SetPropertyValue(groupname + propname,param_def['value'])
            elif param_def['type']=='Fontname':
                self.prop.SetPropertyValue(groupname + propname,param_def['value'])
            else:
                self.prop.SetPropertyValue(groupname + propname,param_def['value'])

    def LoadFromFile(self,event):
        self.myparams.clear()
        self.myparams_default.clear()
        self.ReadFile()
        self.Populate()

    #Lecture d'un fichier .param
    def ReadFile(self,*args):
        if len(args)>0:
            #s'il y a un argument on le prend tel quel
            self.filename = str(args[0])
        else:
            #ouverture d'une boîte de dialogue
            file=wx.FileDialog(self,"Choose .param file", wildcard="param (*.param)|*.param|all (*.*)|*.*")
            if file.ShowModal() == wx.ID_CANCEL: 
                return
            else:
                #récuparétaion du nom de fichier avec chemin d'accès
                self.filename =file.GetPath()

        haveDefaultParams = True
        #idem pour les param par défaut le cas échéant
        if os.path.isfile(self.filename + '.default') :
            with open(self.filename+'.default', 'r') as myfile:
                myparamsline = myfile.read().splitlines()
                myfile.close()
            self.ParseFile(myparamsline,self.myparams_default)
        else:
            haveDefaultParams = False

        #lecture du contenu
        if os.path.isfile(self.filename):
            with open(self.filename, 'r') as myfile:
                #split des lignes --> récupération des infos sans '\n' en fin de ligne
                #  différent de .readlines() qui lui ne supprime pas les '\n'
                myparamsline = myfile.read().splitlines()
                myfile.close()
        
        #conversion et remplissage du dictionnaire
        self.ParseFile(myparamsline,self.myparams)
        if(not(haveDefaultParams)):
            self.ParseFile(myparamsline,self.myparams_default)
            self.createDefaultFile()
        
        self.Update_IncGroup()

    #Parsing du fichier pour trouver groupes et paramètres et remplissage d'un dictionnaire
    def ParseFile(self,myparamsline,todict):

        for param in myparamsline:
            if param.endswith(':'):
                #création d'un dict sur base du nom de groupe, sans le :
                curgroup = param.replace(':','')
                curgroup = curgroup.strip()
                #Par défaut un groupe n'est pas incrémentable
                isInc = False
                #On verifie si le groupe est incrémentable
                curgroup,iterInfo = self.Extract_IncrInfo(curgroup)
                # Groupe avec indice incrémentable 
                if iterInfo!=None:
                    isInc = True
                    iterGroup = iterInfo[0]
                    iterParam = iterInfo[1]
                    iterMin = iterInfo[2]
                    iterMax = iterInfo[3]
                    self.myIncGroup[curgroup] = {}
                    self.myIncGroup[curgroup]["Ref group"] = iterGroup
                    self.myIncGroup[curgroup]["Ref param"] = iterParam
                    self.myIncGroup[curgroup]["Min"] = iterMin
                    self.myIncGroup[curgroup]["Max"] = iterMax
                    self.myIncGroup[curgroup]["Dict"] = {}
                    if not "Saved" in self.myIncGroup[curgroup]:
                        self.myIncGroup[curgroup]["Saved"] = {}
                # Groupe classique
                else:
                    todict[curgroup]={}
            elif param.startswith('%json'):
                #c'est du code json --> on le prend tel quel
                parsed_json = json.loads(param.replace('%json',''))
                curparam['added_json']=parsed_json
            else:
                #split sur base d'une tabulation
                paramloc=param.split('\t')
                #on enlève les espaces avant et après toutes les variables
                for i in range(len(paramloc)) :
                    paramloc[i] = paramloc[i].strip()
                paramloc[0], iterInfo = self.Extract_IncrInfo(paramloc[0])
                #le parametre courant est pas incrémentable -> ajout au dictionnaire particulier des paramètres
                if iterInfo!=None:
                    self.myIncParam[paramloc[0]]["Group"] = curgroup
                    if len(iterInfo)>1:
                        self.myIncParam[paramloc[0]]["Ref param"] = iterInfo[0]
                        self.myIncParam[paramloc[0]]["Min"] = iterInfo[1]
                        self.myIncParam[paramloc[0]]["Max"] = iterInfo[2]
                        self.myIncParam[paramloc[0]]["Dict"] = {}

                    if not "Saved" in self.myIncGroup[curgroup]:
                        self.myIncParam[paramloc[0]]["Saved"] = {}
                        # self.myIncGroup[curgroup]["Dict"][paramloc[0]]=self.myIncParam[paramloc[0]]
                        #pointage du param courant dans le dict de référence
                    curparam=self.myIncParam[paramloc[0]]
                else:
                    #on verifie si le groupe est incrémentable pour pointer vers le bon dictionnaire
                    if isInc:
                        #création d'un dict sur base du nom de paramètre
                        self.myIncGroup[curgroup]["Dict"][paramloc[0]]={}
                        #pointage du param courant dans le dict de référence
                        curparam=self.myIncGroup[curgroup][paramloc[0]]
                    else:
                        #création d'un dict sur base du nom de paramètre
                        todict[curgroup][paramloc[0]]={}
                        #pointage du param courant dans le dict
                        curparam=todict[curgroup][paramloc[0]]

                #ajout de la valeur et du commentaire
                curparam['value']=paramloc[1]
                try:
                    curparam['comment']=paramloc[2]
                                       
                    #recherche du typage
                    if paramloc[2].find('integer')>-1 and paramloc[2].find('double')>-1:
                        curparam['type']='Integer_or_Float'
                    elif paramloc[2].find('integer')>-1:
                        curparam['type']='Integer'
                    elif paramloc[2].find('logical')>-1:
                        curparam['type']='Logical'
                    elif paramloc[2].find('double')>-1 or param.find('dble')>-1 or param.find('real')>-1:
                        curparam['type']='Float'
                    elif paramloc[2].find('(file)')>-1:
                        curparam['type']='File'
                    elif paramloc[2].find('(directory)')>-1 or param.find('(dir)')>-1:
                        curparam['type']='Directory'
                    else:
                        curparam['type']='String'

                    try:
                        param_def=self.myparams_default[curgroup][paramloc[0]]
                        curparam['type']=param_def['type']
                    except:
                        pass
                except:
                    curparam['comment']=''
                    curparam['type']='String'
    
    #Remplissage de l'objet de gestion de propriétés sur base des dictionnaires
    def Populate(self):
        #gestion des paramètres actifs
        try:
            self.prop.Clear()
        except:
            pass
        page = self.prop.AddPage("Active Parameters")
        page = self.prop.AddPage("Default Parameters")

        page = self.prop.GetPage(self.prop.GetPageByName("Active Parameters"))

        if len(self.myparams)>0:
            for group in self.myparams.keys():
                page.Append(pg.PropertyCategory(group))

                for param_name in self.myparams[group].keys():
                    
                    param=self.myparams[group][param_name]
                    locname=group + param_name

                    try:
                        #on donne priorité aux données (type, commentaire) du groupe par défaut mais on utilise la valeur des paramètres actifs
                        param_def=self.myparams_default[group][param_name]
                        if 'added_json' in param_def.keys():
                            list_keys = [ k for k in param_def['added_json']['Values'].keys()]
                            list_values = [ k for k in param_def['added_json']['Values'].values()]
                            page.Append(pg.EnumProperty(param_name,name=locname,labels=list_keys,values=list_values,value=int(float(param['value']))))
                        else:
                            if param_def['type']=='Integer_or_Float':
                                page.Append(pg.IntProperty(label=param_name,name=locname,value=float(param['value'])))
                            elif param_def['type']=='Integer':
                                page.Append(pg.IntProperty(label=param_name,name=locname,value=int(param['value'])))
                            elif param_def['type']=='Logical':
                                if param['value']=='.true.' or param['value']=='.True.':
                                    mybool=True
                                elif param['value']=='.false.' or param['value']=='.False.':
                                    mybool=False
                                elif param['value']==False or param['value']=='false':
                                    mybool=False
                                elif param['value']==True or param['value']=='true':
                                    mybool=True
                                page.Append(pg.BoolProperty(label=param_name,name=locname,value=mybool))
                            elif param_def['type']=='Float':
                                page.Append(pg.FloatProperty(label=param_name,name=locname,value=float(param['value'])))
                            elif param_def['type']=='File':
                                page.Append(pg.FileProperty(label=param_name,name=locname,value=param['value']))
                            elif param_def['type']=='Directory':
                                newobj=pg.DirProperty(locname,locname,value=param['value'])
                                newobj.SetLabel(param_name)
                                page.Append(newobj)
                            elif param_def['type']=='Color':
                                page.Append(pg.ColourProperty(label=param_name,name=locname,value=param['value']))
                            elif param_def['type']=='Fontname':
                                page.Append(pg.FontProperty(label=param_name,name=locname,value=param['value']))
                            else:
                                page.Append(pg.StringProperty(label=param_name,name=locname,value=param['value']))
                    except:
                        #si le groupe par défaut n'a pas de groupe équivalent, on lit les élément du groupe actif
                        if 'added_json' in param.keys():
                            list_keys = [ k for k in param['added_json']['Values'].keys()]
                            list_values = [ k for k in param['added_json']['Values'].values()]
                            page.Append(pg.EnumProperty(label=param_name,name=locname,labels=list_keys,values=list_values,value=int(param['value'])))
                        else:
                            if param['type']=='Integer_or_Float':
                                page.Append(pg.IntProperty(label=param_name,name=locname,value=float(param['value'])))
                            elif param['type']=='Integer':
                                page.Append(pg.IntProperty(label=param_name,name=locname,value=int(param['value'])))
                            elif param['type']=='Logical':
                                if param['value']=='.true.' or param['value']=='.True.':
                                    mybool=True
                                elif param['value']=='.false.' or param['value']=='.False.':
                                    mybool=False
                                elif param['value']==False or param['value']=='false':
                                    mybool=False
                                elif param['value']==True or param['value']=='true':
                                    mybool=True
                                page.Append(pg.BoolProperty(label=param_name,name=locname,value=mybool))
                            elif param['type']=='Float':
                                page.Append(pg.FloatProperty(label=param_name,name=locname,value=float(param['value'])))
                            elif param['type']=='File':
                                page.Append(pg.FileProperty(label=param_name,name=locname,value=param['value']))
                            elif param['type']=='Directory':
                                newobj=pg.DirProperty(locname,locname,value=param['value'])
                                newobj.SetLabel(param_name)
                                page.Append(newobj)
                            elif param['type']=='Color':
                                page.Append(pg.ColourProperty(label=param_name,name=locname,value=param['value']))
                            elif param['type']=='Fontname':
                                page.Append(pg.FontProperty(label=param_name,name=locname,value=param['value']))
                            else:
                                page.Append(pg.StringProperty(label=param_name,name=locname,value=param['value']))
                
                    try:
                        self.prop.SetPropertyHelpString(locname,param_def['added_json']['Full_Comment'])
                    except:
                        try:
                            self.prop.SetPropertyHelpString(locname,param_def['comment'])
                        except:
                            self.prop.SetPropertyHelpString(locname,param['comment'])

        #gestion des paramètres par défaut
        page = self.prop.GetPage(self.prop.GetPageByName("Default Parameters"))

        if len(self.myparams_default)>0:
            for group in self.myparams_default.keys():
                page.Append(pg.PropertyCategory(group))

                for param_name in self.myparams_default[group].keys():
                    
                    param=self.myparams_default[group][param_name]
                    locname='def' + group + param_name
                    
                    addJson=False
                    if 'added_json' in param.keys():
                        addJson=True
                    
                    if addJson:
                        list_keys = [ k for k in param['added_json']['Values'].keys()]
                        list_values = [ k for k in param['added_json']['Values'].values()]
                        page.Append(pg.EnumProperty(param_name,name=locname,labels=list_keys,values=list_values,value=int(float(param['value']))))
                    else:
                        if param['type']=='Integer_or_Float':
                            page.Append(pg.IntProperty(label=param_name,name=locname,value=float(param['value'])))
                        elif param['type']=='Integer':
                            page.Append(pg.IntProperty(label=param_name,name=locname,value=int(param['value'])))
                        elif param['type']=='Logical':
                            if param['value']=='.true.' or param['value']=='.True.':
                                mybool=True
                            elif param['value']=='.false.' or param['value']=='.False.':
                                mybool=False
                            elif param['value']==False or param['value']=='false':
                                mybool=False
                            elif param['value']==True or param['value']=='true':
                                mybool=True
                            page.Append(pg.BoolProperty(label=param_name,name=locname,value=mybool))
                        elif param['type']=='Float':
                            page.Append(pg.FloatProperty(label=param_name,name=locname,value=float(param['value'])))
                        elif param['type']=='File':
                            page.Append(pg.FileProperty(label=param_name,name=locname,value=param['value']))
                        elif param['type']=='Directory':
                            newobj=pg.DirProperty(locname,locname,value=param['value'])
                            newobj.SetLabel(param_name)
                            page.Append(newobj)
                        elif param['type']=='Color':
                            page.Append(pg.ColourProperty(label=param_name,name=locname,value=param['value']))
                        elif param_def['type']=='Fontname':
                            page.Append(pg.FontProperty(label=param_name,name=locname,value=param['value']))
                        else:
                            page.Append(pg.StringProperty(label=param_name,name=locname,value=param['value']))
                
                    try:
                        self.prop.SetPropertyHelpString(locname,param['added_json']['Full_Comment'])
                    except:
                        self.prop.SetPropertyHelpString(locname,param['comment'])
             
        # Display a header above the grid
        self.prop.ShowHeader()
        self.prop.Refresh()

    def PopulateOnePage(self):
        #gestion des paramètres actifs
        self.prop.Clear()
        page = self.prop.AddPage("Current")

        if len(self.myparams)>0:
            for group in self.myparams.keys():
                page.Append(pg.PropertyCategory(group))

                for param_name in self.myparams[group].keys():
                    
                    param=self.myparams[group][param_name]
                    locname=group + param_name

                    if 'added_json' in param.keys():
                        list_keys = [ k for k in param['added_json']['Values'].keys()]
                        list_values = [ k for k in param['added_json']['Values'].values()]
                        page.Append(pg.EnumProperty(param_name,name=locname,labels=list_keys,values=list_values,value=int(param['value'])))
                    else:
                        if param['type']=='Integer_or_Float':
                            page.Append(pg.IntProperty(label=param_name,name=locname,value=float(param['value'])))
                        elif param['type']=='Integer':
                            page.Append(pg.IntProperty(label=param_name,name=locname,value=int(param['value'])))
                        elif param['type']=='Logical':
                            if param['value']=='.true.' or param['value']=='.True.':
                                mybool=True
                            elif param['value']=='.false.' or param['value']=='.False.':
                                mybool=False
                            page.Append(pg.BoolProperty(label=param_name,name=locname,value=mybool))
                        elif param['type']=='Float':
                            page.Append(pg.FloatProperty(label=param_name,name=locname,value=float(param['value'])))
                        elif param['type']=='File':
                            page.Append(pg.FileProperty(label=param_name,name=locname,value=param['value']))
                        elif param['type']=='Directory':
                            newobj=pg.DirProperty(locname,locname,value=param['value'])
                            newobj.SetLabel(param_name)
                            page.Append(newobj)
                        elif param['type']=='Color':
                            page.Append(pg.ColourProperty(label=param_name,name=locname,value=param['value']))
                        elif param['type']=='Fontname':
                            page.Append(pg.FontProperty(label=param_name,name=locname,value=param['value']))
                        else:
                            page.Append(pg.StringProperty(label=param_name,name=locname,value=param['value']))
                
                    if 'added_json' in param.keys():
                        self.prop.SetPropertyHelpString(locname,param['added_json']['Full_Comment'])
                    else:
                        self.prop.SetPropertyHelpString(locname,param['comment'])
                
        # Display a header above the grid
        self.prop.ShowHeader()
        self.prop.Refresh()
    
    #sauvegarde dans le fichier texte
    def SavetoFile(self,event):
        # self.ApplytoMemory(0)

        with open(self.filename, 'w') as myfile:

            for group in self.myparams.keys():
                myfile.write(' ' + group +':\n')
                for param_name in self.myparams[group].keys():
                    myfile.write(param_name +'\t' + str(self.myparams[group][param_name]['value'])+'\n')

            myfile.close()

    #relecture du fichier sur base du nom déjà connu
    def Reload(self,event):
        self.myparams.clear()
        self.myparams_default.clear()
        self.ReadFile(self.filename)
        self.Populate()

    #Transfert des données en mémoire --> remplissage des dictionnaires
    def ApplytoMemory(self,event):

        #on vide le dictionnaire des paramètres actifs
        self.myparams={}

        if self.prop.IsPageModified:
            #on boucle sur tous les paramètres du défault
            for group in self.myparams_default.keys():
                groupexists = False
                for param_name in self.myparams_default[group].keys():
                    
                    param = self.myparams_default[group][param_name]
                    curprop = self.prop.GetPropertyByName(group + param_name)
                    curdefprop = self.prop.GetPropertyByName('def' + group + param_name)
                    
                    if curprop != None :
                        if param['type']=='Integer_or_Float':
                            vpar = float(curprop.m_value)
                            vpardef = float(curdefprop.m_value)
                            if vpar != vpardef :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                self.myparams[group][param_name]['value']=vpar
                        elif param['type']=='Integer':
                            if int(curprop.m_value) != int(curdefprop.m_value) :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                self.myparams[group][param_name]['value']=int(curprop.m_value)
                        elif param['type']=='Logical':
                            if curprop.m_value != curdefprop.m_value :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                if curprop.m_value:
                                    self.myparams[group][param_name]['value']='.true.'
                                else:
                                    self.myparams[group][param_name]['value']='.false.'
                        elif param['type']=='Float':
                            #try:
                            #    vpar = float(curprop.m_value.replace('d','e'))
                            #except:
                            vpar = float(curprop.m_value)

                            #try:
                            #    vpardef = float(curdefprop.m_value.replace('d','e'))
                            #except:
                            vpardef = float(curdefprop.m_value)

                            if vpar != vpardef :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                self.myparams[group][param_name]['value']=vpar
                        elif param['type']=='File':
                            if str(curprop.m_value) != str(curdefprop.m_value) :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                self.myparams[group][param_name]['value']=str(curprop.m_value)
                        elif param['type']=='Directory':
                            if str(curprop.m_value) != str(curdefprop.m_value) :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                self.myparams[group][param_name]['value']=str(curprop.m_value)
                        else:
                            if str(curprop.m_value) != str(curdefprop.m_value) :
                                if not groupexists : 
                                    self.myparams[group]={}
                                    groupexists = True
                                self.myparams[group][param_name] = {}
                                self.myparams[group][param_name]['value']=str(curprop.m_value)

            if not self.callback is None:
                self.callback()
            self.Update_IncGroup()
            self.Update_IncParam()
        else:
            wx.MessageDialog(self,'Nothing to do!')

    def position(self,position):
        self.SetPosition(wx.Point(position[0],position[1]+50))

    def OnClose(self, event):
        if not self.callbackdestroy is None:
            self.callbackdestroy()
        
        if self.DestroyAtClosing:
            self.Destroy()
        else:
            self.Hide()
        pass

    def createDefaultFile(self):

        with open(self.filename+'.default', 'w') as myfile:

            for group in self.myparams.keys():
                myfile.write(' ' + group +':\n')
                for param_name in self.myparams[group].keys():
                    myfile.write(param_name +'\t' + str(self.myparams[group][param_name]['value'])+'\n')

            myfile.close()

    
    def get_param(self, group, name):

        try:
            element = self.myparams[group][name]["value"]
        except:
            try:
                element = self.myparams_default[group][name]["value"]
            except:
                element  = None

        return element

    # Mise à jour des groupes inctrémmentables:
    # Les groupes existants dans les paramètres courants seront sauvés dans le dicionnaire myIncGroup avec son incrément associé.
    # Tout groupe sauvé avec le même incrément sera écrasé.
    # Si le nombre associé au groupe est plus grand que désiré, tous les groupe en surplus seront sauvé dans dans le dicionnaire myIncGroup
    # mais supprimé du dictionnaire de paramètre courant.
    # S'il n'y a pas assez de groupe dans les paramètres courant, on les ajoute avec les valeurs sauvées, sinon avec des valeurs par défaut.
    # Also check the max and min values
    def Update_IncGroup(self):

        for curIncGroup in self.myIncGroup:
            refGroup = self.myIncGroup[curIncGroup]["Ref group"]
            refParam = self.myIncGroup[curIncGroup]["Ref param"]
            iterMin = self.myIncGroup[curIncGroup]["Min"]
            iterMax = self.myIncGroup[curIncGroup]["Max"]
            nbElements = self.get_param(refGroup,refParam)
            savedDict = {}
            savedDict = self.myIncGroup[curIncGroup]["Saved"]
            templateDict = self.myIncGroup[curIncGroup]["Dict"]
            if(nbElements==None):
                wx.MessageBox(_('The reference of the incrementable group does not exist!'), _('Error'), wx.OK|wx.ICON_ERROR)
            elif(nbElements>iterMax):
                nbElements = iterMax
            # elif(nbElements<iterMin):
            #     nbElements = iterMax

            for i in range(1,nbElements+1):
                curGroup = curIncGroup.replace("$n$",str(i))
                if(curGroup in self.myparams):
                    savedDict[curGroup] = {}
                    savedDict[curGroup] = self.myparams[curGroup]
                elif(curGroup in savedDict):
                    self.myparams[curGroup] = {}
                    self.myparams[curGroup] = savedDict[curGroup]
                else:
                    self.myparams[curGroup] = {}
                    self.myparams[curGroup] = templateDict.copy()
            
            for i in range(nbElements+1,iterMax+1):
                curGroup = curIncGroup.replace("$n$",str(i))
                if(curGroup in self.myparams):
                    savedDict[curGroup] = {}
                    savedDict[curGroup] = self.myparams[curGroup].copy()
                    self.myparams[curGroup] = {}
                else:
                    break


    # Mise à jour des paramètres inctrémmentables:
    # Les paramètres existants dans les paramètres courants seront sauvés dans le dicionnaire myIncParam avec son incrément associé.
    # Tout groupe sauvé avec le même incrément sera écrasé.
    # Si le nombre associé au groupe est plus grand que désiré, tous les groupe en surplus seront sauvé dans dans le dicionnaire myIncParam
    # mais supprimé du dictionnaire de paramètre courant.
    # S'il n'y a pas assez de groupe dans les paramètres courant, on les ajoute avec les valeurs sauvées, sinon avec des valeurs par défaut.
    # Also check the max and min values
    def Update_IncParam(self):

        for curIncParam in self.myIncParam:
            refGroup = self.myIncParam[curIncParam]["Group"]
            if(refGroup.find("$n$")>-1):
                nbMax = self.myIncGroup[refGroup]["Max"]
                refGroup = refGroup.replace("$n$","")
                i=1
                while(i<nbMax+1):
                    curGroup = refGroup.replace("$n$",str(i))
                    i += 1
                    if curGroup in self.myparams:
                        self.Update_OneIncParam(curIncParam, curGroup)
                    else:
                        break
            else:
                self.Update_OneIncParam(curIncParam, refGroup)

    
    def Update_OneIncParam(self, curIncParam, refGroup):
        refGroup = self.myIncParam[curIncParam]["Group"]
        refParam = self.myIncParam[curIncParam]["Ref param"]
        iterMin = self.myIncParam[curIncParam]["Min"]
        iterMax = self.myIncParam[curIncParam]["Max"]
        nbElements = self.get_param(refGroup,refParam)
        savedDict = {}
        savedDict = self.myIncParam[curIncParam]["Saved"]
        templateDict = self.myIncParam[curIncParam]["Dict"]
        if(nbElements==None):
            wx.MessageBox(_('The reference of the incrementable group does not exist!'), _('Error'), wx.OK|wx.ICON_ERROR)
        elif(nbElements>iterMax):
            nbElements = iterMax
        # elif(nbElements<iterMin):
        #     nbElements = iterMax

        for i in range(1,nbElements+1):
            curGroup = curIncParam.replace("$n$",str(i))
            if(curGroup in self.myparams):
                savedDict[curGroup] = {}
                savedDict[curGroup] = self.myparams[curGroup]
            elif(curGroup in savedDict):
                self.myparams[curGroup] = {}
                self.myparams[curGroup] = savedDict[curGroup]
            else:
                self.myparams[curGroup] = {}
                self.myparams[curGroup] = templateDict.copy()
        
        for i in range(nbElements+1,iterMax+1):
            curGroup = curIncParam.replace("$n$",str(i))
            if(curGroup in self.myparams):
                savedDict[curGroup] = {}
                savedDict[curGroup] = self.myparams[curGroup].copy()
                self.myparams[curGroup] = {}
            else:
                break



                    
    def Extract_IncrInfo(self, nameStr:str):

        iterInfo = []
        newName = ""
        posSep1 = nameStr.find("$")
        posSep2 = nameStr[posSep1:].find("$")

        # Groupe avec indice incrémentable 
        if posSep1>-1 or posSep2>-1:
            iterCode = nameStr[posSep1+1:posSep2+1]
            posSep1 = iterCode.find("(")
            posSep2 = iterCode[posSep1:].find(")")
            iterCode = iterCode[posSep1+1:posSep2+1]
            newName = nameStr.replace(iterCode,'')
            # newName = nameStr.replace(':','')
            newName = newName.strip()
            iterInfo = iterCode.split(',')
        else:
            newName = nameStr
            iterInfo = None

        return newName, iterInfo