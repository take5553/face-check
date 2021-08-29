from jetcam.usb_camera import USBCamera
from device_check import get_device_id, get_format
import json_util as ju


class MyCamera(USBCamera):

    def __init__(self, *args, **kwargs):
        super(MyCamera, self).__init__(*args, **kwargs)


    def _gst_str(self):
        self._settings = ju.load()
        cap_device = get_device_id(self._settings['camera_mode'])[0]
        cap_orig_width = self._settings['cap_settings']['cap_width']
        cap_orig_height = self._settings['cap_settings']['cap_height']
        cap_fps = self._settings['cap_settings']['cap_fps']
        
        if self._settings['camera_mode'] == 'usb':
            if self._settings['cap_settings']['cap_mode'] == 'MJPG':
                crop_height = int((cap_orig_width - self._settings['canvas_settings']['canvas_height']) / 2)
                crop_width = int((cap_orig_height- self._settings['canvas_settings']['canvas_width']) / 2)
                string = 'v4l2src device=/dev/video{} '.format(cap_device) \
                    + '! image/jpeg,width=(int){},height=(int){},framerate=(fraction){}/1 '.format(cap_orig_width, cap_orig_height, cap_fps) \
                    + '! jpegdec ' \
                    + '! videoflip method=upper-left-diagonal ' \
                    + '! videocrop top={} bottom={} left={} right={} '.format(crop_height, crop_height, crop_width, crop_width) \
                    + '! videoconvert ! video/x-raw,format=(string)BGR ' \
                    + '! appsink'
        elif self._settings['camera_mode'] == 'csi':
            crop_top = int((cap_orig_height - self._settings['canvas_settings']['canvas_height']) / 2)
            if crop_top < 0:
                crop_top = 0
            crop_bottom = cap_orig_height - crop_top
            crop_left = int((cap_orig_width - self._settings['canvas_settings']['canvas_width']) / 2)
            if crop_left < 0:
                crop_left = 0
            crop_right = cap_orig_width - crop_left
            string = 'nvarguscamerasrc sensor-id={} '.format(cap_device) \
                + '! video/x-raw(memory:NVMM), width={}, height={}, format=(string)NV12 '.format(cap_orig_width, cap_orig_height) \
                + '! nvvidconv flip-method=6 left={} right={} top={} bottom={} '.format(crop_left, crop_right, crop_top, crop_bottom) \
                + '! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx '.format(self._settings['canvas_settings']['canvas_width'], self._settings['canvas_settings']['canvas_height']) \
                + '! videoconvert ' \
                + '! appsink'
        print('video format: ' + string)
        return string