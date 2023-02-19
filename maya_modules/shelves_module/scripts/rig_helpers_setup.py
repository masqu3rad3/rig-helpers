import os, sys
from maya import cmds
from maya import mel

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir))
SHELF_DIR = os.path.join(parent_dir, "shelves")

if not os.path.exists(SHELF_DIR):
    print('\n\n WARNING \n\n')


def add_python_path():
    """adds the python path to during launch"""
    maya_modules_path = os.path.abspath(os.path.join(parent_dir, os.pardir))
    rigging_path = os.path.abspath(os.path.join(maya_modules_path, os.pardir))
    if rigging_path not in sys.path:
        sys.path.append(rigging_path)
    print("%s added to the python path" % rigging_path)


def load_shelves(reset=False):
    """
    Loads all shelves under SHELF_DIR.
    Args:
        reset: (Bool) if True, deletes the existing shelves and re-creates them

    Returns: None

    """
    if os.path.isdir(SHELF_DIR) and not cmds.about(batch=True):
        for s in os.listdir(SHELF_DIR):
            path = os.path.join(SHELF_DIR, s).replace('\\', '/')
            if not os.path.isfile(path): continue
            name = os.path.splitext(s)[0].replace('shelf_', '')
            # Delete existing shelf before loading
            if cmds.shelfLayout(name, exists=True):
                if reset:
                    cmds.deleteUI(name)
                    mel.eval('loadNewShelf("{}")'.format(path))
            else:
                mel.eval('loadNewShelf("{}")'.format(path))


