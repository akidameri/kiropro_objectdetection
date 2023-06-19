# conda activate sklearn-env
# cd Desktop/Masterarbeit Objekterkennung
# python train_val_test_split.py

import os
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

root_path = 'C:/Users/User/Desktop/Masterarbeit Objekterkennung/Images/test_02'

rgb_paths = get_files_in_folder(root_path + '/images')
label_paths = get_files_in_folder(root_path + '/labels')

create_directories(root_path)

rgb_trainval, rgb_test, label_trainval, label_test = train_test_split(rgb_paths, label_paths, test_size=0.1, random_state=42)
rgb_train, rgb_val, label_train, label_val = train_test_split(rgb_trainval, label_trainval, test_size=0.1, random_state=42)

for rgb in rgb_train: shutil.copy(rgb, root_path + '/train/images')
for rgb in rgb_val: shutil.copy(rgb, root_path + '/val/images')
for rgb in rgb_test: shutil.copy(rgb, root_path + '/test/images')
for label in label_train: shutil.copy(label, root_path + '/train/labels')
for label in label_val: shutil.copy(label, root_path + '/val/labels')
for label in label_test: shutil.copy(label, root_path + '/test/labels')