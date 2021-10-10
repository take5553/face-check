#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

import json
import os
from device_check import get_device_id, get_format, get_device_list
import gst_builder

class MySettings():
    
    
    _camera_settings = None
    _capture_settings = None
    _canvas_settings = None
    _save_settings = None
    _recognition_settings = None
    _window_settings = None
    _gst_str = ''
    _setting_file_path = os.path.join(os.path.dirname(__file__), 'setting.json')
    _d = {}
    
    
    def __init__(self):
        self.load()
        
        
    def load(self):
        self._d = self._get_settings_dictionary()
        self._camera_settings = _CameraSettings(self._d['camera_settings'])
        self._capture_settings = _CaptureSettings(self._d['capture_settings'])
        self._canvas_settings = _CanvasSettings(self._d['canvas_settings'])
        self._save_settings = _SaveSettings(self._d['save_settings'])
        self._recognition_settings = _RecognitionSettings(self._d['recognition_settings'], self._d['save_settings'])
        self._window_settings = _WindowSettings(self._d['window_settings'])
        self._gst_str = self._d['gst_str']
        
        
    def save(self):
        self._d = {
            'camera_settings': {
                'device_id' : self._camera_settings.device_id,
                'connection_method' : self._camera_settings.connection_method
            },
            'capture_settings' : {
                'mode' : self._capture_settings.mode,
                'width' : self._capture_settings.width,
                'height' : self._capture_settings.height,
                'fps' : self._capture_settings.fps,
                'rotation' : self._capture_settings.rotation
            },
            'canvas_settings' : {
                'width' : self._canvas_settings.width,
                'height' : self._canvas_settings.height,
                'update_interval' : self._canvas_settings.update_interval
            },
            'save_settings' : {
                'main_dir' : self._save_settings.main_dir,
                'onepic_dir' : self._save_settings.onepic_dir,
                'result_save_dir' : self._save_settings.result_save_dir
            },
            'recognition_settings' : {
                'confirmation_sound' : self._recognition_settings.confirmation_sound
            },
            'window_settings' : {
                'fullscreen' : self._window_settings.fullscreen,
                'fontsize' : self._window_settings.fontsize
            }
        }
        gst_str = gst_builder.get_gst(self._d)
        self._d['gst_str'] = gst_str
        with open(self._setting_file_path, 'w') as f:
            json.dump(self._d, f, indent=4)
        
    @property
    def camera(self):
        return self._camera_settings
    
    
    @property
    def capture(self):
        return self._capture_settings
    
    
    @property
    def canvas(self):
        return self._canvas_settings
    
    
    @property
    def save_dir(self):
        return self._save_settings
    
    
    @property
    def recognition(self):
        return self._recognition_settings
    
    
    @property
    def window(self):
        return self._window_settings
        
        
    @property
    def gst_str(self):
        return self._gst_str
        
        
    def _get_settings_dictionary(self):
        if os.path.exists(self._setting_file_path):
            with open(self._setting_file_path, 'r') as f:
                d = json.load(f)
        else:
            device_str = get_device_list()
            if device_str == '':
                raise RuntimeError('No device detected.')
            device_id, connection_method = device_str.split()[0].split(':')
            format_ = get_format(device_id)
            resolution = format_.resolution()
            d = {
                'camera_settings': {
                    'device_id' : device_id,
                    'connection_method' : connection_method
                },
                'capture_settings' : {
                    'mode' : format_.name,
                    'width' : int(resolution[0]),
                    'height' : int(resolution[1]),
                    'fps' : float(resolution[2]),
                    'rotation' : 0
                },
                'canvas_settings' : {
                    'width' : 400,
                    'height' : 400,
                    'update_interval' : 30
                },
                'save_settings' : {
                    'main_dir' : os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/")),
                    'onepic_dir' : 'register/',
                    'result_save_dir' : os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "../data/result/"))
                },
                'recognition_settings' :{
                    'confirmation_sound' : ''
                },
                'window_settings' : {
                    'fullscreen' : True,
                    'fontsize' : 20
                }
            }
            gst_str = gst_builder.get_gst(d)
            d['gst_str'] = gst_str
            with open(self._setting_file_path, 'w') as f:
                json.dump(d, f, indent=4)
        return d
    
    
