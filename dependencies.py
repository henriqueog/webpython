import sys
import subprocess

def instalarDependencias(*bibliotecaDependencias):
	"""Tenta instalar pacotes que foram passados via parâmetro"""
	libsArgs = list(bibliotecaDependencias)
	for lib in libsArgs:
		subprocess.check_call([sys.executable, '-m', 'pip', 'install', lib])
