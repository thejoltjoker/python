# V!ctor GUI Customization
# Copyright (c) 2016 Victor Perez. All Rights Reserved.

# Import Python Files
import customTools

# Nuke Menu Definitions
customToolsMenu = nuke.menu('Nuke').addMenu('Custom Tools')
customToolsMenu.addCommand('Reload all read nodes', 'reloadAllRead()')
customToolsMenu.addCommand('Set all read nodes to nearest frame', 'readNodeNearestFrame()')
# menu.addCommand('Convert Gizmo to Group', 'V_ConvertGizmosToGroups.convertGizmosToGroups()', 'ctrl+shift+h')

# V!ctor Tools Toolbar Definitions
# toolbar = nuke.menu('Nodes')
# VMenu = toolbar.addMenu('V!ctor', icon='V_Victor.png')
# VMenu.addCommand('V_CheckMatte', 'nuke.createNode("V_CheckMatte")', icon='V_CheckMatte.png')
# VMenu.addCommand('V_IdBuilder', 'nuke.createNode("V_IdBuilder")', icon='V_IdBuilder.png')
# VMenu.addCommand('V_IdPackage', 'nuke.createNode("V_IdPackage")', icon='V_IdPackage.png')
# VMenu.addCommand('V_IdFilter', 'nuke.createNode("V_IdFilter")', icon='V_IdFilter.png')
# VMenu.addCommand('V_EdgeMatte', 'nuke.createNode("V_EdgeMatte")', icon='V_EdgeMatte.png')
# VMenu.addCommand('V_Multilabeler', 'nuke.createNode("V_Multilabeler")', icon='V_Multilabeler.png')