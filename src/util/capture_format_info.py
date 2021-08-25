import re

class CaptureFormatInfo:
    def __init__(self, format_info_string):
        self._index = re.search(r"Index.*: (\d+)", format_info_string)[1]
        tmp = re.search(r"Pixel Format: ('(.+)'.*)\n", format_info_string)
        self._format_fullname = tmp[1]
        self._format_name = tmp[2]
        self._format_description = re.search(r"Name.*: (.+)\n", format_info_string)[1]
        self._format_resolutions = re.findall(r"Size: Discrete (.+)x(.+)\n.*\((\d+\.\d+) fps\)\n", format_info_string)

    @property
    def index(self):
        return self._index
        
    @property
    def name(self):
        return self._format_name

    @property
    def fullname(self):
        return self._format_fullname

    @property
    def description(self):
        return self._format_description

    def resolution(self, index=None):
        if index != None:
            return self._format_resolutions[index]
        
        ret = ('0', '0', '0.')
        for res in self._format_resolutions:
            ret = self._max(res, ret)[1]
        return ret

    def _max(self, res1, res2):
        if int(float(res1[2])) > int(float(res2[2])):
            return (0, res1)
        elif int(float(res1[2])) < int(float(res2[2])):
            return (1, res2)

        if int(res1[0]) > int(res2[0]):
            return (0, res1)
        elif int(res1[0]) < int(res2[0]):
            return (1, res2)

        if int(res1[1]) > int(res2[1]):
            return (0, res1)
        elif int(res1[1]) < int(res2[1]):
            return (1, res2)

        return res1

    def __gt__(self, other):
        self_resolution = self.resolution()
        other_resolution = other.resolution()
        if self._max(self_resolution, other_resolution)[0] == 0:
            return True
        else:
            return False

    @property
    def resolutions(self):
        return self._format_resolutions
    