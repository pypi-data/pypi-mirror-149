import pathlib
from setuptools import setup, find_packages
 
# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()


classifiers = [
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='cgr-pdfextract',
  version='3.0.9',
  description='Herramienta para la extracción de datos de los "Informes de Control Posterior" de la Contraloria General de la República" del Perú',
  long_description=README,
  long_description_content_type="text/markdown",
  url='',  
  author='Jelsin Palomino',
  author_email='jstpalomino@hotmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords=['Perú', 'Peru', 'contraloria', 'informes de control posterior'], 
  packages=find_packages(),
  install_requires=[''] 
)