from setuptools import setup
setup(
    name = 'sclbl',
    version = '0.1.0',
    packages = ['sclbl'],
    entry_points = {
        'console_scripts': [
            'sclbl = sclbl.__main__:main'
        ]
    })
