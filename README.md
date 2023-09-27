# Comparative Analysis of an Object Detection Method Trained on Synthetic and Real-World Images for Industrial Robotic Assembly Processes

This is the reprisatory used for my master's thesis. The thesis is aiming to compare and analayse the performance between object detection model trained on synthetic and real-life datasets, and then opmtimising the performance of the model.

Inside this reprisatory you will find the main codes for synthetic data generation.


## The maincodes/syngears Directory

Inside the maincodes/syngears directory, you will find the codes to generate synthetic images for the SynGears dataset. The python scripts inside this directory contain suffixes. The suffixes refer to the eight scenes of the SynGears dataset. Refer the documentation of Chapter 5.1.2, specifically Table 5.2 and Figure 5.7.


## The maincodes/domain-randomisation-with-physics Directory

Inside the maincodes/domain-randomisation-with-physics directory, you will find codes to generate synthetic data to create domain randomisation (DR) datasets, discussed in Chapter 6.3.


## Others
Other code files inside the maincodes directory consist of:

1) bb2d_visualizer_npy.py : The code is used to visualise the bounding box annotation from the label files.
   
2) dataset_reducer.py: The code is used to reduce the size of dataset. The code will randomly choose image and label files based on the input percentage reduction, and omit them. It is used in the approaches in Chapter 6.1 and Chapter 6.2.
  
3) format_bb2d_labels_domain_rand.py and format_bb2d_labels_syndata_gen.py: They are used to convert the default label format to YOLO label format. The difference between these two is that, the format_bb2d_labels_domain_rand.py is mainly used to convert labels within DR datasets, while the another code is used for other datasets outside DR applications.

4) move_and_rename.py: The code is used to move and rename image and label files

5) train_val_test_split.py: It used to split the dataset into training, validation, and test sets.
