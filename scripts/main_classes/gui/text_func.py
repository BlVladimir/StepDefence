from logging import error

from direct.gui.DirectFrame import DirectFrame


def center_text(frame:DirectFrame):
    try:
        text  = frame.component('text0')
    except KeyError:
        error('text not found')
        return

    min_pt, max_pt = text.getTightBounds()

    x, z = frame['text_pos']
    frame['text_pos'] = (x, z-(max_pt.z+min_pt.z)/2)
