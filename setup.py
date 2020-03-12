from setuptools import setup

setup(
    name='self',
    version='0.1.0',
    packages=['self'],
    entry_points={
        'console_scripts': [
            'self = self.main:main'
        ]
    },
)