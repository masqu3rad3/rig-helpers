import os
import sys
from maya import cmds
from maya import mel

dir_path = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.abspath(os.path.join(dir_path, os.pardir)) # shelves_module dir
SHELF_DIR = os.path.join(parent_dir, "shelves")

if not os.path.exists(SHELF_DIR):
    print('\n\n WARNING - Rig Helpers Source shelf path does not exist \n\n')


def add_python_path():
    """Add the python paths to during launch."""
    maya_modules_path = os.path.abspath(os.path.join(parent_dir, os.pardir))
    rigging_path = os.path.abspath(os.path.join(maya_modules_path, os.pardir))
    studiolibrary_path = os.path.join(rigging_path, "studiolibrary", "src")
    if rigging_path not in sys.path:
        sys.path.append(rigging_path)
        print("%s added to the python path" % rigging_path)
    if studiolibrary_path not in sys.path:
        sys.path.insert(0, studiolibrary_path)
        print("%s added to the python path" % studiolibrary_path)


def load_shelves(reset=False):
    """
    Load all shelves under SHELF_DIR.
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

def load_menu():
    """Load the menu items for the rig helpers module."""

    # add a separator
    # cmds.menuItem(divider=True)
    recreate_command = "rig_helpers_setup.load_shelves(reset=True)"
    add_to_menu("RigHelpers", "Re-create Shelves", recreate_command)

def add_to_menu(menu, menu_item, command):
    """Add an item to a menu.
    This is a generic method
    """

    main_window = mel.eval('$tmpVar=$gMainWindow')
    menu_widget = '%s_widget' % menu

    # dont create another menu if already exists
    if cmds.menu(menu_widget, label=menu, exists=True, parent=main_window):
        trigger_menu = '%s|%s' % (main_window, menu_widget)
    else:
        trigger_menu = cmds.menu(menu_widget, label=menu, parent=main_window, tearOff=True)

    # skip the process if the menu_item exists
    item_array = cmds.menu(menu_widget, query=True, itemArray=True)
    if item_array:
        for item in item_array:
            label = cmds.menuItem(item, query=True, label=True)
            if label == menu_item:
                return

    cmds.menuItem(label=menu_item, command=command)

