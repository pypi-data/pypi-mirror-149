
from setuptools import setup, find_packages
from os import path
from io import open

here = path.abspath(path.dirname(__file__))
# fetch the long description from the README.md
#with open(path.join(here, 'README.md'), encoding='utf-8') as f:
#long_description = f.read()

setup(
    name='pythonscipytest3', 
    version='0.0.1',  
    description='',  
#    long_description=long_description,  
 #   long_description_content_type='text/markdown',  
    url='https://github.com/<username>/<project-name>',  
    author='',  
    author_email='',  

    # For a list of valid classifiers, see https://pypi.org/classifiers/
    classifiers=[  
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    keywords='simple python calculator',  
    # When your source code is in a subdirectory under the project root, e.g.
    # `src/`, it is require to define the `package_dir` argument.
    package_dir={'': 'src'}, 
    packages=find_packages(where='src'),  # Required
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*, <4',
)
#setup(
#    name='pythonscipymoduletest2',
#    version='0.6',
 #   license='MIT',
  #  author="Giorgos Myrianthous",
   # author_email='email@example.com',
    #packages=find_packages('src'),
   # package_dir={'': 'src'},
  #  url='https://github.com/gmyrianthous/example-publish-pypi',
   # keywords='example project',
    #install_requires=[
     #     'scikit-learn',
     # ],

#)
