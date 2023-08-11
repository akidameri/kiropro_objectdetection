# cd Documents/GearProject/gearproject/maincodes && python3 train_val_test_split.py

import os
import shutil
from sklearn.model_selection import train_test_split

# Create train, val, and test dirs and subdirs
def create_directories(root_dir):
    for file_type in ('images', 'labels'):
        try:
            os.makedirs(root_dir + '/train/' + file_type)
            os.makedirs(root_dir + '/val/' + file_type)
            os.makedirs(root_dir + '/test/' + file_type)
        except FileExistsError:
            pass

# Locate file paths. The paths are sorted in alphabetical order, ensuring the labels are correctly assigned to their respective image files
def get_files_in_folder(folder_path):
    file_names = os.listdir(folder_path)
    file_names = sorted(file_names)
    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]

    return file_paths

# Root source (to be changed)
root_path = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/real_200'

create_directories(root_path)

rgb_paths = get_files_in_folder(root_path + '/images')
label_paths = get_files_in_folder(root_path + '/labels')

# Split the dataset into train, val, test set
rgb_trainval, rgb_test, label_trainval, label_test = train_test_split(rgb_paths, label_paths, test_size=0.1, random_state=42)
rgb_train, rgb_val, label_train, label_val = train_test_split(rgb_trainval, label_trainval, test_size=0.111111111, random_state=42)

# Copy images and labels and move them into their correct dirs
for rgb in rgb_train: shutil.copy(rgb, root_path + '/train/images')
for rgb in rgb_val: shutil.copy(rgb, root_path + '/val/images')
for rgb in rgb_test: shutil.copy(rgb, root_path + '/test/images')
for label in label_train: shutil.copy(label, root_path + '/train/labels')
for label in label_val: shutil.copy(label, root_path + '/val/labels')
for label in label_test: shutil.copy(label, root_path + '/test/labels')