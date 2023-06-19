import os
import numpy as np
import shutil
from sklearn.model_selection import train_test_split

def get_files_in_folder(folder_path):
    file_names = os.listdir(folder_path)
    file_names = sorted(file_names)

    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]

    return file_paths

def create_directories(root_dir):
    for file_type in ('images', 'labels'):
        try:
            os.makedirs(root_dir + '/train/' + file_type)
            os.makedirs(root_dir + '/val/' + file_type)
            os.makedirs(root_dir + '/test/' + file_type)
        except FileExistsError:
            pass

root_path = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/synreal_25'

rgb_paths = get_files_in_folder(root_path + '/images')
label_paths = get_files_in_folder(root_path + '/labels')

create_directories(root_path)

rgb_trainval, rgb_test, label_trainval, label_test = train_test_split(rgb_paths, label_paths, test_size=0.1, random_state=42)
rgb_train, rgb_val, label_train, label_val = train_test_split(rgb_trainval, label_trainval, test_size=0.1, random_state=42)

shutil.copy(rgb_train, root_path + '/train/images')
shutil.copy(rgb_val, root_path + '/val/images')
shutil.copy(rgb_test, root_path + '/test/images')
shutil.copy(label_train, root_path + '/train/labels')
shutil.copy(label_val, root_path + '/val/labels')
shutil.copy(label_test, root_path + '/test/labels')