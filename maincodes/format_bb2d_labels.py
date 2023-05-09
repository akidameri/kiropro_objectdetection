# cd Documents/GearProject/gearproject/maincodes
# python3 format_bb2d_labels.py

import os
import glob
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

# Find paths for all numpy files
in_dir = '/home/kiropro/Documents/GearProject/gearproject/datasets/09_rand_scene' # to be changed
numpy_file_paths = glob.glob(os.path.join(in_dir, '*.npy'))

for i in range(len(numpy_file_paths)):

    fn = np.load(f'/home/kiropro/Documents/GearProject/gearproject/datasets/09_rand_scene/bounding_box_2d_tight_{i:04d}.npy') # to be changed
    df = convert_bbox_to_xywh_format(fn)
    # Save as txt file. Note that the name file must be the same as the rgb images
    with open(f'/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/09_rand_scene/train/labels/rgb_{i:04d}.txt', 'w') as f: # to be changed
        df_string = df.to_string(header=False, index=False) 
        f.write(df_string)