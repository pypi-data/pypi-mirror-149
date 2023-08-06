import os

from pathlib import Path
from setuptools import find_packages, setup

import cycIFAAP



def AllFiles():
	files = ['FiReTiTiLiB.jar', 'lib/*.jar']
	for file_path in Path('cycIFAAP/Restore/').glob('**/*.py'):
		path = str(file_path)
		if not "PyTorch_Models" in path:
			files.append(path[9:])
	return files



setup(
	name=cycIFAAP.__name__,
	packages=find_packages(),
	version=cycIFAAP.__version__,
	author="Guillaume THIBAULT, Erik Burlingame, Young Hwan Chang",
	author_email="thibaulg@ohsu.edu, chanyo@ohsu.edu",
	maintainer="Guillaume THIBAULT",
	maintainer_email="thibaulg@ohsu.edu",
	url="https://www.thibault.biz/Research/cycIFAAP/cycIFAAP.html",
	download_url="https://www.thibault.biz/Doc/cycIFAAP/cycIFAAP-" + cycIFAAP.__version__ + ".tar.gz",
	license="MIT",
	plateforms='ALL',
	package_data={'cycIFAAP': AllFiles()},
	#data_files=[('',['cycIFAAP/FiReTiTiLiB.jar'])],
	keywords=["cyclic Immunofluorescence", "cycif", "immunofluorescence",
				"registration", "segmentation", "features", "features extraction", "restore", "napari",
				"nuclei", "nucleus", "cells", "cell", "cell analysis", "cell type"],
	classifiers=["Development Status :: 5 - Production/Stable",
					"Environment :: Console",
					"Environment :: GPU",
					"Environment :: GPU :: NVIDIA CUDA :: 10.2",
					"Environment :: Other Environment",
					"Intended Audience :: Developers",
					"Intended Audience :: Healthcare Industry",
					"Intended Audience :: Science/Research",
					"License :: OSI Approved :: MIT License",
					"Operating System :: OS Independent",
					"Programming Language :: Java",
					"Programming Language :: Python :: 3",
					"Programming Language :: Python :: 3.8",
					"Programming Language :: Python :: 3.9",
					"Topic :: Scientific/Engineering",
					"Topic :: Scientific/Engineering :: Artificial Intelligence",
					"Topic :: Scientific/Engineering :: Bio-Informatics",
					"Topic :: Scientific/Engineering :: Image Processing",
					"Topic :: Scientific/Engineering :: Image Recognition"],
	install_requires=["FiReTiTiPyLib>=1.4.1",
					"numpy>=1.20",
					#"cellpose>=1.0.0",
					#"DeepCell>=0.11.0",
					],
	python_requires=">=3.8,<3.10",
	description="Cyclic ImmunoFluoresence (cycIF) Automatic Analysis Pipeline",
	long_description=open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
	)
