import setuptools

setuptools.setup(
    name='compactem',
    version='0.9.8',
    description='compactem',
    license="Apache 2.0",
    packages=setuptools.find_packages(exclude=['docs']),
    url="https://bitbucket.org/aghose/compactem",
    classifiers=[
            'Topic :: Scientific/Engineering',
            'Topic :: Scientific/Engineering :: Artificial Intelligence',
            'License :: OSI Approved :: Apache Software License',
            'Programming Language :: Python :: 3 :: Only',
    ],
    author="Abhishek Ghose",
    long_description="""This library implements a set of algorithms to create compact models: smaller versions of 
                        models with accuracy similar to their original version.  
                        
                        See https://compactem.readthedocs.io/en/latest/index.html""",
    long_description_content_type="text/markdown",
    python_requires='>=3.6',
    install_requires=['seaborn>=0.11.0', 'numpy>=1.18.2', 'scipy>=1.4.1', 'lightgbm>=3.0.0', 'hyperopt>=0.2.5',
                      'matplotlib>=3.3.3', 'pandas>=1.1.4', 'scikit_learn>=0.23.2', 'lipo>=1.2.2', 'pysot>=0.3.3']

)
