from setuptools import *


setup(
    name='rmgr',
    version='0.0.2',
    packages=find_namespace_packages('inc'),
    package_dir={'rmgr': 'inc/rmgr'},
    install_requires=[
            'cbutil',
            'aiofile',
            'awrand'
        ],
    python_requires='>=3.8',

    url='https://github.com/happyxianyu/rmgr',
    license='Apache License 2.0',
    author='happyxianyu',
    author_email=' happyxianyu623@outlook.com',
    description=''
)
