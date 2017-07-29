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

usr = 'servidor-utfsm'
serv = 'cardano.inf.santiago.usm.cl'
scp = 'scp ' + usr + '@' + serv + ':'
dir = '~/reuters/'
ext = '.dat.tar.gz' 

#	Descarga subset.
#	file_subset: Archivo a descargar.
#	d_path: Ruta de descarga.
def descargar_subset(file_subset,d_path):
	command = scp + dir +  file_subset + ' ' + d_path
	subprocess.call(command.split())

#	Descarga label.
#	file_label: Archivo a descargar.
#	d_path: Ruta de descarga.
def descargar_label(file_label,d_path):
	command = scp + dir +  file_label + ' ' + d_path
	subprocess.call(command.split())

#	Verifica si es necesario descargar archivos.
#	file_subset: Nombre del archivo de subset.
#	file_label: Nombre del archivo de label.
#	d_path: Ruta de descarga
def check_download(file_subset,file_label,d_path):
	if os.path.exists(d_path + file_subset) == False:
		descargar_subset(file_subset,d_path)
	if os.path.exists(d_path + file_label) == False:
		descargar_label(file_label,d_path)

#	Verifica si los parametros son correctos.
#	subset: Nombre del subset.
#	label: Nombre del label.
def check_params(subset,label,n):
	if (subset != 'test' and subset != 'train'):
		raise ValueError("subset debe ser 'train' o 'test'. Se ingresó '%s'" % subset)
	if (label != 'topics' and label != 'regions' and label != 'industries'):
		raise ValueError("label debe ser 'topics', 'regions' o 'industries'. Se ingresó '%s'" % label)
	if (n<-1 or n==0 or isinstance(n,int)==False):
		raise ValueError("n debe ser un entero positivo. Se ingresó %d" %n)

#	Carga dataset.
#	subset: Nombre del subset.
#	label: Nombre del label.
#	n: Cantidad de elementos a considerar. -1 indica que se utilizarán todos.
#	d_path: Ruta de descarga.
def load_data(subset,label,n=-1,d_path='~/reuters/'):
	check_params(subset,label,n)
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
		# Realiza un ping para corroborar que se encuentre activo cardano.
		cmd = 'ping ' + serv + ' -c 1 -W 2'
		response = subprocess.check_output(
			cmd.split(),
			stderr=subprocess.STDOUT,
			universal_newlines=True
			)
		check_download(file_subset,file_label,my_dir)

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
		raise NameError("No se puede conectar con el servidor")
	except IOError:
		raise IOError("No se pueden abrir los archivos")