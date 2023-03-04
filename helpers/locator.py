"""Locator related helper functions"""

from maya import cmds

from trigger.library.naming import unique_name

def locate(objects=None, constraint=False):
    """Create locators matching the pivot point of selected object"""
    objects = objects or cmds.ls(selection=True, type="transform")
    if not isinstance(objects, (tuple, list)):
        objects = [objects]
    locator_list = []
    for obj in objects:
        _locator = cmds.spaceLocator(name=unique_name("locate"))[0]
        if constraint:
            cmds.parentConstraint(obj, _locator, maintainOffset=False)
        else:
            cmds.matchTransform(_locator, obj)
        locator_list.append(_locator)
    return locator_list