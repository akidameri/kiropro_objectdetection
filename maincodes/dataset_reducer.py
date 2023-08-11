# cd Documents/GearProject/gearproject/maincodes && python3 dataset_reducer.py

import os
import shutil
from sklearn.model_selection import train_test_split

# Create train, val, and test dirs and subdirs
def create_directories(root_dir):
    try:
        os.makedirs(root_dir + '/images')
        os.makedirs(root_dir + '/labels')
    except FileExistsError:
        pass

# Locate file paths. The paths are sorted in alphabetical order, ensuring the labels are correctly assigned to their respective image files
def get_files_in_folder(folder_path):
    file_names = os.listdir(folder_path)
    file_names = sorted(file_names)
    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]

    return file_paths

# Source path, destination path and reduction ratio (to be changed)
in_root_path = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/real/train'
out_root_path = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/real_200'
reduction_percentage_in_ratio = 0.6875 # percentage reduction = 1 - (reduced size / original size) 

rgb_paths = get_files_in_folder(in_root_path + '/images')
label_paths = get_files_in_folder(in_root_path + '/labels')

# Data reduction using sklearn.train_test_split
rgb_reduced, rgb_omit, label_reduced, label_omit = train_test_split(rgb_paths, label_paths, test_size=reduction_percentage_in_ratio, random_state=42)

create_directories(out_root_path)

# Copy images and labels and move them into their correct dirs
for rgb in rgb_reduced: shutil.copy(rgb, out_root_path + '/images')
for label in label_reduced: shutil.copy(label, out_root_path + '/labels')