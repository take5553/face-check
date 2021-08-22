from jetcam.usb_camera import USBCamera
from device_check import get_device_id, get_format


class MyCamera(USBCamera):

    def __init__(self, *args, **kwargs):
        self._camera_mode = kwargs["camera_mode"]
        super(MyCamera, self).__init__(*args, **kwargs)


    def _gst_str(self):
        if self._camera_mode == 'usb':
            cap_device = get_device_id('usb')[0]
            format_ = get_format(cap_device)
            resolution = format_.resolution()
            cap_orig_width = int(resolution[0])
            cap_orig_height = int(resolution[1])
            cap_fps = int(float(resolution[2]))
            crop_height = int((cap_orig_width - self.capture_height) / 2)
            crop_width = int((cap_orig_height- self.capture_width) / 2)
            string = 'v4l2src device=/dev/video{} ' \
                + '! image/jpeg,width=(int){},height=(int){},framerate=(fraction){}/1 '.format(cap_device, cap_orig_width, cap_orig_height, cap_fps) \
                + '! jpegdec ' \
                + '! videoflip method=upper-left-diagonal ' \
                + '! videocrop top={} bottom={} left={} right={} '.format(crop_height, crop_height, crop_width, crop_width) \
                + '! videoconvert ! video/x-raw,format=(string)BGR ' \
                + '! appsink'
        elif self._camera_mode == 'csi':
            cap_device = get_device_id('csi')[0]
            format_ = get_format(cap_device)
            resolution = format_.resolution()
            cap_orig_width = int(resolution[0])
            cap_orig_height = int(resolution[1])
            crop_top = int((cap_orig_height - self.capture_height) / 2)
            if crop_top < 0:
                crop_top = 0
            crop_bottom = cap_orig_height - crop_top
            crop_left = int((cap_orig_width - self.capture_width) / 2)
            if crop_left < 0:
                crop_left = 0
            crop_right = cap_orig_width - crop_left
            string = 'nvarguscamerasrc sensor-id={} '.format(cap_device) \
                + '! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12 ' \
                + '! nvvidconv flip-method=6 left={} right={} top={} bottom={} '.format(crop_left, crop_right, crop_top, crop_bottom) \
                + '! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx '.format(self.capture_width, self.capture_height) \
                + '! videoconvert ' \
                + '! appsink'
        print('video format: ' + string)
        return string