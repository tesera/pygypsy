import versioneer
from codecs import open as codecs_open
from setuptools import setup, find_packages, Extension

try:
    import numpy as np
except ImportError:
    msg = 'Numpy must be installed to install pygypsy'
    raise ImportError(msg)

from Cython.Build import cythonize

with codecs_open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


extensions = [
    Extension("pygypsy.basal_area_increment", ["pygypsy/basal_area_increment.pyx"],
              include_dirs = [np.get_include()]),
]


setup(name='pygypsy',
      version=versioneer.get_version(),
      cmdclass=versioneer.get_cmdclass(),
      description=u"Forestry Growth and Yield Projection System",
      long_description=LONG_DESCRIPTION,
      classifiers=[],
      keywords='',
      author=u"Julianno Sambatti, Jotham Apaloo, Ian Moss",
      author_email='julianno.sambatti@tesera.com',
      url='',
      license='',
      packages=find_packages(exclude=['tests']),
      ext_modules=cythonize(extensions),
      zip_safe=False,
      include_package_data=True,
      package_data={
          'pygypsy': ['scripts/config/*'],
      },
      install_requires=[
          'click>=6.6',
          'pandas>=0.18.1',
          'matplotlib>=1.5.2',
          'colorlog>=2.7.0',
          'jsonschema>=2.5.1',
          'boto3>=1.4.1',
          'boto>=2.43.0',
      ],
      extras_require={
          'test': ['pytest==2.9.1', 'pytest-cov==2.4.0'],
          'lint': ['pylint==1.5.4'],
          'docs': ['sphinx==1.4.1'],
          'dev': [
              'git-pylint-commit-hook==2.1.1',
              'Cython==0.25.1',
              'configparser==3.5.0', # compat for git-pylint-commit-hook
              'versioneer==0.17',
              'twine>=1.8.1',
          ],
          'analysis': [
              'jupyter>=1.0.0',
              'scikit-learn>=0.18',
              'snakeviz>=0.4.1',
          ],
      },
      entry_points="""
      [console_scripts]
      pygypsy=pygypsy.scripts.cli:cli
      """
     )
