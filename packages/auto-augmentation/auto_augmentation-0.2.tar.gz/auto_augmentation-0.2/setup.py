from setuptools import setup, find_packages


setup(
    name='auto_augmentation',
    version='0.2',
    author="Max RK",
    author_email='mjr3717@ic.ac.uk',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://gitlab.doc.ic.ac.uk/g21mscprj15/auto_augment',
    keywords='example project',
    install_requires=[
          'torch',
          'torchvision',
          'pygad',
          'numpy',
          'tqdm',
      ],

)