from jetcam.usb_camera import USBCamera

class MyCamera(USBCamera):
    def __init__(self, *args, **kwargs):
        self._camera_mode = kwargs["camera_mode"]
        super(MyCamera, self).__init__(*args, **kwargs)
    
    def _gst_str(self):
        if self._camera_mode == 'usb':
            cap_device = 1
            cap_orig_width = 1920
            cap_orig_height = 1080
            cap_fps = 30
            crop_height = int((cap_orig_width - self.capture_height) / 2)
            crop_width = int((cap_orig_height- self.capture_width) / 2)
            string = 'v4l2src device=/dev/video{} ! image/jpeg,width=(int){},height=(int){},framerate=(fraction){}/1 ! jpegdec ! videoflip method=upper-left-diagonal ! videocrop top={} bottom={} left={} right={} ! videoconvert ! video/x-raw,format=(string)BGR ! appsink'.format(cap_device, cap_orig_width, cap_orig_height, cap_fps, crop_height, crop_height, crop_width, crop_width)
        elif self._camera_mode == 'csi':
            cap_device = 0
            cap_orig_width = 1280
            cap_orig_height = 720
            crop_top = int((cap_orig_height - self.capture_height) / 2)
            if crop_top < 0:
                crop_top = 0
            crop_bottom = cap_orig_height - crop_top
            crop_left = int((cap_orig_width - self.capture_width) / 2)
            if crop_left < 0:
                crop_left = 0
            crop_right = cap_orig_width - crop_left
            string = 'nvarguscamerasrc sensor-id={} ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12 ! nvvidconv flip-method=6 left={} right={} top={} bottom={} ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx ! videoconvert ! appsink'.format(cap_device, crop_left, crop_right, crop_top, crop_bottom, self.capture_width, self.capture_height)
        print('video format: ' + string)
        return string