from jetcam.usb_camera import USBCamera

class MyCamera(USBCamera):
    def __init__(self, *args, **kwargs):
        super(MyCamera, self).__init__(*args, **kwargs)
    
    def _gst_str(self):
        crop_height = int((1920 - self.capture_height) / 2)
        crop_width = int((1080- self.capture_width) / 2)
        string = 'v4l2src device=/dev/video{} ! image/jpeg,width=(int)1920,height=(int)1080,framerate=(fraction){}/1 ! jpegdec ! videoflip method=upper-left-diagonal ! videocrop top={} bottom={} left={} right={} ! videoconvert ! video/x-raw,format=(string)BGR ! appsink'.format(self.capture_device, self.capture_fps, crop_height, crop_height, crop_width, crop_width)
        print('video format: ' + string)
        return string