from setuptools import setup, find_packages


setup(
    name='MechEngPy',
    version='0.0.5',
    license='GPT-3',
    author="Valter Alvares Gonzaga Filho",
    author_email='valtergonzagafilho@gmail.com',
    packages=find_packages('MechEngPy'),
    package_dir={'': 'MechEngPy'},
    url='https://github.com/valtervg13/MechPy/tree/main/MechPy',
    keywords='Mechanical Engineering, Engineering, Mechanical Design, Machine Design',
    install_requires=[
          'NumPy',
          'MatPlotLib',
          'Scipy',
          'Pandas'
      ],

)
