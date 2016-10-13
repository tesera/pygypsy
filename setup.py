from codecs import open as codecs_open
from setuptools import setup, find_packages


with codecs_open('README.md', encoding='utf-8') as f:
    long_description = f.read()


setup(name='gypsy',
      version='0.0.1',
      description=u"Controlling Gypsy modules, and outputs",
      long_description=long_description,
      classifiers=[],
      keywords='',
      author=u"Julianno Sambatti",
      author_email='julianno.sambatti@tesera.com',
      url='',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      zip_safe=False,
      include_package_data=True,
      package_data={
          'gypsy': ['data/*'],
      },
      install_requires=[
          'click>=6.6',
          'pandas>=0.18.1',
          'scipy>=0.17.1',
      ],
      extras_require={
          'test': ['pytest>=2.9.1'],
          'dev': ['pytest>=2.9.1', 'sphinx>=1.4.1',
                  'pylint>=1.5.4', 'git-pylint-commit-hook>=2.1.1',
                  'pytest-cov>=2.3.1']
      },
      entry_points="""
      [console_scripts]
      gypsy=gypsy.scripts.cli:cli
      """
      )
