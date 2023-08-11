# cd Documents/GearProject/gearproject/maincodes
# python3 bb2d_visualizer_npy.py

from dis import dis
import os
import json

import hashlib
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

'''
Takes in the data from a specific label id and maps it to the proper color for the bounding box
'''
def data_to_colour(data):
    if isinstance(data, str):
        data = bytes(data, "utf-8")
    else:
        data = bytes(data)
    m = hashlib.sha256()
    m.update(data)
    key = int(m.hexdigest()[:8], 16)
    r = ((((key >> 0) & 0xFF) + 1) * 33) % 255
    g = ((((key >> 8) & 0xFF) + 1) * 33) % 255
    b = ((((key >> 16) & 0xFF) + 1) * 33) % 255

    # illumination normalization to 128
    inv_norm_i = 128 * (3.0 / (r + g + b))

    return (int(r * inv_norm_i) / 255, int(g * inv_norm_i) / 255, int(b * inv_norm_i) / 255)

'''
Takes the segmentation images, the color for the labels and the output path to visualize the segmentation output
'''

def colorize_bbox_2d(rgb_path, data, id_to_labels, file_path):

    rgb_img = Image.open(rgb_path)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(rgb_img)
    for bbox_2d in data:
        id = bbox_2d["semanticId"]
        color = data_to_colour(id)
        labels = id_to_labels[str(id)]
        rect = patches.Rectangle(
            xy=(bbox_2d["x_min"], bbox_2d["y_min"]),
            width=bbox_2d["x_max"] - bbox_2d["x_min"],
            height=bbox_2d["y_max"] - bbox_2d["y_min"],
            edgecolor=color,
            linewidth=2,
            label=labels,
            fill=False,
        )
        ax.add_patch(rect)

    plt.legend(loc="upper left")

    plt.savefig(file_path)

out_dir = '/home/kiropro/Documents/GearProject/gearproject/datasets/01_single' # to be changed
rgb = "rgb_0040.png" # to be changed
vis_out_dir = '/home/kiropro//Documents/GearProject/gearproject/visualizer'
rgb_path = os.path.join(out_dir, rgb)
rgb_image = Image.open(rgb_path)

bbox2d_tight_file_name = "bounding_box_2d_tight_0040.npy" # to be changed
data = np.load(os.path.join(out_dir, bbox2d_tight_file_name))

# Check for labels
bbox2d_tight_labels_file_name = "bounding_box_2d_tight_labels_0040.json" # to be changed
with open(os.path.join(out_dir, bbox2d_tight_labels_file_name), "r") as json_data:
    bbox2d_tight_id_to_labels = json.load(json_data)

# colorize and save image
colorize_bbox_2d(rgb_path, data, bbox2d_tight_id_to_labels, os.path.join(vis_out_dir, "bbox2d_tight_0040.png")) # to be changed
