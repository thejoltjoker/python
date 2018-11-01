import nuke

def readNodeNearestFrame():
	nodes = nuke.allNodes()

	for node in nodes:
	    if node.Class() == "Read":
	        node['on_error'].setValue('nearest frame')


def reloadAllRead():
	nodes = nuke.allNodes()

	for node in nodes:
		if node.Class() == "Read":
			node.knob("reload").execute()