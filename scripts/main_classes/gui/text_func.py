from logging import error

from direct.gui.DirectFrame import DirectFrame
from panda3d.core import Vec3


def center_text(frame:DirectFrame, displacement_vec:Vec3=Vec3(0, 0, 0)):
    try:
        text  = frame.component('text0')
    except KeyError:
        error('text not found')
        return

    min_pt, max_pt = text.getTightBounds()

    x, z = frame['text_pos']

    frame['text_pos'] = (x + displacement_vec.x, z - (max_pt.z + min_pt.z) * 0.5 + displacement_vec.z)
