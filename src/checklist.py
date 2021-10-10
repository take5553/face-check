#
# Copyright (c) 2021 Takeshi Yamazaki
# This software is released under the MIT License, see LICENSE.
#

import os
import datetime
from mysettings import MySettings

class CheckList():
    
    settings = None
    _check_list = []
    _checked_list = []
    _non_registered_list = []
    
    def __init__(self):
        self.settings = MySettings()
        self._checklist_filename = 'checklist.txt'
        self._checkedlist_filename = 'checked.txt'
        
        self._list_path = self.settings.save_dir.main_dir
        os.makedirs(self._list_path, exist_ok=True)
        self._registered_dir = self._list_path + self.settings.save_dir.onepic_dir
        os.makedirs(self._registered_dir, exist_ok=True)
        self._result_dir = self.settings.save_dir.result_save_dir
        os.makedirs(self._result_dir, exist_ok=True)
        
        self.init_checking()
        
        
    def add_to_checked(self, name):
        self._checked_list.append(name)
        self._save_checked_list()
    
        
    def _save_checked_list(self):
        s = '\n'.join(self._checked_list)
        with open(self._list_path + self._checkedlist_filename, 'w') as f:
            f.write(s)
        
        
    def has_name(self, name):
        return name in self._check_list
        
        
    def already_checked(self, name):
        return name in self._checked_list
    
    
    def init_checking(self):
        files = sorted(os.listdir(self._registered_dir))
        self._file_list = [os.path.join(self._registered_dir, f) for f in files if os.path.isfile(os.path.join(self._registered_dir, f))]
        registered_list = [s[:-8] for s in files]
        if not os.path.exists(self._list_path + self._checklist_filename):
            self._check_list = registered_list
            self._non_registered_list = []
            s = '\n'.join(self._check_list)
            with open(self._list_path + self._checklist_filename, 'w') as f:
                f.write(s)
        else:
            with open(self._list_path + self._checklist_filename, 'r') as f:
                input_list = [s.strip() for s in f.readlines()]
            self._check_list = sorted(list(set(input_list) & set(registered_list)))
            self._non_registered_list = sorted(list(set(self._check_list) ^ set(input_list)))
        if not os.path.exists(self._list_path + self._checkedlist_filename):
            self._checked_list = []
        else:
            with open(self._list_path + self._checkedlist_filename, 'r') as f:
                self._checked_list = [s.strip() for s in f.readlines()]
                
                
    def get_checked_list(self):
        return self._checked_list
    
    
    def delete_from_checked_list(self, index):
        del self._checked_list[index]
        self._save_checked_list()

    
    def finish_checking(self):
        dt_now = datetime.datetime.now()
        result = dt_now.strftime('%Y-%m-%d %H:%M:%S') + '\n\n'
        result += '-----checked-----\n'
        for name in self._checked_list:
            result += name + '\n'
        result += '\n'
        result += '-----not checked-----\n'
        not_checked_list = sorted(list(set(self._check_list) ^ set(self._checked_list)))
        for name in not_checked_list:
            result += name + '\n'
        result += '\n'
        result += '-----not registered-----\n'
        for name in self._non_registered_list:
            result += name + '\n'
        file_name = 'result{}.txt'.format(dt_now.strftime('%Y%m%d-%H%M%S'))
        os.makedirs(self._result_dir, exist_ok=True)
        with open(self._result_dir + file_name, 'w') as f:
            f.write(result)
        os.remove(self._list_path + self._checkedlist_filename)
        self._checked_list = []
        return self._list_path + file_name