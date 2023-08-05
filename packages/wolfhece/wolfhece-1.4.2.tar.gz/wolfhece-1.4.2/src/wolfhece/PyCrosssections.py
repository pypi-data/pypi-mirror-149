
#import geopandas as gpd
from .PyVertexvectors import Zones, vector
from .PyVertex import wolfvertex

class crosssections:

    myprofiles:dict

    def __init__(self,myfile) -> None:
        
        f=open(myfile,'r')
        lines=f.read().splitlines()
        f.close()

        self.myprofiles={}

        lines.pop(0)
        nameprev=''
        index=0
        for curline in lines:
            vals=curline.split('\t')
            name=vals[0]

            if name!=nameprev:
                #création d'un nouveau dictionnaire
                self.myprofiles[name]={}
                curdict=self.myprofiles[name]
                curdict['index']=index
                index+=1
                curdict['cs']=vector(name=name)
                cursect:vector
                cursect=curdict['cs']

            x=float(vals[1])
            y=float(vals[2])
            type=vals[3]
            z=float(vals[4])

            curvertex=wolfvertex(x,y,z)
            cursect.add_vertex(curvertex)
            if type=='LEFT':
                curdict['left']=curvertex
            elif type=='BED':
                curdict['bed']=curvertex
            elif type=='RIGHT':
                curdict['right']=curvertex

            nameprev=name
       
        pass

    def get_min(self,whichname='',whichprofile=None):
        curvect:vector
        if whichname!='':
            curvect=self.myprofiles[whichname]['cs']
            curvert=curvect.myvertices
        elif not whichprofile is None:
            curvect=whichprofile['cs']
            curvert=curvect.myvertices
        return sorted(curvert,key=lambda x:x.z)[0]       
