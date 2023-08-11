# cd Documents/GearProject/gearproject/maincodes && python3 move_and_rename.py

import os
import glob
import shutil
import numpy as np
import pandas as pd

# Create images, labels and temporary dirs and subdirs
def create_directories(root_dir):
    try:
        os.makedirs(root_dir + '/temp')
        os.makedirs(root_dir + '/images')
        os.makedirs(root_dir + '/labels')
    except FileExistsError:
        pass

# Find paths for all numpy files, convert them to the right format, and save them into another folder
# These 3 variables below must be changed
in_root_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/data-increment/syn_4000' 
out_root_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/full_opt' 
num = 3457 # Starting index number to rename images and labels 

create_directories(out_root_dir)

temp_dir =  out_root_dir + '/temp'
rgb_dir = out_root_dir + '/images'
label_dir = out_root_dir + '/labels'

rgb_file_paths = glob.glob(os.path.join(in_root_dir + '/images', '*.png'))
label_file_paths = glob.glob(os.path.join(in_root_dir + '/labels', '*.txt'))

for rgb in rgb_file_paths:
    shutil.copy(rgb, temp_dir)
for label in label_file_paths:
    shutil.copy(label, temp_dir)

# Rename RGB files
files = os.listdir(in_root_dir + '/images')
for i in range(len(files)):

    rgb_source = os.path.join(temp_dir, f'rgb_{i}.png')
    rgb_destination = os.path.join(rgb_dir, f'rgb_{i + num}.png')
    os.rename(rgb_source, rgb_destination)

    label_source = os.path.join(temp_dir, f'rgb_{i}.txt')
    label_destination = os.path.join(label_dir, f'rgb_{i + num}.txt')
    os.rename(label_source, label_destination)