#!/usr/bin/env python
# -*- coding: utf-8 -*-
# El siguiente archivo obtiene los datos de Reuters RCV1-v2. Si los archivos no se encuentran en el directorio POR DEFINIR, los descarga.
# Ejemplo:
#	import reuters as r
#	data,label = r.load_data(subset='train',label='topics')

import numpy as np
import subprocess
import tarfile
import os

cmd = 'scp servidor-utfsm@cardano.inf.santiago.usm.cl:~/reuters/'
ext = '.dat.tar.gz' 

def descargar_subset(file_subset,d_path):
	command = cmd +  file_subset + ' ' + d_path
	#os.system(command)
	subprocess.call(command.split())

def descargar_label(file_label,d_path):
	command = cmd +  file_label + ' ' + d_path
	#os.system(command)
	subprocess.call(command.split())

def check_download(file_subset,file_label,d_path):
	if os.path.exists(d_path + file_subset) == False:
		descargar_subset(file_subset,d_path)
	
	if os.path.exists(d_path + file_label) == False:
		descargar_label(file_label,d_path)

def check_params(subset,label):
	flag=1
	if (subset != 'test' and subset != 'train'):
		print "Subset debe set test o train"
		flag = 0
	if (label != 'topics' and label != 'regions' and label != 'industries'):
		print "label debe set topics, regions o industries"
		flag = 0
	return flag


def load_data(subset,label,n=-1,d_path='~/reuters/'):
	if check_params(subset,label):
		my_dir = os.path.expanduser(d_path)
		try:
			os.makedirs(my_dir)
		except OSError:
			if os.path.isdir(my_dir):
				pass
			else:
				raise

		file_subset = subset + ext
		file_label = subset + '_' + label + ext

		try:
			response = subprocess.check_output(
				'ping cardano.inf.santiago.usm.cl -c 1 -W 2'.split(),
				stderr=subprocess.STDOUT,  # get all output
				universal_newlines=True  # return string not bytes
				)
			check_download(file_subset,file_label,my_dir)
			#datafile = open(my_dir + file_subset,'r')
			#labelfile = open(my_dir + file_label,'r')
			#datalines = datafile.readlines()
			#labellines = labelfile.readlines()
			datafile = tarfile.open(my_dir + file_subset, "r:gz")
			for member in datafile.getmembers():
				f = datafile.extractfile(member)
				if f:
					datalines = f.readlines()

			labelfile = tarfile.open(my_dir + file_label, "r:gz")
			for member in labelfile.getmembers():
				f = labelfile.extractfile(member)
				if f:
					labellines = f.readlines()

			index = np.arange(len(datalines))
			np.random.shuffle(index)

			if n==-1:
				n=index.shape[0]

			data = np.array(datalines,dtype=object)[index[:n]]
			label = np.array(labellines,dtype=object)[index[:n]]

			datafile.close()
			labelfile.close()

			del datalines,labellines
			return data,label
		except subprocess.CalledProcessError:
			response = None
			print "No se puede conectar con el servidor"
		except IOError:
			print "No se pueden abrir los archivos"