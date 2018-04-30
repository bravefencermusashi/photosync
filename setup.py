from setuptools import setup

setup(
    name='photosync',
    version='1.0.1',
    packages=['photosync'],
    entry_points={
        'console_scripts': ['photosync = photosync.photosync:main']
    }
)
