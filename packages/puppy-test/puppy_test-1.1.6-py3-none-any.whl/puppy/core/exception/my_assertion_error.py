from ..function.track.xml_track import xmlTrack
from ..function.beautify.fold import Fold


class MyAssertionError(object):

    @staticmethod
    def raise_error(msg):
        file_path, row = xmlTrack.current_path_row()
        msg = '''\n  File "{}", line {}\n    raise\nAssertionError:{}'''.format(file_path, row, msg)
        msg = Fold.fold_text(msg)
        raise AssertionError(msg)
