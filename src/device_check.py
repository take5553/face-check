import re
import subprocess
from subprocess import PIPE

from capture_format_info import CaptureFormatInfo


def _execute_shell_command(command):
    if command == '':
        raise RuntimeError('No command.')
    
    proc = subprocess.run(command, shell=True, stdout=PIPE, stderr=PIPE)
    return proc.stdout.decode('utf-8')


def _get_device_list():
    command1 = "v4l2-ctl --list-devices"
    results = _execute_shell_command(command1).splitlines()

    device_path_string = '/dev/video'
    csi_camera_string = 'imx219'
    usb_camera_string = 'usb'
    ret = ''

    for i in range(len(results)):
        if device_path_string in results[i]:
            index = results[i].find(device_path_string) + len(device_path_string)
            device_id = results[i][index]
            if csi_camera_string in results[i - 1]:
                camera_mode = 'csi'
            elif usb_camera_string in results[i - 1]:
                camera_mode = 'usb'
            ret += device_id + ':' + camera_mode + ' '
    
    return ret


def get_device_id(camera_mode):
    if not ((camera_mode == 'csi') or (camera_mode == 'usb')):
        raise RuntimeError('Wrong parameter.')

    device_list = _get_device_list().split()
    if len(device_list) == 0:
        raise RuntimeError('No device detected.')
    
    ret = ''
    for device_info in device_list:
        id, mode = device_info.split(':')
        if mode == camera_mode:
            ret += id + ' '

    return ret.split()


def get_formats(device_id):
    command = 'v4l2-ctl -d {} --list-formats-ext'.format(device_id)
    entire_result = _execute_shell_command(command)
    formats = re.split("\n\n", entire_result)
    ret = []

    for i in range(len(formats) - 1):
        ret += [CaptureFormatInfo(formats[i] + '\n')]

    return ret


def get_format(device_id, format_index=None):
    formats = get_formats(device_id)
    if format_index != None:
        return formats[format_index]
    else:
        ret = formats[0]
        for format_ in formats:
            if format_ > ret:
                ret = format_
    return ret
                

if __name__ == '__main__':
    print(_get_device_list())
    try:
        for id in get_device_id('csi'):
            print('csi camera id: ' + id)
    except:
        print('No csi camera detected.')
    try:
        for id in get_device_id('usb'):
            print('usb camera id: ' + id)
    except:
        print('No usb camera detected.')