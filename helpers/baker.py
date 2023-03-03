"""Generic Baking Tool"""

import logging

from maya import cmds


LOG = logging.getLogger(__name__)


def get_active_range():
    range_min = int(cmds.playbackOptions(q=True, min=True))
    range_max = int(cmds.playbackOptions(q=True, max=True))
    return [range_min, range_max]

def validate_node(node):
    if not cmds.objExists(node):
        msg = "Destination node {} does not exist.".format(node)
        LOG.error(msg)
        raise Exception(msg)


def bake(
    source_node,
    destination_node=None,
    use_namespace=True,
    namespace=None,
    frame_range=None,
    attributes=None,
):
    if use_namespace:
        if not namespace:
            selection = cmds.ls(sl=True)
            if not selection:
                msg = "Nothing selected. Namepace cannot defined"
                LOG.error(msg)
                raise Exception(msg)
            else:
                namespace = cmds.ls(sl=True)[0].rpartition(":")[0]
        source_node = "{}:{}".format(namespace, source_node)
        validate_node(source_node)
        _name = namespace
    else:
        _name = ""

    if not destination_node:
        destination_node = cmds.spaceLocator(
            name="{}_baked_data".format(_name)
        )
    else:
        validate_node(destination_node)

    frame_range = frame_range or get_active_range()

    # default channels are rotation only
    attributes = attributes or ["rx", "ry", "rz"]

    for frame in range(frame_range[0], frame_range[1] + 1):
        cmds.currentTime(frame)
        for attr in attributes:
            val = cmds.getAttr("{}.{}".format(source_node, attr))
            cmds.setKeyframe(destination_node, attribute=attr, v=val)
