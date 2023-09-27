# Object Detection using YOLOV7x trained on Synthetic and Real-Life Datasets

This is the reprisatory used for my master's thesis with the topic "Comparative Analysis of an Object Detection Method Trained on Synthetic and Real-World Images for Industrial Robotic Assembly
Processes". The thesis is aiming to compare and analayse the performance between object detection model trained on synthetic and real-life datasets, and then opmtimising the performance of the model.

Inside this reprisatory you will find the main codes for synthetic data generation.

Inside the maincodes/syngears directory, you will find the codes to generate synthetic images for the SynGears dataset. The python scripts inside this directory contain suffixes. The suffixes refer to the eight scenes of the SynGears dataset. Refer the documentation of Chapter 5.1.2, specifically Table 5.2 and Figure 5.7.

Inside the maincodes/domain-randomisation-with-physics directory, you will find codes to generate synthetic data to create domain randomisation datasets, discussed in Chapter 6.3.

Other code files inside the maincodes directory consist of:

1) bb2d_visualizer_npy.py : 
