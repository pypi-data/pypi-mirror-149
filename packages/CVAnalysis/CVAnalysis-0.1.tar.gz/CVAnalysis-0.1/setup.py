from setuptools import setup, find_packages


setup(
    name='CVAnalysis',
    version='0.1',
    license='GNU',
    author="Luca Fabbri",
    author_email='luca.fabbri98@outlook.it',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/lfabbri98/CV_Analysis_Library',
    keywords='capacitance, voltage, analysis, CV',
    install_requires=[
          'pandas',
          'scipy',
          'numpy',
          'matplotlib'
      ],

)