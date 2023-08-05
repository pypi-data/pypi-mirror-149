import sys
import numpy as np
import matplotlib.pyplot as plt
import shutil
from numpy.testing._private.utils import measure

from .PostProcessHydrology import PostProcessHydrology
from .Catchment import *
from .Comparison import *
from ..wolf_array import *
from ..PyParams import*
from . import cst_exchanges as cste
from . import constant as cst

if not '_' in __builtins__:
    import gettext
    _=gettext.gettext

class Optimisation(wx.Frame):
    
    workingDir:str
    launcherDir:list
    myParams:dict
    nbParams:int
    optiFactor:float

    launcherParam:Wolf_Param
    comparHowParam:Wolf_Param
    saParam:Wolf_Param
    optiParam:Wolf_Param

    refCatchment:Catchment


    def __init__(self, parent=None, title="", w=500, h=500):
        super(Optimisation, self).__init__(parent, title=title, size=(w,h))

        self.workingDir = ""
        self.launcherDir = []
        self.myParams = {}
        self.nbParams = 0

        self.initGUI()

    

    def initGUI(self):

        menuBar = wx.MenuBar()

        # Creation of the Menu
        fileMenu = wx.Menu()
        newClick = fileMenu.Append(wx.ID_ANY, 'New')
        self.Bind(wx.EVT_MENU, self.new, newClick)
        openClick = fileMenu.Append(wx.ID_ANY, 'Load')
        self.Bind(wx.EVT_MENU, self.load, openClick)
        updateClick = fileMenu.Append(wx.ID_ANY, 'Update')
        self.Bind(wx.EVT_MENU, self.update, updateClick)

        fileMenu.AppendSeparator()

        quitClick = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+W')
        fileMenu.Append(quitClick)
        quitClick = wx.MenuItem(fileMenu, wx.ID_EXIT, 'Quit\tCtrl+W')

        toolMenu = wx.Menu()

        initO = wx.Menu()
        initC2L = initO.Append(wx.ID_ANY, '2 layers')
        self.Bind(wx.EVT_MENU, self.init_lumped_hydro, initC2L)
        initO.Append(wx.ID_ANY, 'VHM')
        initO.Append(wx.ID_ANY, 'GR4')
        initO.Append(wx.ID_ANY, 'UH')

        toolMenu.Append(wx.ID_ANY, 'Initialisation', initO)
        applyClick = toolMenu.Append(wx.ID_ANY, 'Apply best parameters')
        self.Bind(wx.EVT_MENU, self.apply_optim, applyClick)


        visualiseClick = toolMenu.Append(wx.ID_ANY, 'Visualise best parameters')


        menuBar.Append(fileMenu, 'File')
        menuBar.Append(toolMenu, 'Tools')

        self.SetMenuBar(menuBar)

        self.SetSize((1700, 900))
        self.SetTitle("Optimisation")
        self.Centre()

    
    def quitGUI(self, event):
        self.Close()


    def new(self, event):

        self.launcherDir = ["simul_1"]
        
        # Selection of the working directory
        idir=wx.DirDialog(None,"Choose an optimisation directory")
        if idir.ShowModal() == wx.ID_CANCEL:
            print("Optimisation cancelled!")
            # sys.exit()
        self.workingDir = idir.GetPath()+"\\"
        self.launcherDir[0] = self.workingDir+self.launcherDir[0]+"\\"

        # Copy and reading of the optiParam file 
        shutil.copyfile(self.workingDir+"test_opti.param.default", self.workingDir+"test_opti.param")
        shutil.copyfile(self.workingDir+"sa.param.default", self.workingDir+"sa.param")
        shutil.copyfile(self.workingDir+"compare.how.param.default", self.workingDir+"compare.how.param")
        if not os.path.exists(self.launcherDir[0]):
            try:
                os.mkdir(self.launcherDir[0])
            except OSError:
                print ("Creation of the directory %s failed" % self.launcherDir[0])
            else:
                print ("Successfully created the directory %s" % self.launcherDir[0])
        shutil.copyfile(self.workingDir+"launcher.param.default", self.launcherDir[0]+"launcher.param")
        shutil.copyfile(self.workingDir+"launcher.param.default", self.launcherDir[0]+"launcher.param.default")
            

        # Read the main opti file
        self.optiParam = Wolf_Param(to_read=True, filename=self.workingDir+"test_opti.param",title="test_opti")
        # Update all the paths
        self.update_dir_in_params()
        # Read all the param files
        self.launcherParam = Wolf_Param(to_read=True, filename=self.launcherDir[0]+"launcher.param",title="launcher")
        self.comparHowParam = Wolf_Param(to_read=True,filename=self.workingDir+"compare.how.param",title="compare.how")
        self.saParam = Wolf_Param(to_read=True,filename=self.workingDir+"sa.param", title="sa")
        # initialise all param files according to the reference characteristics
        self.init_with_reference()


    
    def load(self, event):


        # Selection of the main 
        idir=wx.FileDialog(None,"Choose an optimatimisation file",wildcard='Fichiers param (*.param)|*.param')
        if idir.ShowModal() == wx.ID_CANCEL:
            print("Post process cancelled!")
            # sys.exit()
        fileOpti = idir.GetPath()
        self.workingDir = idir.GetDirectory() + "\\"

        # Read the main opti file
        self.optiParam = Wolf_Param(to_read=True, filename=fileOpti, title="test_opti")
        self.workingDir = self.optiParam.get_param("Optimizer","dir")
        nbcases = int(self.optiParam.get_param("Cases","nb"))
        for i in range(nbcases):
            self.launcherDir.append(self.optiParam.get_param("Cases","dir_"+str(i+1)))
        self.launcherParam = Wolf_Param(to_read=True, filename=self.launcherDir[0]+"launcher.param",title="launcher")
        self.comparHowParam = Wolf_Param(to_read=True,filename=self.workingDir+"compare.how.param",title="compare.how")
        self.saParam = Wolf_Param(to_read=True,filename=self.workingDir+"sa.param", title="sa")
        self.get_reference()

        #

        # Check if the optimisation intervals are within the simulation interval
        self.checkIntervals()


    
    
    def apply_optim(self, event):
        
        # Get the best parameters
        bestParams = self.collect_optim()

        myModel = self.refCatchment.myModel
        filePath = self.workingDir + "Subbasin_" + str(self.refCatchment.myEffSortSubBasins[0]) + "\\"
        
        myModelDict = cste.modelParamsDict[myModel]["Parameters"]

        for i in range(self.nbParams):
            myType = self.myParams[i+1]["type"]
            self.myParams[i]["value"] = bestParams[i]
            fileName = myModelDict[myType][i]["File"]
            myGroup = myModelDict[myType][i]["Group"]
            myKey = myModelDict[myType][i]["Key"]
            tmpWolf = Wolf_Param(to_read=True, filename=filePath+fileName)
            tmpWolf.myparams[myGroup][myKey]["value"] = bestParams[i]
            tmpWolf.SavetoFile(None)
            tmpWolf.OnClose(None)
            tmpWolf = None

        self.optiFactor = bestParams[-1]

    def init_lumped_hydro(self, event):

        self.optiParam.myparams["Cases"]["nb"]["value"] = 1
        self.optiParam.myparams["Optimizer"]["tuning_method"]["value"] = 2
        self.optiParam.myparams["Optimizer"]["max_nb_run"]["value"] = 30000
        self.optiParam.myparams["Comparison factors"]["nb"]["value"] = 1
        self.optiParam.myparams["Comparison factors"]["which_factor_1"]["value"] = 1

        self.comparHowParam.myparams["Comparison global characteristics"]["nb"]["value"] = 1
        self.comparHowParam.myparams["Comparison 1"]["type"]["value"] = 1
        self.comparHowParam.myparams["Comparison 1"]["nb factors"]["value"] = 1
        self.comparHowParam.myparams["Comparison 1"]["nb intervals"]["value"] = 1
        self.comparHowParam.myparams["Comparison 1"]["factor 1"]["value"] = 1
        
        self.saParam.myparams["Optimisation parameters"]["eps"]["value"] = 1.0E-03
        self.saParam.myparams["Optimisation parameters"]["rt"]["value"] = 0.1
        self.saParam.myparams["Optimisation parameters"]["ns"]["value"] = 10
        self.saParam.myparams["Optimisation parameters"]["nt"]["value"] = 10
        self.saParam.myparams["Optimisation parameters"]["neps"]["value"] = 3
        self.saParam.myparams["Optimisation parameters"]["Nombre iteration max"]["value"] = 500
        self.saParam.myparams["Optimisation parameters"]["Initial Temperature"]["value"] = 20

        self.launcherParam.myparams["Calculs"]["Type de modèle"]["value"] = 4
        self.launcherParam.myparams["Récupération des résultats"]["Nombre de bords de convergence"]["value"] = 0
        self.launcherParam.myparams["Récupération des résultats"]["Nombre de noeuds de convergence"]["value"] = 1
        self.launcherParam.myparams["Récupération des résultats"]["extract_exchange_zone"]["value"] = 0
        self.launcherParam.myparams["Récupération des résultats"]["type_of_geom"]["value"] = 2
        self.launcherParam.myparams["Récupération des résultats"]["type_of_exchange"]["value"] = 15
        self.launcherParam.myparams["Récupération des résultats"]["type_of_data"]["value"] = 13
        
        if(self.refCatchment.myModel==cst.tom_2layers_linIF):
            self.init_2layers_linIF()

        self.optiParam.SavetoFile(None)
        self.optiParam.Reload(None)

        self.comparHowParam.SavetoFile(None)
        self.comparHowParam.Reload(None)

        self.saParam.SavetoFile(None)
        self.saParam.Reload(None)

        self.launcherParam.SavetoFile(None)
        self.launcherParam.Reload(None)


    def init_2layers_linIF(self):

        self.saParam.myparams["Initial parameters"]["Read initial parameters?"]["value"] = 0

        # Retrieve the dictionnary with the properties of all models (parameters, files, etc)
        myModel = self.refCatchment.myModel
        nbParams = cste.modelParamsDict[myModel]["Nb"]
        myModelDict = cste.modelParamsDict[myModel]["Parameters"]

        prefix1 = "param_"
        i=1
        for element in myModelDict:
            paramName = prefix1 + str(i)
            self.launcherParam.myparams[paramName]={}
            self.launcherParam.myparams[paramName]["type_of_data"] = {}
            self.launcherParam.myparams[paramName]["type_of_data"]["value"] = element
            i+=1

        self.launcherParam.myparams["Paramètres à varier"]["Nombre de paramètres à varier"]["value"] = nbParams
        self.nbParams = nbParams
        self.saParam.callback = self.update_parameters_SA
        prefix2 = "Parameter "
        for i in range(1,self.nbParams+1):
            paramName = prefix2 + str(i)
            self.saParam.myparams["Lowest values"][paramName] = {}
            self.saParam.myparams["Highest values"][paramName] = {}
            self.saParam.myparams["Steps"][paramName] = {}
            self.saParam.myparams["Initial parameters"][paramName] = {}
            self.saParam.myparams["Lowest values"][paramName]["value"] = 0.0
            self.saParam.myparams["Highest values"][paramName]["value"] = 0.0
            self.saParam.myparams["Steps"][paramName]["value"] = 0.0
            self.saParam.myparams["Initial parameters"][paramName]["value"] = 0.0
            paramName = prefix1 + str(i)
            self.launcherParam.myparams[paramName]["geom_filename"] = {}
            self.launcherParam.myparams[paramName]["geom_filename"]["value"] = "my_geom.txt"
            self.launcherParam.myparams[paramName]["type_of_geom"] = {}
            self.launcherParam.myparams[paramName]["type_of_geom"]["value"] = 0
            self.launcherParam.myparams[paramName]["type_of_exchange"] = {}
            self.launcherParam.myparams[paramName]["type_of_exchange"]["value"] = -3



    def init_myParams(self):

        self.nbParams = self.launcherParam.get_param("Paramètres à varier", "Nombre de paramètres à varier")

        for i in range(1,self.nbParams+1):
            curParam = "param_" + str(i)
            self.myParams[i] = {}
            self.myParams[i]["type"] = self.launcherParam.get_param(curParam, "type_of_data")
            self.myParams[i]["value"] = 0.0
            


    
    def collect_optim(self):
        
        nameTMP = self.optiParam.get_param("Optimizer","fname")
        optimFile = self.workingDir + nameTMP+".rpt"

        with open(optimFile, newline = '') as fileID:                                                                                          
            data_reader = csv.reader(fileID, delimiter=' ',skipinitialspace=True)
            list_data = []
            for raw in data_reader:
                if(len(raw)>1):
                    if raw[0]+" "+raw[1]=="Best run":
                        list_data.append(raw[3:-1])
        matrixData = np.array(list_data[0]).astype("float")

        return matrixData



    def init_with_reference(self, idLaucher=0):

        # Selection of the working directory
        idir=wx.FileDialog(None,"Choose a reference file",wildcard='Fichiers post-processing (*.postPro)|*.postPro')
        if idir.ShowModal() == wx.ID_CANCEL:
            print("Post process cancelled!")
            # sys.exit()
        refFileName = idir.GetPath()
        refDir = idir.GetDirectory() + "\\"
        myPostPro = PostProcessHydrology(postProFile=refFileName)

        # Recover the Catchment object
        self.refCatchment = myPostPro.myCatchments["Catchment 1"]['Object']
        self.launcherParam.myparams["Calculs"]["Répertoire simulation de référence"]["value"] = self.refCatchment.workingDir

        # Create an empty geom.txt file
        geomName = self.launcherParam.get_param("Récupération des résultats","geom_filename")
        open(self.launcherDir[idLaucher]+geomName, mode='a').close()

        # Complete the default model parameters



        # Complete compare.how file
        dateTmp = self.refCatchment.paramsInput.myparams["Temporal Parameters"]["Start date time"]["value"]
        self.comparHowParam.myparams["Comparison 1"]["date begin 1"]["value"] = dateTmp
        dateTmp = self.refCatchment.paramsInput.myparams["Temporal Parameters"]["End date time"]["value"]
        self.comparHowParam.myparams["Comparison 1"]["date end 1"]["value"] = dateTmp

        # update param files
        self.launcherParam.SavetoFile(None)
        self.launcherParam.Reload(None)
        self.comparHowParam.SavetoFile(None)
        self.comparHowParam.Reload(None)
    

    def get_reference(self, refFile="", idLaucher=0):
        if(refFile==""):
            defaultDir = self.launcherParam.get_param("Calculs","Répertoire simulation de référence")
            idir=wx.FileDialog(None,"Choose a reference file",wildcard='Fichiers post-processing (*.postPro)|*.postPro')
            if idir.ShowModal() == wx.ID_CANCEL:
                print("Post process cancelled!")
                # sys.exit()
            refFileName = idir.GetPath()

        myPostPro = PostProcessHydrology(postProFile=refFileName)
        # Recover the Catchment object
        self.refCatchment = myPostPro.myCatchments["Catchment 1"]['Object']

        self.launcherParam.myparams["Calculs"]["Répertoire simulation de référence"]["value"] = self.refCatchment.workingDir

        # Create an empty geom.txt file
        geomName = self.launcherParam.get_param("Récupération des résultats","geom_filename")
        open(self.launcherDir[idLaucher]+geomName, mode='a').close()
        
        # update param files
        self.launcherParam.SavetoFile(None)
        self.launcherParam.Reload(None)




    def update_dir_in_params(self):
        
        self.optiParam.myparams["Optimizer"]["dir"]["value"] = self.workingDir
        self.optiParam.myparams["Cases"]["dir_1"]["value"] = self.launcherDir[0]
        self.optiParam.myparams["Predefined parameters"]["fname"]["value"] = self.workingDir+"param.what"
        self.optiParam.SavetoFile(None)
        self.optiParam.Reload(None)



    def checkIntervals(self):
        
        print("So far do nothing!")
        # self.comparHowParam[]


    def update_parameters_SA(self):

        for element in self.saParam.myIncParam:
            curParam = self.saParam.myIncParam[element]
            if not  "Ref param" in curParam:
                curGroup = curParam["Ref param"]
                savedDict = self.myIncParam[curGroup]["Saved"]
                for i in range(1,self.nbParams+1):
                    curGroup = curParam.replace("$n$",str(i))
                    if(curGroup in self.saParam.myparams):
                        savedDict[curGroup] = {}
                        savedDict[curGroup] = self.saParam.myparams[curGroup]
                    elif(curGroup in savedDict):
                        self.saParam.myparams[curGroup] = {}
                        self.saParam.myparams[curGroup] = savedDict[curGroup]
                    else:
                        self.saParam.myparams[curGroup] = {}
                        self.saParam.myparams[curGroup] = templateDict.copy()
                # self.saParam.myparams[]


    def update(self, event):

        print("TO DO")


    
    