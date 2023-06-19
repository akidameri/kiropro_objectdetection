from dis import dis
import os
import json

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches

'''
Takes the segmentation images, the color for the labels and the output path to visualize the segmentation output
'''

def colorize_bbox_2d(rgb_path, rgb_label, file_path):

    lines = rgb_label.readlines()
    rgb_label.close

    for index, line in enumerate(lines):
        lines[index] = line.strip()
        lines[index] = line.split()

    rgb_img = Image.open(rgb_path)
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.imshow(rgb_img)
    for bbox_2d in lines:
        labels = 'gear'
        x_min = bbox_2d(1) - bbox_2d(3)/2
        y_min = bbox_2d(2) - bbox_2d(4)/2
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

image_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/example_dataset/train/images' # to be changed
image = "rgb_0040.png" # to be changed
vis_out_dir = '/home/kiropro//Documents/GearProject/gearproject/visualizer'
image_path = os.path.join(image_dir, image)
rgb_image = Image.open(image_path)

label_dir = '/home/kiropro/Documents/GearProject/gearproject/yolov7-main/data/example_dataset/train/labels' # to be changed
label = "rgb_0040.txt" # to be changed
rgb_label = open(os.path.join(label_dir, label), "r")

# colorize and save image
colorize_bbox_2d(rgb_path, data, bbox2d_tight_id_to_labels, os.path.join(vis_out_dir, "bbox2d_tight_0000.png")) # to be changed
