import maya.cmds as cmds
import maya.mel as mel
import sys
import os
import pymel.core as pm

from Analog_Tools.Analog_Save import *
from Analog_Tools import *

from PySide import QtCore, QtGui

# Import scripts
import Analog_Save_Maya
import Analog_Cache_Maya
import Analog_IncrementalSave_v1_0 as Analog_IncrementalSave
import Analog_CreateElements_v0_5 as Analog_CreateElements
import Analog_MayaScripts_v0_1 as Analog_MayaScripts

# Most practical, keeps the parent module so you know where it came from
import MGTools
from MGTools import rigMain, launcher, shaders, pasteBoard
from MGTools.rigMain import *
from MGTools.shaders import *
from MGTools.launcher import *
from MGTools.pasteBoard import *

# COSMOS
try: import cosmos.core.startup as cosmos
except: print "Problem loading cosmos: {}".format(str(IOError))

# Rivet Script
import gf_multiRivet as mrvt

# Check what maya version 
from pymel import versions
print versions.current()

print '============ Running //pixstor/AppData/Analog_Maya/pyscripts/userSetup.py ============'


# Events
def SetProject():
    # Get maya scene file path
    ScenePath = cmds.file(q=True, sceneName=True)
    # Make a ProjectFileObject from analog functions
    FileObject = An_FileClasses.AnProjectFile(ScenePath)

    # Check if a good result was returned
    if not FileObject.Valid:
        return 'Analog: No valid project found'
        
    # Call the method to get the project path
    print FileObject.ProjectPath()
    print 'Analog: Setting project to ' + FileObject.ProjectPath()

    # Set the workspace/project
    cmds.workspace(FileObject.ProjectPath(), o=True)

# def PipeGetComments(self):
#     import Analog_Tools.Analog_Pipe.Functions
#     print 'Analog: Getting comments'
#     Analog_Tools.Analog_Pipe.Functions.GetCommentsFromFile(pm.sceneName())


def OnSceneOpen():
    SetProject()
    # PipeGetComments('')


# Set project when openning a scene
cmds.scriptJob( e=['SceneOpened', 'OnSceneOpen()'])

# scriptJob -event SceneOpened "myTestProc";


# this replaces everything in file menu !
# cmds.evalDeferred(AddToFileMenu)

# Menu item executes
def AnalogSave_Execute(self):
    Analog_Save_Maya.AnalogSave()

def Analog_IncrementalSave_Execute(context):
    Analog_IncrementalSave.IncrementalSave()
    
def AnalogCacheExport_Execute(context):
    # reload(Analog_Cache_Maya)
    Analog_Cache_Maya.AnalogExportAbc()
    
def AnalogCacheImport_Execute(context):
    # reload(Analog_Cache_Maya)
    Analog_Cache_Maya.AnalogImportAbc()
    
# Create elemtns
def Analog_CreateBeautyElements_Execute(self):
    Analog_CreateElements.CreateBeautyElements()
    
def Analog_CreateUtilRenderLayer_Execute(self):
    reload(Analog_CreateElements)
    Analog_CreateElements.CreateUtilRenderLayer()
    
def Analog_CreateIDElements_Execute(self):
    Analog_CreateElements.CreateIDElements()

# Analog_MayaScripts
def SetCameraGate_Execute(self):
    Analog_MayaScripts.SetCameraGate()
 
# Deadline commands just call their Mel command
def SubmitToDeadline_Execute(self):
    # Evaluate a mel command
    print 'SubmitToDeadline_Execute()'
    mel.eval('SubmitJobToDeadline;')

# DBR is Python
def SubmitDeadlineDBR_Execute(self):
    # Evaluate a mel command
    # mel.eval('SubmitMayaVRayDBRToDeadline;')
    
    # Python
    import SubmitMayaVRayDBRToDeadline
    SubmitMayaVRayDBRToDeadline.SubmitToDeadline()
    


def COSMOS_Execute(context):
    cosmos.start()    
