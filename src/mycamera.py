from jetcam.usb_camera import USBCamera

class MJPGCamera(USBCamera):
    def __init__(self, *args, **kwargs):
        super(MJPGCamera, self).__init__(*args, **kwargs)
    
    def _gst_str(self):
        string = 'v4l2src device=/dev/video{} ! image/jpeg,width=(int){},height=(int){},framerate=(fraction){}/1 ! jpegdec ! videoconvert !  video/x-raw, format=(string)BGR ! appsink'.format(self.capture_device, self.capture_width, self.capture_height, self.capture_fps)
        return string