
from setuptools import setup, find_packages

setup(
    name='house-pricing-package',
    version='1.0.0.4',
    license='MIT',
    author="Patrick Saade",
    author_email='patrick_saade@hotmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Patrick844/dsp-patrick-saade/',
    keywords='house pricing project',
    install_requires=[
          'scikit-learn',
          'pandas',
          'numpy',


      ],

)