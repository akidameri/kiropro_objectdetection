# cd Documents/GearProject/gearproject/maincodes
# python3 format_bb2d_labels_syndata_gen.py

import os
import glob
import shutil
import numpy as np
import pandas as pd

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
in_dir = '/home/kiropro/Documents/GearProject/gearproject/datasets/synthetic08' # to be changed
numpy_file_paths = glob.glob(os.path.join(in_dir, '*0059.npy'))
num = 700 # to be changed

for i in range(len(numpy_file_paths)):
    fn = np.load(f'/home/kiropro/Documents/GearProject/gearproject/datasets/synthetic08/bounding_box_2d_tight_{i}_0059.npy') # to be changed
    df = convert_bbox_to_xywh_format(fn)
    # Save as txt file. Note that the name file must be the same as the rgb images
    with open(f'/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/syn/labels/rgb_{i + num}.txt', 'w') as f: 
        df_string = df.to_string(header=False, index=False) 
        f.write(df_string)

# Find, copy, and paste RGB files to another folder
rgb_file_paths = glob.glob(os.path.join(in_dir, '*0059.png'))
temp_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/syn/temp'
out_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/syn/images'
for rgb in rgb_file_paths:
    shutil.copy(rgb, temp_dir)

# Rename RGB files
files = os.listdir(temp_dir)
for i in range(len(files)):
    source = os.path.join(temp_dir, f'rgb_{i}_0059.png')
    destination = os.path.join(out_dir,f'rgb_{i + num}.png')
    os.rename(source, destination)