from setuptools import setup

setup(
    name='dungeon',
    version='0.0.1',
    entry_points={
        'console_scripts': [
            'dungeon=dungeon:devise'
        ]
    }
)
