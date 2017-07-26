#!/usr/bin/env python
# -*- coding: utf-8 -*-
# El siguiente archivo obtiene los datos de Reuters RCV1-v2. Si los archivos no se encuentran en el directorio POR DEFINIR, los descarga.
# Ejemplo:
#	import reuters as r
#	data,label = r.load_data(subset='train',label='topics')

import numpy as np

import os

def descargar_subset(file_subset,d_path):
	command = 'scp servidor-utfsm@cardano.inf.santiago.usm.cl:~/reuters/' +  file_subset + ' ' + d_path
	os.system(command)

def descargar_label(file_label,d_path):
	command = 'scp servidor-utfsm@cardano.inf.santiago.usm.cl:~/reuters/' +  file_label + ' ' + d_path
	os.system(command)

def check_download(file_subset,file_label,d_path):
	if os.path.exists(d_path + file_subset) == False:
		descargar_subset(file_subset,d_path)
	
	if os.path.exists(d_path + file_label) == False:
		descargar_label(file_label,d_path)

def load_data(subset,label,n=-1,d_path='~/reuters/'):
	my_dir = os.path.expanduser(d_path)
	try:
		os.makedirs(my_dir)
	except OSError:
		if os.path.isdir(my_dir):
			pass
		else:
			raise

	file_subset = subset + '.dat'
	file_label = subset + '_' + label + '.dat'
	check_download(file_subset,file_label,my_dir)

	datafile = open(my_dir + file_subset,'r')
	labelfile = open(my_dir + file_label,'r')

	datalines = datafile.readlines()
	labellines = labelfile.readlines()

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