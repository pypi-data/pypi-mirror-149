import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import seaborn
import sys

from collections import defaultdict
from scipy.stats import gaussian_kde
from sklearn import cluster
from sklearn import mixture

from cycIFAAP.Restore.ssc.cluster import selfrepresentation as sr



def nested_dict():
	"""
	A nested dictionary for hierarchical storage of thresholds.
	"""
	return defaultdict(nested_dict)



class Normalization:
	"""
	Automated intensity normalization framework for cycIF imaging datasets.
	
	Parameters
	----------
	
	data: pandas DataFrame
		Contains batch ids, scene ids, cell ids, and marker intensities.
	marker_pairs: list of lists
		Each sub-list contains a marker and its exclusive counterpart marker.
	save_dir: string
		Path to directory for saving results
	manual_thresh: nested dict, optional
		Manual thresholds for adding to figures
		
	Attributes
	----------
	threshs: nested dictionary
	
	"""
	
	def __init__(self, data, marker_pairs, save_dir, save_figs=True, manual_threshs=None, Debug: bool=False):
		"""
		:param data:
		:param marker_pairs:
		:param save_dir:
		:param save_figs:
		:param manual_threshs:
		:param Debug:
		"""
		self.data = data
		self.threshs = nested_dict()
		self.Thresholds = []
		self.marker_pairs = marker_pairs
		self.save_dir = save_dir
		self.save_figs = save_figs
		self.manual_threshs = manual_threshs
		self.Debug = Debug
		if Debug:
			print(*marker_pairs, sep='\n')
		
		
	def get_GMM_thresh(self, data, model, sigma_weight):
		"""
		:param data:
		:param model:
		:param sigma_weight: int, Weighting factor for sigma, where higher value == fewer cells classified as positive.
		:return:
		"""
		model.fit(data)

		neg_idx = np.argmax([np.diagonal(i)[1] for i in model.covariances_])

		mu = model.means_[neg_idx,0]

		# Extract sigma from covariance matrix
		sigma = np.sqrt(np.diagonal(model.covariances_[neg_idx])[0])

		return mu + sigma_weight * sigma



	def get_clustering_thresh(self, data, model, sigma_weight):
		"""
		:param data:
		:param model:
		:param sigma_weight:  int, Weighting factor for sigma, where higher value == fewer cells classified as positive.
		:return:
		"""
		model.fit(data)

		clusters = [data[model.labels_.astype('bool')],
					data[~model.labels_.astype('bool')]]

		# Identify negative cluster based on maximum std on y-axis
		neg_cluster = clusters[np.argmax([i[:,1].std() for i in clusters])]

		mu = neg_cluster[:, 0].mean()
		sigma = neg_cluster[:, 0].std()

		return mu + sigma_weight * sigma
	


	def get_marker_pair_thresh(self, data, scene, marker_pair, batch):
		"""
		:param data:
		:param scene:
		:param marker_pair:
		:param batch:
		:return:
		"""
		ratio_x = 0.75
		ratio_y = 0.5
		
		tmp = data[marker_pair].to_numpy()
		
		#TODO: parameterize thresh
		idx_select = (((tmp[:, 0] > 50) * (tmp[:, 1] > np.quantile(tmp[:, 1], ratio_y))) +
					((tmp[:, 1] > 50) * (tmp[:, 0] > np.quantile(tmp[:, 0], ratio_x))))
		
		marker_pair_data = tmp[idx_select]
		
		xlabel = marker_pair[0]
		ylabel = marker_pair[1]

		models = (('KMeans', 'magenta', cluster.KMeans(n_clusters=2)),
					('GMM',	'blue',  mixture.GaussianMixture(n_components=2, n_init=10)),
					('SSC',	'green', sr.SparseSubspaceClusteringOMP(n_clusters=2)))

		sigma_weight = 3 #TODO: parameterize
		
		if not batch == 'global':
			mydict = {'Scene': scene, 'Marker1': xlabel, 'Marker2': ylabel}
		
		for name, color, model in models:
			if name == 'GMM':
				thresh = self.get_GMM_thresh(marker_pair_data, model, sigma_weight)
			else:
				thresh = self.get_clustering_thresh(marker_pair_data, model, sigma_weight)
			
			self.threshs[batch][scene][xlabel][name] = thresh
			if not batch == 'global':
				if self.Debug:
					print("Entry => " + str(batch) + ", " + str(scene) + ", " + str(xlabel) + " vs " + str(ylabel)
									+ ", " + str(name) + " => " + str(thresh))
				mydict.update({name: thresh})
		
		if not batch == 'global':
			self.Thresholds.append(mydict)
	
	
	
	def SavePlots(self, OutputDir: str, Scene: str, Features, FigSize: int=7, Density: bool=True):
		"""
		:param OutputDir:
		:param Scene:
		:param Features:
		:param FigSize:
		:param Density:
		:return:
		"""
		
		length = len(self.Thresholds)
		nCols = 3
		nRows = int(length / nCols) + (0 if length % nCols == 0 else 1)
		figs, axs = plt.subplots(ncols=nCols, nrows=nRows, figsize=(FigSize * nCols, FigSize * nRows), squeeze=False)
		
		for results, count in zip(self.Thresholds, range(0, length)):
			mark1 = results['Marker1']
			mark2 = results['Marker2']
			kmeans = results['KMeans']
			GMM = results['GMM']
			SSC = results['SSC']
			
			if self.Debug:
				print("Plotting: '"+mark1+"' vs '"+mark2 + "' => " + str(kmeans)+", "+str(GMM)+", "+str(SSC))
			
			X = Features[[mark1, mark2]]
			Indexes = X[(X[mark1] < 5.0) | (X[mark2] < 5.0)].index
			X = X.drop(Indexes)
			
			ax = axs[int(count / nCols), count % nCols]
			ax.axvline(x=GMM, color='b', label='GMM')
			ax.axvline(x=SSC, color='r', label='SSC')
			if Density:
				values = np.vstack([X[mark1], X[mark2]])
				kernel = scipy.stats.gaussian_kde(values)(values)
				plot = seaborn.scatterplot(data=X, x=mark1, y=mark2, c=kernel, cmap="viridis", ax=ax)
			else:
				plot = seaborn.scatterplot(data=X, x=mark1, y=mark2, cmap="viridis", ax=ax)
			
			count += 1
			
		plt.savefig(OutputDir + "/" + Scene + " - Restore.pdf", format="pdf", dpi=150)
		#plt.savefig(OutputDir + "/" + Scene + " - Restore.png", dpi=150)
		#plt.show()
		plt.clf()
		plt.close(figs)



	def normalize_scene(self, scene):
		"""
		Normalization and figure generation
		:param scene:
		:return:
		"""
		if self.Debug:
			print("Scene = " + scene)
		
		scene_data = self.data[self.data.scene == scene]

		for marker_pair in self.marker_pairs:
			if self.Debug:
				print("Processing pair = " + str(marker_pair))
			
			self.get_marker_pair_thresh(scene_data, scene, marker_pair, 'global')
			
			for batch in set(scene_data.batch):
				batch_scene_data = scene_data[scene_data.batch == batch]
				self.get_marker_pair_thresh(batch_scene_data, scene, marker_pair, batch)
		
		if self.save_figs:
			self.SavePlots(self.save_dir, scene, scene_data)



	def run(self):
		os.makedirs(self.save_dir, exist_ok=True)

		scenes = set(self.data.scene)
		if self.Debug:
			print("Scenes found:")
			print(*scenes)
		for scene in scenes:
			if self.Debug:
				print("Processing scene '" + scene + "'.")
			self.normalize_scene(scene)
		
		if self.Debug:
			print("Final Thresholds:")
			print(*self.Thresholds, sep='\n')
		
		TF = pd.DataFrame(self.Thresholds, columns=['Scene', 'Marker1', 'Marker2', 'SSC', 'GMM', 'KMeans'])
		ThreshFile = TF.sort_values(by=['Scene', 'Marker1', 'Marker2'])
		ThreshFile.to_csv(self.save_dir + "/Restore_Thresholds.csv", index=False)





