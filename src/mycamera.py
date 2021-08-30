from jetcam.usb_camera import USBCamera
from device_check import get_device_id, get_format
import json_util as ju


class MyCamera(USBCamera):

    def __init__(self, *args, **kwargs):
        super(MyCamera, self).__init__(*args, **kwargs)


    def _gst_str(self):
        settings = ju.load()
        return settings['gst_str']