class _CameraSettings():
    
    
    _device_id = ''
    _connection_method = ''
    
    
    def __init__(self, camera_settings):
        self._device_id = camera_settings['device_id']
        self._connection_method = camera_settings['connection_method']
        
        
    @property
    def device_id(self):
        return self._device_id
    
    
    @device_id.setter
    def device_id(self, value):
        self._device_id = value
    
    
    @property
    def connection_method(self):
        return self._connection_method
    
    
    @connection_method.setter
    def connection_method(self, value):
        self._connection_method = value
        
    
class _CaptureSettings():
    
    
    _mode = ''
    _width = 0
    _height = 0
    _fps = 0.0
    _rotation = 0
    
    
    def __init__(self, capture_settings):
        self._mode = capture_settings['mode']
        self._width = capture_settings['width']
        self._height = capture_settings['height']
        self._fps = capture_settings['fps']
        self._rotation = capture_settings['rotation']
        
    
    @property
    def mode(self):
        return self._mode
    
    
    @mode.setter
    def mode(self, value):
        self._mode = value
    
    
    @property
    def width(self):
        return self._width
    
    
    @width.setter
    def width(self, value):
        self._width = value
    
    
    @property
    def height(self):
        return self._height
    
    
    @height.setter
    def height(self, value):
        self._height = value
    
    
    @property
    def fps(self):
        return self._fps
    
    
    @fps.setter
    def fps(self, value):
        self._fps = value
    
    
    @property
    def rotation(self):
        return self._rotation
    
    
    @rotation.setter
    def rotation(self, value):
        self._rotation = value


class _CanvasSettings():
    
    
    _width = 0
    _height = 0
    _update_interval = 0
    
    
    def __init__(self, canvas_settings):
        self._width = canvas_settings['width']
        self._height = canvas_settings['height']
        self._update_interval = canvas_settings['update_interval']
        
        
    @property
    def width(self):
        return self._width
    
    
    @width.setter
    def width(self, value):
        self._width = value
        
        
    @property
    def height(self):
        return self._height
    
    
    @height.setter
    def height(self, value):
        self._height = value
        
        
    @property
    def update_interval(self):
        return self._update_interval
    
    
    @update_interval.setter
    def update_interval(self, value):
        self._update_interval = value
        
        
class _SaveSettings():
    
    
    _main_dir = ''
    _onepic_dir = ''
    _result_save_dir = ''
    
    
    def __init__(self, save_settings):
        self._main_dir = save_settings['main_dir']
        if self._main_dir[-1] != '/':
            self._main_dir += '/'
        self._onepic_dir = save_settings['onepic_dir']
        if self._onepic_dir[-1] != '/':
            self._onepic_dir += '/'
        self._result_save_dir = save_settings['result_save_dir']
        if self._result_save_dir[-1] != '/':
            self._result_save_dir += '/'
        
        
    @property
    def main_dir(self):
        return self._main_dir
    
    
    @main_dir.setter
    def main_dir(self, value):
        self._main_dir = value
        
        
    @property
    def onepic_dir(self):
        return self._onepic_dir
    
    
    @onepic_dir.setter
    def onepic_dir(self, value):
        self._onepic_dir = value
        
        
    @property
    def onepic_dir_fullpath(self):
        return self._main_dir + self._onepic_dir
    
    
    @property
    def result_save_dir(self):
        return self._result_save_dir
    
    
    @result_save_dir.setter
    def result_save_dir(self, value):
        self._result_save_dir = value
        
        
class _RecognitionSettings():
    
    
    _main_dir = ''
    _confirmation_sound = ''
    
    
    def __init__(self, recognition_settings, save_settings):
        self._confirmation_sound = recognition_settings['confirmation_sound']
        self._main_dir = save_settings['main_dir']
        
        
    @property
    def confirmation_sound(self):
        if self._confirmation_sound == '':
            return ''
        return os.path.join(self._main_dir, self._confirmation_sound)
        
        
    @property
    def confirmation_sound_filename(self):
        return self._confirmation_sound
    
    
    @confirmation_sound_filename.setter
    def confirmation_sound_filename(self, value):
        self._confirmation_sound = value
        
        
class _WindowSettings():
    
    
    _fullscreen = ''
    _fontsize = 0
    
    
    def __init__(self, window_settings):
        self._fullscreen = window_settings['fullscreen']
        self._fontsize = window_settings['fontsize']
        
        
    @property
    def fullscreen(self):
        return self._fullscreen
    
    
    @fullscreen.setter
    def fullscreen(self, value):
        self._fullscreen = value
        
        
    @property
    def fontsize(self):
        return self._fontsize
    
    
    @fontsize.setter
    def fontsize(self, value):
        self._fontsize = value