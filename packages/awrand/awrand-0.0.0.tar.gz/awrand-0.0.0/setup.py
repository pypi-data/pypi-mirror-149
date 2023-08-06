from setuptools import *


setup(
    name='awrand',
    version='0.0.0',
    packages=find_namespace_packages('inc'),
    package_dir={'awrand': 'inc/awrand'},
    install_requires=[
    
        ],
    python_requires='>=3.8',

    url='https://github.com/happyxianyu/awrand',
    license='Apache License 2.0',
    author='happyxianyu',
    author_email=' happyxianyu623@outlook.com',
    description='A random generator'
)
