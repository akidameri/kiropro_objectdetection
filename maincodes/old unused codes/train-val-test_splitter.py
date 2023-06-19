# cd Documents/GearProject/gearproject/maincodes
# python3 train-val-test_splitter.py

import os
import shutil
import numpy as np

def copy_and_move_files(root_dir, file_type, file_format, train_indexes, val_indexes, test_indexes):
    
    # Create directories
    try:
        os.makedirs(root_dir + '/train/' + file_type)
        os.makedirs(root_dir + '/val/' + file_type)
        os.makedirs(root_dir + '/test/' + file_type)
    except FileExistsError:
        pass

    # Source path for images/labels
    source = root_dir + '/' + file_type

    # Move the splitted dataset into their respective folder
    for i in train_indexes:
        train_source = os.path.join(source, f'rgb_{i:04d}.{file_format}')
        train_destination = root_dir + '/train/' + file_type
        shutil.copy(train_source, train_destination)

    for i in val_indexes:
        val_source = os.path.join(source, f'rgb_{i:04d}.{file_format}')
        val_destination = root_dir + '/val/' + file_type
        shutil.copy(val_source, val_destination)

    for i in test_indexes:
        test_source = os.path.join(source, f'rgb_{i:04d}.{file_format}')
        test_destination = root_dir + '/test/' + file_type
        shutil.copy(test_source, test_destination)

# Root path
root_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/04_flying'
rgb_source = root_dir + '/images'

# Index files for rgbs/labels. The rgbs and labels must have the same index in train/val/test subfolder
index = list(range(len(os.listdir(rgb_source))))

# Shuffle index files
np.random.shuffle(index)

#Split to 80% train, 10% val, 10% test
val_ratio = 0.1
test_ratio = 0.1
train_indexes, val_indexes, test_indexes = np.split(
    np.array(index),
    [int(len(index)*(1 - (val_ratio + test_ratio))),
     int(len(index)*(1 - (test_ratio)))],
     axis=0)

# Copy files and move them into their respective folders
copy_and_move_files(root_dir, 'images', 'png', train_indexes, val_indexes, test_indexes)
copy_and_move_files(root_dir, 'labels', 'txt', train_indexes, val_indexes, test_indexes)