def MGTools_Execute(context):
    MGTools.launcher.main(os.environ['ANALOG_APPDATA'] + '/Analog_Maya/icons/')

def MGCopy(context):
    path = os.environ['ANALOG_TOOLS'] + '/Analog_Paste/'
    #Copy
    selection = cmds.ls(sl=True)
    if (len(selection) >= 1):
        cmds.file((path + "MayaPaste.ma"),force=True,type="mayaAscii",es=True,pr=True)
        mel.eval('inViewMessage -smg "Copied" -pos topRight -bkc 0x00000000 -fade;')
        print (path + "MayaPaste")
    else:
        mel.eval('inViewMessage -smg "No object selected" -pos topRight -bkc 0x00000000 -fade;')

def MGPaste(context):
    path = os.environ['ANALOG_TOOLS'] + '/Analog_Paste/'
    #Paste
    print path
    cmds.file((path + "MayaPaste.ma"), i=True)

def SetVRaySettings(self):
    VRaySettingsNode = pm.ls(type='VRaySettingsNode')[0]

    # Cant find the node, easy way instead
    cmds.setAttr('defaultRenderGlobals.animation', 1)
    VRaySettingsNode.dontSaveImage.set(1)
    VRaySettingsNode.animBatchOnly.set(1)
    VRaySettingsNode.globopt_cache_geom_plugins.set(1)
    VRaySettingsNode.globopt_light_doHiddenLights.set(0)
    VRaySettingsNode.globopt_geom_doHidden.set(0)
    VRaySettingsNode.globopt_light_doDefaultLights.set(0)
    VRaySettingsNode.globopt_mtl_filterMaps.set(0)
    VRaySettingsNode.dmcMaxSubdivs.set(50)
    # VRaySettingsNode.giOn.set(1)
    VRaySettingsNode.primaryEngine.set(2)
    VRaySettingsNode.sys_embreeUse.set(1)
    VRaySettingsNode.sys_regsgen_xc.set(32)
    VRaySettingsNode.sys_progress_increment.set(1)
    VRaySettingsNode.samplerType.set(1)

# Select all GEO objects inside selected group
def SelectMeshesInGroup(self):
    RootGroup = cmds.ls(selection=True)

    # Always use fullPath=True to avoid short name conflict errors
    ChildMeshShapes = maya.cmds.listRelatives(RootGroup, allDescendents=True, noIntermediate=True, fullPath=True, type='mesh')

    # These are the SHAPE nodes of the child meshes, really we want to select THEIR transforms (their parent)
    ChildMeshes = maya.cmds.listRelatives(ChildMeshShapes, fullPath=True, parent=True)
    
    # Select meshes
    cmds.select( ChildMeshes, replace=True )

# Move all meshes to selected group
def MoveChildMeshesToSelected(self):
    RootGroup = cmds.ls(selection=True)

    # Always use fullPath=True to avoid short name conflict errors
    ChildMeshes = maya.cmds.listRelatives(RootGroup, allDescendents=True, noIntermediate=True, fullPath=True, type="mesh")

    # Parent the meshes to the selected root group
    for Mesh in ChildMeshes:
        cmds.parent( Mesh, RootGroup)
    

    
