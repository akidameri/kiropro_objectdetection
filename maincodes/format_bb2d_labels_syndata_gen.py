# cd Documents/GearProject/gearproject/maincodes && python3 format_bb2d_labels_syndata_gen.py

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

# Find paths for all numpy files, convert them to the right format, and save them into another folder
# These 3 variables below must be changed
in_root_dir = '/home/kiropro/Documents/GearProject/gearproject/datasets/p11_scene' 
out_root_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/full_opt' 
num = 1871 # Starting index number to rename images and labels 

create_directories(out_root_dir)

numpy_file_paths = glob.glob(os.path.join(in_root_dir, '*0059.npy'))

for i in range(len(numpy_file_paths)):
    fn = np.load(in_root_dir + f'/bounding_box_2d_tight_{i}_0059.npy')
    df = convert_bbox_to_xywh_format(fn)
    # Save as txt file. Note that the name file must be the same as the rgb images
    with open(out_root_dir + f'/labels/rgb_{i + num}.txt', 'w') as f:
        df_string = df.to_string(header=False, index=False) 
        f.write(df_string)

# Find, copy, and paste RGB files to another folder
rgb_file_paths = glob.glob(os.path.join(in_root_dir, '*0059.png'))
temp_dir =  out_root_dir + '/temp'
rgb_dir = out_root_dir + '/images'
for rgb in rgb_file_paths:
    shutil.copy(rgb, temp_dir)

# Rename RGB files
files = os.listdir(temp_dir)
for i in range(len(files)):
    source = os.path.join(temp_dir, f'rgb_{i}_0059.png')
    destination = os.path.join(rgb_dir, f'rgb_{i + num}.png')
    os.rename(source, destination)