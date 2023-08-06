from setuptools import setup, find_packages


setup(
    name='icdpicpy',
    version='1.2',
    license='MIT',
    author="Konstantin Botnar",
    author_email='kosta.botnar@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['data/*','config/*']},
    url='https://github.com/Industrial-Metagenomics/icdpicpy',
    keywords='EMR ISS NISS Mortality',
    install_requires=[
          'pandas',
      ],
)