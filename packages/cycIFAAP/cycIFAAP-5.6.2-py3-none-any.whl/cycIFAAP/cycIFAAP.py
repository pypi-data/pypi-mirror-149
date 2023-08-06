import importlib
import os
import sys

import FiReTiTiPyLib.CyclicIF.CyclicIF_JavaInterfacer as cycIFji



def Run(parameters):
	cycIFji.Run(parameters, JavaJarsPath=os.path.dirname(os.path.abspath(__file__)))
	print("cycIFAAP done!")
	#sys.exit(0)



if __name__ == '__main__':

	Parameters = {'nbCPU': 12, # Number of CPU / cores you wish to use.
				'Experiment': "CROPS", # Can be 'CROPS' or 'TMA'.
				#'Python_Path': "...", # If necessary, give the entire / absolute path to your python.
				#'Java_Xms': '4G', # How much memory to allocate when the job starts.
				#'Java_Xmx': '8G', # How much memory maximum to allocate.
				#'Registration_Technique': "OpenCV", #Which registration technique to use?
				'Registration_Reverse': True, # If True the last round dapi image will be used as reference instead of the first round dapi image.
				'SegmentNuclei_RoundToSegment': 'R1', #ZProjection', # Which round to segment? By default the consensus/z-projection.
				'SegmentNuclei_Model': 'MaskRCNN_512x512_Norm=B - 9686_831_8976 - 20201009.pt', # The deep learning segmentation model to use.
				#'SegmentNuclei_Model': 'CellPose_cpu_30_0.4', # In this example, CellPose will use CPUs and the number is the CellPose diameter parameter.
				'SegmentNuclei_Model': 'Mesmer', # In this example, CellPose will use CPUs and the number is the CellPose diameter parameter.
				#'SegmentNuclei_BorderEffectSize': 73, # Nuclei segmentation parameter.
				#'SegmentNuclei_BatchSize': 3, # Nuclei segmentation parameter.
				#'SegmentNuclei_CheckOverlap': 7, # Nuclei segmentation parameter.
				#'SegmentNuclei_SaveNuclei': False, # Nuclei segmentation parameter.
				#'SegmentNuclei_Threshold': 0.07, # Nuclei segmentation parameter.
				'SegmentCells_DilationRatio': 3.0, # Coeffient applied to the inflated nuclei for cell segmentation if no markers are available
				'ExitAfterSegmentation': True, # If True, the pipeline will stop after cell segmentation, and skip background subtraction and exclusive markers.
				#'Background_Subtraction': True, # If True, the background subtraction will be performed for each marker and used during features extraction.
				'Images_Directory': "/Users/firetiti/Downloads/CyclicIF/cycIFAAP_Example1/Test - 2048x2048/", # The directory containing the images to process. Always make a backup!!!
				#'FE_SaveImages': True, # If True, all the resulting / check images will be saved.
				#'FE_BiasedFeaturesOnly': True, # If True, only the biased (intensity based) features will be extracted.
				#'FE_DistanceFromBorder': True, # If True, the distance from the sample border will be computed.
				#'FE_Rim_Size': 3f, # The rim size/dimensions/width.
				#'Segmentation': False, # If True, it performs the segmentation, but skips the registration.
				'Registration_And_Segmentation': True, # If True, this starts the registration and segmentation.
				#'FeaturesExtraction': True, # If True, this starts the features extraction.
				#'QualityControl': False, # If True, this starts the quality control.
				}
	
	Run(Parameters)


