import os
import numpy as np
from sklearn.model_selection import train_test_split

def get_files_in_folder(folder_path):
    file_names = os.listdir(folder_path)
    file_names = sorted(file_names)

    file_paths = [os.path.join(folder_path, file_name) for file_name in file_names]
    return file_paths

root_path = 

rgb_paths = get_files_in_folder(root_path + '/images')
label_paths = get_files_in_folder(root_path + '/labels')

rgb_trainval, rgb_test, label_trainval, label_test = train_test_split(rgb_paths, label_paths, test_size=0.1, random_state=42)
rgb_train, rgb_val, label_train, label_val = train_test_split(rgb_trainval, label_trainval, test_size=0.1, random_state=42)



dst_path =

