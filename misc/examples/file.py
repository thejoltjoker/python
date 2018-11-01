import sys, os

from Analog_Tools import Analog_Save, Analog_Functions, Analog_Structure
from Analog_Tools.Analog_Save import Main
from Analog_Tools import An_FileClasses

from PySide import QtCore, QtGui

# Maya
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

def AnalogSave():
    # Grab and instance already open (nuke/maya?)
    app = QtGui.QApplication.instance()

    # Create the Qt Application
    if app is None:
        app = QtGui.QApplication(sys.argv)


    # Get current scene path
    ScenePath = cmds.file(q=True, sceneName=True)

    if ScenePath:
        print ScenePath

    if Analog_Functions.GetUser() == 'sreeves':
        TestProjects = True
    else:
        TestProjects = False

    # Create (an instance of the class) and show the form
    oForm = Analog_Save.Main.MainWindow("Maya", ScenePath, Verbose=True, TestProjects=TestProjects)


    # exec_() is nodal rather than show()
    # if checks if it returns 1 or 0 and if so to cancel or accept the dialogs return
    if oForm.exec_():
        AnalogSaveOutputPath = oForm.GetOutput()

        OutputPath = AnalogSaveOutputPath[0] + '.mb'


        # Check if file exists
        if os.path.isfile(OutputPath):

            # Ask if user wants to overwrite
            oOverwrite = OverwriteFile()
            if oOverwrite:
                Save(OutputPath, AnalogSaveOutputPath)

        # If it doesnt not exits, save
        else:
            Save(OutputPath, AnalogSaveOutputPath)


def OverwriteFile():
    # Make a message box object
    MsgBox = QtGui.QMessageBox()

    # Set some properties
    MsgBox.setText('A file already exists')
    MsgBox.setInformativeText("Do you want to overwrite the file?")
    MsgBox.setStandardButtons(QtGui.QMessageBox.Save | QtGui.QMessageBox.Cancel)
    MsgBox.setDefaultButton(QtGui.QMessageBox.Cancel)

    # Execute the messagebox and return the resilt
    Result = MsgBox.exec_()

    # Do something with the return
    if Result == QtGui.QMessageBox.Save:
        Save = True
    else:
        Save = False

    return Save

def Save(OutputPath, AnalogSaveOutput):

    # Set lots of settings
    MayaCommands(AnalogSaveOutput)

    # Maya Save command
    pm.saveAs(OutputPath)
    print 'Saving to ' + OutputPath

    # Add file to recent files
    mel.eval ('string $newFileName = `file -q -sn`')
    mel.eval('string $format = `fileExtension $newFileName`')
    mel.eval ('if ($format == "mb") {addRecentFile($newFileName, "mayaBinary");}')
    mel.eval ('if ($format == "ma") {addRecentFile($newFileName, "mayaAscii");}')

def MayaCommands(AnalogSaveOutput):

    # Load Vray - if already loaded it skips
    cmds.loadPlugin( 'vrayformaya.mll' )

    # check for no vray

    # Check if vray settings exist, if not create so that attribute can be edited
    if not cmds.objExists('vraySettings'):
        # Selecting the node causes an error to popup
        cmds.createNode('VRaySettingsNode', name='vraySettings', skipSelect = True)

    # Change renderer to vray
    cmds.setAttr('defaultRenderGlobals.ren', 'vray', type='string')


    # Set the render output file path
    oScenePath = AnalogSaveOutput[0]


    # Get maya scene file path from analogsaveoutput
    SaveScenePath = oScenePath + '.mb'

    # Make a ProjectFileObject from analog functions
    FileObject = An_FileClasses.AnProjectFile(SaveScenePath)

    # Get render PATH from Object
    # Need to remove the project from this path so it starts with 2D_PRODUCTION
    RenderDir = FileObject.GetRenderPath().replace(FileObject.ProjectPath(),'')

    # Tokens - possibly non-maya specific
    TokenScene = '<scene>'
    TokenPass = '<layer>'

    RenderFile = TokenScene + '/' + TokenScene + '_' + TokenPass

    print 'RenderDir: ' + RenderDir
    print 'RenderFile: ' + RenderFile

    # Set output path
    cmds.setAttr('vraySettings.fileNamePrefix', RenderDir + '/' + RenderFile , type='string')

    # Set Output as EXR
    cmds.setAttr('vraySettings.imageFormatStr', 'exr', type = 'string')

    # Set the workspace/project
    cmds.workspace (FileObject.ProjectPath(), o=True)




    # Wishlist
    # set resolution, from pipe?
    #cmds.setAttr("vraySettings.width",  width)
    #cmds.setAttr("vraySettings.height",  height)
    # fps, from pipe?


    # print cmds.getAttr('vraySettings.imageFormatStr')



