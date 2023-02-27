"""Locator related helper functions"""

from maya import cmds

def locate(objects=None, constraint=False):
    """Create locators matching the pivot point of selected object"""
    objects = objects or cmds.ls(sl=True, type="transform")
    if not isinstance(objects, (tuple, list)):
        objects = [objects]
    locator_list = []
    for obj in objects:
        _locator = cmds.spaceLocator(name="locate")[0] # I don't worry about the name
        if constraint:
            cmds.parentConstraint(obj, _locator, maintainOffset=False)
        else:
            cmds.matchTransform(_locator, obj)
        locator_list.append(_locator)
    return locator_list