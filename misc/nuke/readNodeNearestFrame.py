import nuke

nodes = nuke.allNodes()

for node in nodes:
    if node.Class() == "Read":
        node['on_error'].setValue('nearest frame')