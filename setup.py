from setuptools import setup

setup(
    name='reviews',
    version='0.1',
    py_modules=['reviews'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        reviews=reviews:cli
    ''',
)