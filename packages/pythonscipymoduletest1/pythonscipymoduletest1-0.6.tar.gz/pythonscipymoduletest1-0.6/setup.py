from setuptools import setup, find_packages
from scipy.linalg import *
import numpy as np
a=np.array([[9, 6, -5,2], [4, 5, -7,3], [-3, -4, 2,-5],[6,1,9,-5]])
b=np.array([17, 10, 20, 23])
x=solve(a, b)
x


setup(
    name='pythonscipymoduletest1',
    version='0.6',
    license='MIT',
    author="Giorgos Myrianthous",
    author_email='email@example.com',
    #packages=find_packages('src'),
   # package_dir={'': 'src'},
    url='https://github.com/gmyrianthous/example-publish-pypi',
    keywords='example project',
    install_requires=[
          'scikit-learn',
      ],

)