################################################
# Build 'Analog' menu
def AddAnalogMenu():
    
    # MainWindow = pm.getMelGlobal('string', 'gMainWindow')
    # this returns as 'MayaWindow' which is what we want to use

    AnalogMenu = pm.menu( label='Analog', parent = 'MayaWindow')
    pm.menuItem( parent=AnalogMenu, label='Analog Save', command=AnalogSave_Execute )
    pm.menuItem( parent=AnalogMenu, label='Analog Incremental Save', command=Analog_IncrementalSave_Execute )
    
 
    pm.menuItem( parent = AnalogMenu, divider=True)         
    pm.menuItem( parent = AnalogMenu, label='Analog Cache Import', command = AnalogCacheImport_Execute )
    pm.menuItem( parent = AnalogMenu, label='Analog Cache Export', command = AnalogCacheExport_Execute )

    
    cmds.menuItem( parent = AnalogMenu, divider=True)
    
    # pm.menuItem( parent = AnalogMenu, label='Pipe Get Comments', command = PipeGetComments )
    
    cmds.menuItem( parent = AnalogMenu, divider=True)
    
    pm.menuItem( parent = AnalogMenu, label='Submit to Deadline', command = SubmitToDeadline_Execute )
    pm.menuItem( parent = AnalogMenu, label='Deadline DBR', command = SubmitDeadlineDBR_Execute )
    
    cmds.menuItem( parent = AnalogMenu, divider=True)
    
    #pm.menuItem( parent = AnalogMenu, label='MG Tools', command = MGTools_Execute , i=("R:/Analog_Maya/icons/tools_icon.png"))
    pm.menuItem( parent = AnalogMenu, label='MG Copy', command = ('pasteboardCopy()') ,i="copyUV.png")
    pm.menuItem( parent = AnalogMenu, label='MG Paste', command = ('pasteboardPaste()') , i="pasteU.png")
    pm.menuItem( parent = AnalogMenu, label='MG Paste-Board', command = ('pasteboardUi()') , i="layoutUV.png")
    pm.menuItem( parent = AnalogMenu, label='COSMOS', command = COSMOS_Execute , i=(os.environ['ANALOG_APPDATA'] + '/Analog_Maya/icons/cosmos.png'))
  
    cmds.menuItem( parent = AnalogMenu, divider=True)
    
    pm.menuItem( parent = AnalogMenu, label='SR Select Meshes in Group', command = SelectMeshesInGroup )
    pm.menuItem( parent = AnalogMenu, label='SR Move Meshes to root Group', command = MoveChildMeshesToSelected )
    pm.menuItem( parent = AnalogMenu, label='SR Set Camera Gate', command = SetCameraGate_Execute )
        
    cmds.menuItem( parent = AnalogMenu, divider=True)

    pm.menuItem( parent = AnalogMenu, label='Analog SetVRaySettings', command = SetVRaySettings )
    
    cmds.menuItem( parent = AnalogMenu, divider=True)
    
    pm.menuItem( parent = AnalogMenu, label='Analog Create Beauty Elements', command = Analog_CreateBeautyElements_Execute )
    pm.menuItem( parent = AnalogMenu, label='Analog Create Util RL', command = Analog_CreateUtilRenderLayer_Execute )
    pm.menuItem( parent = AnalogMenu, label='Analog Create ID Elemnts', command = Analog_CreateIDElements_Execute )
    

    
# Add to the built-in 'File' menu
def AddToFileMenu():
    FileMenu = pm.getMelGlobal('string', 'gMainFileMenu')
    pm.menuItem( parent = FileMenu, label='Analog Save', command = AnalogSave_Execute )
    pm.menuItem( parent = FileMenu, label='Analog Incremental Save', command = Analog_IncrementalSave_Execute )

    
    
    
#This command is to open up a port that can be used to tallk to another computer in the network, 
#renamed now to reflect better what it does 
def openLocalPort():
    print 'openLocalPort() in usersetup.py'
    import maya.cmds as cmds
    import socket
    #Code for other machine
    try: cmds.commandPort(n=":7890")
    except: randomValue = 0

    #Get lockal
    ip = socket.gethostbyname(socket.gethostname())
    print ip

    #parse
    try: 
        cmds.commandPort(n=":7890") 
        cmds.commandPort(n=(ip + ":7890"))
        print "Value 7890"
    except:
        try: 
            cmds.commandPort(n=":7891") 
            cmds.commandPort(n=(ip + ":7891"))
            print "Value 7891"
        except:
            print "Loaded succesfully..."
    
    

    
# Wait until maya is idle, everything has loaded, then run custom stuff
cmds.evalDeferred(AddAnalogMenu)