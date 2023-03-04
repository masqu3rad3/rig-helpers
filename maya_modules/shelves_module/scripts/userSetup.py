from maya import cmds
import rig_helpers_setup

cmds.evalDeferred(rig_helpers_setup.add_python_path)
cmds.evalDeferred(rig_helpers_setup.load_shelves)
cmds.evalDeferred(rig_helpers_setup.load_menu)
