from setuptools import setup, find_packages

setup(name='simple_exact_diagonalization_routines',
      version='0.11',
      description='A set of functions useful for quick exact diagonalization computations and checks.',
      url='https://github.com/marekgluza/simple_exact_diagonalization_routines',
      author='Marek Gluza',
      license='GPL-3.0',
      packages=find_packages('src'),
    package_dir={'': 'src'},
    install_requires=['numpy',                     
                      ],
      zip_safe=False)
