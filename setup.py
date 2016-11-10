from codecs import open as codecs_open
from setuptools import setup, find_packages


with codecs_open('README.md', encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()


setup(name='gypsy',
      version='0.0.1',
      description=u"Forestry Growth and Yield Projection System",
      long_description=LONG_DESCRIPTION,
      classifiers=[],
      keywords='',
      author=u"Julianno Sambatti, Jotham Apaloo, Ian Moss",
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
          'matplotlib>=1.5.2',
          'colorlog>=2.7.0',
      ],
      extras_require={
          'test': ['pytest==2.9.1', 'pytest-cov==2.4.0'],
          'lint': ['pylint==1.5.4'],
          'docs': ['sphinx==1.4.1'],
          'dev': ['git-pylint-commit-hook==2.1.1'],
          'analysis': ['jupyter>=1.0.0', 'scikit-learn>=0.18',
                       'snakeviz>=0.4.1'],
      },
      entry_points="""
      [console_scripts]
      gypsy=gypsy.scripts.cli:cli
      """
     )
