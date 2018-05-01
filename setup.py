from setuptools import setup

setup(
    name='photosync',
    version='1.0.2',
    packages=['photosync'],
    entry_points={
        'console_scripts': ['photosync = photosync.photosync:main']
    }
)
