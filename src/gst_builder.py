from device_check import get_device_id, get_format

def get_gst(settings):
    cap_device = settings['camera_settings']['device_id']
    string = ''

    if settings['camera_settings']['connection_method'] == 'usb':
        string += 'v4l2src device=/dev/video{}'.format(cap_device)
        # Capture
        if settings['capture_settings']['mode'] == 'MJPG':
            string += ' ! image/jpeg,width=(int){},height=(int){},framerate=(fraction){}/1 ! jpegdec' \
                .format(settings['capture_settings']['width'], settings['capture_settings']['height'], int(settings['capture_settings']['fps']))
        else:
            string += ' ! video/x-raw,width=(int){},height=(int){},framerate=(fraction){}/1' \
                .format(settings['capture_settings']['width'], settings['capture_settings']['height'], int(settings['capture_settings']['fps']))
        # Flip
        if settings['capture_settings']['rotation'] == 0:
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 1:
            string += ' ! videoflip method=counterclockwise'
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 2:
            string += ' ! videoflip method=rotate-180'
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 3:
            string += ' ! videoflip method=clockwise'
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 4:
            string += ' ! videoflip method=horizontal-flip'
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 5:
            string += ' ! videoflip method=upper-right-diagonal'
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 6:
            string += ' ! videoflip method=vertical-flip'
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 7:
            string += ' ! videoflip method=upper-left-diagonal'
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        # Crop
        crop_height = int((int(cap_height) - int(settings['canvas_settings']['height'])) / 2)
        crop_width = int((int(cap_width) - int(settings['canvas_settings']['width'])) / 2)
        if crop_height < 0:
            crop_height = 0
        if crop_width < 0:
            crop_width = 0
        if crop_height != 0 or crop_width != 0:
            string += ' ! videocrop top={} bottom={} left={} right={}'.format(crop_height, crop_height, crop_width, crop_width)
        # Output
        string += ' ! videoconvert ! video/x-raw,format=(string)BGR ! appsink'
    elif settings['camera_settings']['connection_method'] == 'csi':
        # Capture
        string += 'nvarguscamerasrc sensor-id={}'.format(cap_device)
        string += ' ! video/x-raw(memory:NVMM), width={}, height={}, format=(string)NV12' \
            .format(settings['capture_settings']['width'], settings['capture_settings']['height'])
        # Flip and Crop (with 90 degree rotatation or just flipping horizontally)
        if settings['capture_settings']['rotation'] == 0:
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 1:
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 2:
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 3:
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 4:
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 5:
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 6:
            cap_height, cap_width = settings['capture_settings']['height'], settings['capture_settings']['width']
        elif settings['capture_settings']['rotation'] == 7:
            cap_width, cap_height = settings['capture_settings']['height'], settings['capture_settings']['width']
        crop_top = int((int(cap_height) - int(settings['canvas_settings']['height'])) / 2)
        crop_left = int((int(cap_width) - int(settings['canvas_settings']['width'])) / 2)
        if crop_top < 0:
            crop_top = 0
        if crop_left < 0:
            crop_left = 0
        crop_bottom = int(cap_height) - crop_top
        crop_right = int(cap_width) - crop_left
        string += ' ! nvvidconv'
        if settings['capture_settings']['rotation'] != 0:
            string += ' flip-method={}'.format(settings['capture_settings']['rotation'])
        if crop_top != 0 or crop_left != 0:
            string += ' left={} right={} top={} bottom={}'.format(crop_left, crop_right, crop_top, crop_bottom)
        # Output
        string += ' ! video/x-raw, width=(int){}, height=(int){}, format=(string)BGRx' \
            .format(settings['canvas_settings']['width'], settings['canvas_settings']['height'])
        string += ' ! videoconvert ! appsink'
    return string