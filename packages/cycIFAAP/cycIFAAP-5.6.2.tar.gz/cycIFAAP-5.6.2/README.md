# Cyclic ImmunoFluorescence Automatic Analysis Pipeline

This pipeline takes as input a set of cyclic immunofluorescence (cycIF) images and performs the following operations:
 - Registration
 - Nuclei segmentation (using CellPose or own trained Mask R-CNN model)
 - Background subtraction
 - Compute each marker exclusiveness to be used with Restore
 - Use Restore when possible for automatic gating (optionnal)
 - Features extraction
 - Cell type computation
 - Automatic visualization using Napari
 - Quality control (tissue loss and Restore based)


For installation, more information/details and full examples with code and data, visit:
https://www.thibault.biz/Research/cycIFAAP/cycIFAAP.html
