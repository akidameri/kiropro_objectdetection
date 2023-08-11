# cd Documents/GearProject/gearproject/maincodes && python3 format_bb2d_labels_domain_rand.py

# TO BE CHANGED: in_dir, out_dir

import os
import glob
import shutil
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split


def convert_bbox_to_xywh_format(numpy_data):

    # Change to dataframe type
    df = pd.DataFrame(numpy_data, columns = ['semanticID','x_min','y_min','x_max','y_max'])
    
    # Calculate x_center, y_center, width, and height to match the yolov7 label format
    df['x_center'] = (df['x_max']+df['x_min'])/2
    df['y_center'] = (df['y_max']+df['y_min'])/2
    df['width'] = df['x_max']-df['x_min']
    df['height'] = df['y_max']-df['y_min']

    # Remove unnecessary columns
    df.drop(['x_min', 'y_min', 'x_max', 'y_max'], axis=1,inplace=True)

    # Convert pixels to normalized xywh format (from 0 - 1). I.e. pixels will be divided by image width and heigth
    df = df/640

    # Change class ID to 0
    df['semanticID'] = 0

    return df

# Create temporary, train, val, and test dirs and subdirs. The temporary directory is used to copy the files from the source to the destination file, before splitting into train/val/test sets
def create_directories(root_dir):
    for file_type in ('images', 'labels'):
        try:
            os.makedirs(root_dir + '/temp/' + file_type)
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

# Find paths for all numpy files
in_dir = '/home/kiropro/Documents/GearProject/gearproject/datasets/p09_flying_wo_shadow' # to be changed
out_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/p09_flying_wo_shadow' # to be changed

create_directories(out_dir)

numpy_file_paths = glob.glob(os.path.join(in_dir, '*.npy'))

for i in range(len(numpy_file_paths)):
    fn = np.load(in_dir + f'/bounding_box_2d_tight_{i:04d}.npy')
    df = convert_bbox_to_xywh_format(fn)
    # Save as txt file. Note that the name file must be the same as the rgb images
    with open(out_dir + f'/temp/labels/rgb_{i:04d}.txt', 'w') as f:
        df_string = df.to_string(header=False, index=False) 
        f.write(df_string)

# Find, copy, and paste RGB files to another folder
rgb_file_paths = glob.glob(os.path.join(in_dir, '*.png'))
for rgb in rgb_file_paths:
    shutil.copy(rgb, out_dir + '/temp/images')

rgb_paths = get_files_in_folder(out_dir + '/temp/images')
label_paths = get_files_in_folder(out_dir + '/temp/labels')

# Split the dataset into train, val, test set (Train:val:test = 0.8:0.1:0.1)
rgb_trainval, rgb_test, label_trainval, label_test = train_test_split(rgb_paths, label_paths, test_size=0.1, random_state=42)
rgb_train, rgb_val, label_train, label_val = train_test_split(rgb_trainval, label_trainval, test_size=0.1111111, random_state=42)

# Copy images and labels and move them into their correct dirs
for rgb in rgb_train: shutil.copy(rgb, out_dir + '/train/images')
for rgb in rgb_val: shutil.copy(rgb, out_dir + '/val/images')
for rgb in rgb_test: shutil.copy(rgb, out_dir + '/test/images')
for label in label_train: shutil.copy(label, out_dir + '/train/labels')
for label in label_val: shutil.copy(label, out_dir + '/val/labels')
for label in label_test: shutil.copy(label, out_dir + '/test/labels')