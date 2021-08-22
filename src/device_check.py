import subprocess
from subprocess import PIPE


def get_device_list():
    command1 = "v4l2-ctl --list-devices"

    proc = subprocess.run(command1, shell=True, stdout=PIPE, stderr=PIPE)
    results = proc.stdout.decode('utf-8').splitlines()

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

    device_list = get_device_list().split()
    if len(device_list) == 0:
        raise RuntimeError('No device detected.')
    
    ret = ''
    for device_info in device_list:
        id, mode = device_info.split(':')
        if mode == camera_mode:
            ret += id + ' '

    return ret


if __name__ == '__main__':
    print(get_device_list())
    try:
        print('csi camera id: ' + get_device_id('csi'))
    except:
        print('No csi camera detected.')
    try:
        print('usb camera id: ' + get_device_id('usb'))
    except:
        print('No usb camera detected.')