if __name__ == "__main__":
	
	path = '/Users/firetiti/Downloads/CyclicIF/StandaloneNew/./Test - 2048x2048 - Features/tmp/'
	mi = pd.read_csv(path + 'Restore.csv')
	
	pairs = [
		['aSMA - Rings', 'CD45 - Rings'],
		['aSMA - Rings', 'CK5 - Rings'],
		['aSMA - Rings', 'Ecad - Rings'],
		['AR - Rings', 'CK5 - Rings'],
		['AR - Rings', 'FOXP3 - Nuclei'],
		['CD20 - Rings', 'CK5 - Rings'],
		['CK5 - Rings', 'CD68 - Rings'],
		['CK5 - Rings', 'Vim - Rings'],
		['CK5 - Rings', 'CD4 - Rings'],
		['CK5 - Rings', 'CD45 - Rings'],
		['CD3 - Rings', 'CK5 - Rings'],
		['CD4 - Rings', 'CK5 - Rings'],
		['CD4 - Rings', 'Ecad - Rings'],
		['CD45 - Rings', 'CK5 - Rings'],
		['CD45 - Rings', 'CK8 - Rings'],
		['CD8 - Rings', 'CK5 - Rings'],
		['PD1 - Rings', 'CK5 - Rings'],
		['Ecad - Rings', 'CD68 - Rings'],
		['Ecad - Rings', 'CD4 - Rings'],
		['Vim - Rings', 'CD68 - Rings'],
		['Vim - Rings', 'CD45 - Rings'],
		['Vim - Rings', 'Ecad - Rings'],
		['CK8 - Rings', 'CD68 - Rings'],
		['CK8 - Rings', 'CD4 - Rings'],
		['CK8 - Rings', 'CD45 - Rings'],
		['CD44 - Rings', 'CK5 - Rings'],
		['FOXP3 - Rings', 'CK5 - Rings'],
		['FOXP3 - Rings', 'CK8 - Rings']
		]
	
	pairs2 = [
		['CD8 - Rings', 'CK5 - Rings'],
		['Ecad - Rings', 'CD68 - Rings'],
		['CK8 - Rings', 'CD45 - Rings'],
		['CD44 - Rings', 'CK5 - Rings']
		]
	
	pairs = [
		['aSMA - Rings', 'CD45 - Rings'],
		['aSMA - Rings', 'CK5 - Rings'],
		['aSMA - Rings', 'Ecad - Rings'],
		['AR - Rings', 'CK5 - Rings'],
		['AR - Rings', 'FOXP3 - Nuclei'],
		['CD20 - Rings', 'CK5 - Rings'],
		['CK5 - Rings', 'CD68 - Rings'],
		['CK5 - Rings', 'Vim - Rings'],
		['CK5 - Rings', 'CD4 - Rings'],
		['CK5 - Rings', 'CD45 - Rings'],
		['CD3 - Rings', 'CK5 - Rings'],
		['CD4 - Rings', 'CK5 - Rings'],
		['CD4 - Rings', 'Ecad - Rings'],
		['CD45 - Rings', 'CK5 - Rings'],
		['CD45 - Rings', 'CK8 - Rings'],
		['CD8 - Rings', 'CK5 - Rings'],
		['PD1 - Rings', 'CK5 - Rings'],
		['Ecad - Rings', 'CD68 - Rings'],
		['Ecad - Rings', 'CD4 - Rings'],
		['Vim - Rings', 'CD68 - Rings'],
		['Vim - Rings', 'CD45 - Rings'],
		['Vim - Rings', 'Ecad - Rings'],
		['CK8 - Rings', 'CD68 - Rings'],
		['CK8 - Rings', 'CD4 - Rings'],
		['CK8 - Rings', 'CD45 - Rings'],
		['CD44 - Rings', 'CK5 - Rings'],
		['FOXP3 - Rings', 'CK5 - Rings'],
		['FOXP3 - Rings', 'CK8 - Rings']
		]
	
	norm = Normalization(mi, pairs, path, Debug=True)
	norm.run()
	print('Restore Done!')
	sys.exit(0)
